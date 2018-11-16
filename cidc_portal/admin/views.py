from flask import Blueprint
from flask import render_template
from flask import session
from flask import request
from flask import redirect

from cidc_portal.auth.wrapper import requires_login, requires_roles

from cidc_portal.main.services.utils import base_user_info

from cidc_portal.main.services.admin import fetch_users
from cidc_portal.main.services.trials import fetch_trials
from cidc_portal.main.services.admin import fetch_users_trials
from cidc_portal.main.services.admin import fetch_single_user
from cidc_portal.main.services.admin import change_user_role
from cidc_portal.main.services.admin import add_user_to_trial
from cidc_portal.main.services.admin import remove_user_from_trial
from cidc_portal.main.services.assays import fetch_assays

from cidc_portal.main.forms.registration import RegistrationForm

from cidc_portal.main.services.utils import url_for_with_prefix

from constants import ADMIN_ROLE
from constants import ROLE_LIST

from cidc_portal.main.services.admin import TRIAL_ASSAY_PERMISSION_TYPES

admin_bp = Blueprint("admin", __name__, template_folder="templates")


@admin_bp.context_processor
def build_main_context():
    return base_user_info(session)


@admin_bp.route("/admin/home", methods=["GET"])
@requires_login()
@requires_roles([ADMIN_ROLE])
def home():
    user_list = fetch_users(session["jwt_token"])
    trials_list = fetch_trials(session["jwt_token"])
    return render_template("admin_home.jinja2", users=user_list, trials=trials_list)


@admin_bp.route("/admin/user_info", methods=["GET"])
@requires_login()
@requires_roles([ADMIN_ROLE])
def user_info():
    selected_user = request.args.get("user_id")

    all_trials = fetch_trials(session["jwt_token"])
    all_assays = fetch_assays(session["jwt_token"])

    retrieved_user_info = fetch_single_user(session["jwt_token"], selected_user)

    register_form = RegistrationForm(
        email=retrieved_user_info["email"],
        contact_email=retrieved_user_info.get("preferred_contact_email"),
        organization=retrieved_user_info.get("organization"),
        first_n=retrieved_user_info.get("first_n"),
        last_n=retrieved_user_info.get("last_n"),
        cidc_role=retrieved_user_info.get("position_description"),
        permissions=retrieved_user_info.get("permissions"),
    )

    # Fetch trials the user is a collaborator on.
    users_trials = fetch_users_trials(
        session["jwt_token"], retrieved_user_info["email"]
    )["_items"]

    # Build a dict with the fancy names for the objects that make up permissions.
    permission_display = []

    for permission in retrieved_user_info["permissions"]:
        trial_name = next(
            (trial for trial in all_trials if trial["_id"] == permission["trial"]), None
        )["trial_name"]

        assay_name = next(
            (assay for assay in all_assays if assay["_id"] == permission["assay"]), None
        )["assay_name"]

        permission_display.append(
            {"trial": trial_name, "assay": assay_name, "role": permission["role"]}
        )

    return render_template(
        "admin_user_info.jinja2",
        retrieved_user_info=retrieved_user_info,
        register_form=register_form,
        users_trials=users_trials,
        role_list=ROLE_LIST,
        update_role_url=url_for_with_prefix("/admin/update_role"),
        add_user_to_trial_url=url_for_with_prefix("/admin/add_user_trial"),
        remove_user_from_trial_url=url_for_with_prefix("/admin/remove_user_from_trial"),
        trial_assay_permission_types=TRIAL_ASSAY_PERMISSION_TYPES,
        assays=all_assays,
        all_trials=all_trials,
        permissions_display=permission_display,
    )


@admin_bp.route("/admin/update_role", methods=["POST"])
@requires_login()
@requires_roles([ADMIN_ROLE])
def update_role():
    user_id = request.form.get("user_id")
    new_role = request.form.get("system_role")

    change_user_role(session["jwt_token"], user_id, new_role)

    return redirect(url_for_with_prefix("/admin/user_info?user_id=%s" % user_id))


@admin_bp.route("/admin/add_user_trial", methods=["POST"])
@requires_login()
@requires_roles([ADMIN_ROLE])
def add_user_trial():
    user_id = request.form.get("user_id")
    new_trial = request.form.get("add_user_to_trial")
    assay_type = request.form.get("assay_type")
    trial_permission = request.form.get("trial_permission")

    add_user_to_trial(
        session["jwt_token"], new_trial, [user_id], assay_type, trial_permission
    )

    return redirect(url_for_with_prefix("/admin/user_info?user_id=%s" % user_id))


@admin_bp.route("/admin/remove_user_from_trial", methods=["POST"])
@requires_login()
@requires_roles([ADMIN_ROLE])
def remove_user_trial():
    user_id = request.form.get("user_id")
    new_trial = request.form.get("remove_user_from_trial")

    remove_user_from_trial(session["jwt_token"], new_trial, [user_id])

    return redirect(url_for_with_prefix("/admin/user_info?user_id=%s" % user_id))
