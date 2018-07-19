from flask import Blueprint
from flask import redirect
from flask import current_app
from flask import session

from cidc_portal.auth.auth0 import establish_login_auth
from cidc_portal.auth.auth0 import callback_handling
from cidc_portal.auth.auth0 import get_auth0_login

from cidc_portal.main.services.user import get_user_role

from constants import URL_PREFIX

main_bp = Blueprint('main',
                    __name__,
                    template_folder='templates')

auth0 = establish_login_auth(current_app)


def url_for_with_prefix(url):
    return "%s%s" % (URL_PREFIX, url)


@main_bp.route('/', methods=['GET'])
def index():

    if "jwt_token" in session and session["jwt_token"] is not None:

        # If the user is logged in, direct them to their roles homepage.
        user_role = "CIMAC_BIOFX"

        if user_role == "CIMAC_BIOFX":
            return redirect(url_for_with_prefix("/cimac_biofx/home"))

    return redirect(url_for_with_prefix("/login"))


@main_bp.route('/logout', methods=['GET'])
def logout():

    if 'jwt_token' in session:
        del session['jwt_token']

    session.clear()

    return redirect(url_for_with_prefix("/login"))


@main_bp.route('/login', methods=['GET'])
def login():

    return get_auth0_login(auth0)


@main_bp.route('/callback', methods=['GET'])
def callback_controller():
    session["jwt_token"], user_payload = callback_handling(auth0)

    # After login, get user's role from Eve
    session["user_role"] = get_user_role(session["jwt_token"])

    session["user_name"] = user_payload["email"]

    return redirect(url_for_with_prefix("/"))
