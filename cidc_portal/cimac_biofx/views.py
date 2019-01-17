from flask import Blueprint
from flask import render_template
from flask import session
from flask import request

from cidc_portal.auth.wrapper import requires_login, requires_roles

from cidc_portal.main.services.user import get_user_info
from cidc_portal.main.services.user import get_cimac_biofox_user_home_data
from cidc_portal.main.services.uploads import get_olink_status
from cidc_portal.main.services.uploads import remove_data_record
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


@cimac_biofx_bp.route("/cimac_biofx/uploads", methods=["GET"])
@requires_login()
@requires_roles([CIMAC_BIOFX_ROLE, ADMIN_ROLE])
def uploads():
    session["cidc_user_info"] = get_user_info(session["jwt_token"])

    olink_uploads = get_olink_status(session["jwt_token"])

    return render_template(
        "upload_status.jinja2", jwt=session["jwt_token"],
        olink_uploads=olink_uploads,
        remove_uploaded_file_url=url_for_with_prefix("/cimac_biofx/remove-upload")
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


@cimac_biofx_bp.route("/cimac_biofx/remove-upload", methods=["POST"])
@requires_login()
@requires_roles([CIMAC_BIOFX_ROLE, ADMIN_ROLE])
def remove_upload():
    session["cidc_user_info"] = get_user_info(session["jwt_token"])

    data_id = request.form.get("data_id")

    remove_data_record(session["jwt_token"], data_id)

    return redirect(url_for_with_prefix("/cimac_biofx/uploads"))


@cimac_biofx_bp.route("/cimac_biofx/browse-files", methods=["GET"])
@requires_login()
@requires_roles([CIMAC_BIOFX_ROLE, ADMIN_ROLE])
def browse_files():
    session["cidc_user_info"] = get_user_info(session["jwt_token"])

    return render_template('react.jinja2')


@cimac_biofx_bp.route("/cimac_biofx/wes-pipeline", methods=["GET"])
@requires_login()
@requires_roles([CIMAC_BIOFX_ROLE, ADMIN_ROLE])
def wes_pipeline():
    session["cidc_user_info"] = get_user_info(session["jwt_token"])

    return render_template('react.jinja2')


@cimac_biofx_bp.route("/cimac_biofx/wes-upload", methods=["GET"])
@requires_login()
@requires_roles([CIMAC_BIOFX_ROLE, ADMIN_ROLE])
def wes_upload_instructions():
    session["cidc_user_info"] = get_user_info(session["jwt_token"])

    return render_template('react.jinja2')
