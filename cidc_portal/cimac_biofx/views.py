from flask import Blueprint
from flask import render_template
from flask import session
from flask import request

from cidc_portal.auth.wrapper import requires_login, requires_roles

from cidc_portal.main.services.user import get_user_info
from cidc_portal.main.services.user import get_cimac_biofox_user_home_data
from cidc_portal.main.services.utils import base_user_info

from cidc_portal.main.services.utils import url_for_with_prefix

from constants import ADMIN_ROLE
from constants import CIMAC_BIOFX_ROLE

from flask import redirect

cimac_biofx_bp = Blueprint("cimac_biofx", __name__, template_folder="templates")


@cimac_biofx_bp.context_processor
def build_main_context():
    return base_user_info(session)


@cimac_biofx_bp.route("/cimac_biofx/home", methods=["GET"])
@requires_login()
@requires_roles([CIMAC_BIOFX_ROLE, ADMIN_ROLE])
def home():
    session["cidc_user_info"] = get_user_info(session["jwt_token"])

    user_home_data = get_cimac_biofox_user_home_data(session["jwt_token"])

    return render_template(
        "home.jinja2", jwt=session["jwt_token"], user_home_data=user_home_data
    )


@cimac_biofx_bp.route("/cimac_biofx/cli-install", methods=["GET"])
@requires_login()
@requires_roles([CIMAC_BIOFX_ROLE, ADMIN_ROLE])
def cli_install():
    session["cidc_user_info"] = get_user_info(session["jwt_token"])

    return render_template(
        "cli-install.jinja2", jwt=session["jwt_token"]
    )


@cimac_biofx_bp.route("/cimac_biofx/olink-upload", methods=["GET"])
@requires_login()
@requires_roles([CIMAC_BIOFX_ROLE, ADMIN_ROLE])
def olink_upload():
    session["cidc_user_info"] = get_user_info(session["jwt_token"])

    return render_template(
        "olink-upload.jinja2", jwt=session["jwt_token"]
    )
