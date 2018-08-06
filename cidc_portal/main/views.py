from flask import Blueprint
from flask import redirect
from flask import current_app
from flask import session
from flask import render_template
from flask import request

from constants import ADMIN_ROLE
from constants import CIMAC_BIOFX_ROLE
from constants import REGISTRANT_ROLE

from cidc_portal.auth.auth0 import establish_login_auth
from cidc_portal.auth.auth0 import callback_handling
from cidc_portal.auth.auth0 import get_auth0_login

from cidc_portal.main.services.user import get_user_info, update_user_info
from cidc_portal.auth.wrapper import requires_login, requires_roles

from .services.utils import url_for_with_prefix
from .services.utils import base_user_info

from .forms.registration import RegistrationForm

main_bp = Blueprint('main',
                    __name__,
                    template_folder='templates')

auth0 = establish_login_auth(current_app)


@main_bp.context_processor
def build_main_context():
    return base_user_info(session)


@main_bp.route('/privacy', methods=['GET'])
def privacy():
    return render_template('privacy.jinja2')


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

    # After login, get user's info from Eve
    session["cidc_user_info"] = get_user_info(session["jwt_token"])
    session["user_name"] = user_payload["email"]

    return redirect(url_for_with_prefix("/"))


@main_bp.route('/', methods=['GET'])
def index():
    if "jwt_token" in session and session["jwt_token"] is not None:

        session["cidc_user_info"] = get_user_info(session["jwt_token"])

        # This will be None if the user's token was invalid for any reason.
        if session["cidc_user_info"] is not None:
            # If the user is logged in, direct them to their roles homepage.
            if session["cidc_user_info"]["role"] == CIMAC_BIOFX_ROLE:
                return redirect(url_for_with_prefix("/cimac_biofx/home"))
            elif session["cidc_user_info"]["role"] == REGISTRANT_ROLE:

                # Check if user's registration is filled out.
                if session["cidc_user_info"]["registered"]:
                    return redirect(url_for_with_prefix("/register"))
                else:
                    return redirect(url_for_with_prefix("/request_pending"))

            elif session["cidc_user_info"]["role"] == ADMIN_ROLE:
                return redirect(url_for_with_prefix("/trials-summary"))

        # The user's JWT was invalid but they have a session, clear their session and start over again.
        return redirect(url_for_with_prefix("/logout"))
    return redirect(url_for_with_prefix("/login"))


@main_bp.route('/register', methods=['GET', 'POST'])
@requires_login()
@requires_roles([REGISTRANT_ROLE, ADMIN_ROLE])
def register():
    session["cidc_user_info"] = get_user_info(session["jwt_token"])

    if session["cidc_user_info"]["role"] is None:
        return redirect(url_for_with_prefix("/logout"))

    # If a user has already submitted a registration, bounce them to wait page.
    if session["cidc_user_info"]["registered"]:
        return redirect(url_for_with_prefix("/request_pending"))

    register_form = RegistrationForm(request.form)

    # Form submission method.
    if request.method == 'POST':
        if register_form.validate():
            update_user_info(session["jwt_token"], register_form)
            return redirect(url_for_with_prefix("/request_pending"))
        else:

            render_template('register.jinja2',
                            save_url=url_for_with_prefix("/register"),
                            register_form=register_form)
    return render_template('register.jinja2',
                           save_url=url_for_with_prefix("/register"),
                           register_form=register_form)


@main_bp.route('/request_pending', methods=['GET'])
@requires_login()
def request_pending():
    session["cidc_user_info"] = get_user_info(session["jwt_token"])

    if session["cidc_user_info"]["role"] is None:
        return redirect(url_for_with_prefix("/logout"))

    # If a previously registered/accepted user visits this page, redirect them to the index.
    if session["cidc_user_info"]["role"] != REGISTRANT_ROLE:
        return redirect(url_for_with_prefix("/"))

    # If a user makes it here without filling out registration form, bounce them there.
    if not session["cidc_user_info"]["registered"]:
        return redirect(url_for_with_prefix("/register"))

    return render_template('request-pending.jinja2')
