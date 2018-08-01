import requests
import logging

from authlib.flask.client import OAuth

from flask import _request_ctx_stack

from jose import jwt

from constants import (
    AUTH0_CLIENT_ID,
    AUTH0_CLIENT_SECRET,
    AUTH0_DOMAIN,
    AUTH0_CALLBACK_URL,
    AUTH0_AUDIENCE,
    ALGORITHMS
)


def establish_login_auth(app):

    oauth = OAuth(app)

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
    access_tokens = login_auth.authorize_access_token(audience=AUTH0_AUDIENCE)

    payload = token_auth(access_tokens["id_token"])

    return access_tokens["id_token"], payload



# TODO: This is all repeated from ingestion-api
# Format error response and append status code.
class AuthError(Exception):
    """[summary]

    Arguments:
        Exception {[type]} -- [description]
    """
    def __init__(self, error, status_code):
        self.error = error
        self.status_code = status_code


def get_rsa_key(token):
    json_url = "https://" + AUTH0_DOMAIN + "/.well-known/jwks.json"
    jwks = requests.get(json_url).json()

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

    return rsa_key


def token_auth(token):
    """
    Checks if the supplied token is valid.
    """

    if not token:
        raise AuthError(
            {
                "code": "token_missing",
                "description": "Token was missing in callback"
            },
            401
        )

    logging.info({
        'message': "Getting RSA Key",
        'category': 'FAIR-PORTAL-RSAKEY'
    })

    rsa_key = get_rsa_key(token)

    if rsa_key:
        try:
            payload = jwt.decode(
                token,
                rsa_key,
                algorithms=ALGORITHMS,
                audience=AUTH0_CLIENT_ID,
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

        _request_ctx_stack.top.current_user = payload

        return payload

    raise AuthError(
        {
            "code": "invalid_header",
            "description": "Unable to find appropriate key"
        },
        401
    )
