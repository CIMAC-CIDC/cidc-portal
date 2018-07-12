from flask import Blueprint
from flask import redirect
from flask import current_app
from flask import session

from cidc_portal.auth.auth0 import establish_login_auth
from cidc_portal.auth.auth0 import callback_handling
from cidc_portal.auth.auth0 import get_auth0_login

main_bp = Blueprint('main',
                    __name__,
                    template_folder='templates')

auth0 = establish_login_auth(current_app)


@main_bp.route('/', methods=['GET'])
def index():
    return redirect("/login")


@main_bp.route('/login', methods=['GET'])
def login():
    return get_auth0_login(auth0)


@main_bp.route('/callback', methods=['GET'])
def callback_controller():
    session["jwt_token"] = callback_handling(auth0)

    # If the user got in okay, redirect them to appropriate page.
    user_role = "CIMAC_BIOFX"

    if user_role == "CIMAC_BIOFX":
        return redirect("/cimac_biofx/home")

    return redirect("/")
