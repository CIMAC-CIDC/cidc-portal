from flask import Blueprint
from flask import render_template
from flask import session
from flask import request

from cidc_portal.auth.wrapper import requires_login, requires_roles

from cidc_portal.main.services.utils import base_user_info

from cidc_portal.main.services.admin import fetch_users
from cidc_portal.main.services.trials import fetch_trials
from cidc_portal.main.services.admin import fetch_users_trials
from cidc_portal.main.services.admin import fetch_single_user

from cidc_portal.main.forms.registration import RegistrationForm

from constants import ADMIN_ROLE

admin_bp = Blueprint('admin',
                       __name__,
                       template_folder='templates')


@admin_bp.context_processor
def build_main_context():
    return base_user_info(session)


@admin_bp.route('/admin/home', methods=['GET'])
@requires_login()
@requires_roles([ADMIN_ROLE])
def home():
    user_list = fetch_users(session["jwt_token"])
    trials_list = fetch_trials(session["jwt_token"])
    return render_template('admin_home.jinja2',
                           users=user_list,
                           trials=trials_list)


@admin_bp.route('/admin/user_info', methods=['GET'])
@requires_login()
@requires_roles([ADMIN_ROLE])
def user_info():

    selected_user = request.args.get('user_id')

    retrieved_user_info = fetch_single_user(session["jwt_token"], selected_user)

    register_form = RegistrationForm(email=retrieved_user_info["e-mail"],
                                     contact_email=retrieved_user_info.get("preferred_contact_email"),
                                     organization=retrieved_user_info.get("organization"),
                                     first_n=retrieved_user_info.get("first_n"),
                                     last_n=retrieved_user_info.get("last_n"),
                                     cidc_role=retrieved_user_info.get("position_description"))

    users_trials = fetch_users_trials(session["jwt_token"], retrieved_user_info["e-mail"])

    return render_template('admin_user_info.jinja2',
                           retrieved_user_info=retrieved_user_info,
                           register_form=register_form,
                           users_trials=users_trials)
