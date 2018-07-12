import requests
import json

from urllib.request import urlopen
from authlib.flask.client import OAuth as OAuth_authlib
from flask import _request_ctx_stack

from constants import (
    AUTH0_CLIENT_ID,
    AUTH0_CLIENT_SECRET,
    AUTH0_DOMAIN,
    AUTH0_CALLBACK_URL,
    AUTH0_AUDIENCE,
    ALGORITHMS
)


def establish_login_auth(app):

    oauth = OAuth_authlib(app)

    auth0 = oauth.register(
        'auth0',
        client_id=AUTH0_CLIENT_ID,
        client_secret=AUTH0_CLIENT_SECRET,
        api_base_url='https://%s/' % AUTH0_DOMAIN,
        access_token_url='https://%s/oauth/token' % AUTH0_DOMAIN,
        authorize_url='https://%s/authorize' % AUTH0_DOMAIN,
        client_kwargs={
            'scope': 'openid profile email',
        },
    )

    return auth0


def get_auth0_login(login_auth):
    return login_auth.authorize_redirect(redirect_uri=AUTH0_CALLBACK_URL,
                                         audience=AUTH0_AUDIENCE)


def callback_handling(login_auth):
    # Handles response from token endpoint
    access_tokens = login_auth.authorize_access_token()

    return access_tokens["id_token"]


# TODO: This is repeated from ingestion-api
# Format error response and append status code.
class AuthError(Exception):
    """[summary]

    Arguments:
        Exception {[type]} -- [description]
    """
    def __init__(self, error, status_code):
        self.error = error
        self.status_code = status_code


def token_auth(token):
    """
    Checks if the supplied token is valid.
    """
    json_url = "https://" + AUTH0_DOMAIN + "/.well-known/jwks.json"
    jsonurl = urlopen(json_url)
    jwks = json.loads(jsonurl.read())

    if not token:
        print('no token received')
        return False

    unverified_header = None
    try:
        unverified_header = jwt.get_unverified_header(token)
    except jwt.JWTError as err:
        print(err)

    if not jwks:
        print('no jwks')
        return False

    rsa_key = {}
    for key in jwks["keys"]:
        if key["kid"] == unverified_header["kid"]:
            rsa_key = {
                "kty": key["kty"],
                "kid": key["kid"],
                "use": key["use"],
                "n": key["n"],
                "e": key["e"]
            }
    if rsa_key:
        try:
            payload = jwt.decode(
                token,
                rsa_key,
                algorithms=ALGORITHMS,
                audience=AUTH0_AUDIENCE,
                issuer="https://"+AUTH0_DOMAIN+"/"
            )
        except jwt.ExpiredSignatureError:
            print('Expired Signature Error')
            raise AuthError(
                {
                    "code": "token_expired",
                    "description": "token is expired"
                },
                401
            )
        except jwt.JWTClaimsError as claims:
            print(claims)
            raise AuthError(
                {
                    "code": "invalid_claims",
                    "description": "incorrect claims, please check the audience and issuer"
                },
                401
            )
        except Exception as err:
            print(err)
            raise AuthError(
                {
                    "code": "invalid_header",
                    "description": "Unable to parse authentication token."
                },
                401
            )

        # Get user e-mail from userinfo endpoint.
        if 'gty' not in payload:
            res = requests.get(
                'https://cidc-test.auth0.com/userinfo',
                headers={"Authorization": 'Bearer {}'.format(token)}
            )

            if not res.status_code == 200:
                print("There was an error fetching user information")
                raise AuthError(
                    {
                        "code": "No_info",
                        "description": "No userinfo found at endpoint"
                    },
                    401
                )

            payload['email'] = res.json()['email']
            _request_ctx_stack.top.current_user = payload
            return True
        else:
            payload['email'] = "taskmanager-client"
            _request_ctx_stack.top.current_user = payload
            return True
    raise AuthError(
        {
            "code": "invalid_header",
            "description": "Unable to find appropriate key"
        },
        401
    )
