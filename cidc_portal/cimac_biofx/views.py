from flask import Blueprint
from flask import render_template
from flask import session

from cidc_portal.auth.wrapper import requires_login, requires_roles

from cidc_portal.main.services.user import get_cimac_biofox_user_home_data

cimac_biofx_bp = Blueprint('cimac_biofx',
                           __name__,
                           template_folder='templates')


@cimac_biofx_bp.route('/cimac_biofx/home', methods=['GET'])
@requires_login()
@requires_roles(["CIMAC_BIOFX"])
def home():
    user_home_data = get_cimac_biofox_user_home_data(session["jwt_token"])

    return render_template('home.jinja2',
                           jwt=session["jwt_token"],
                           user_role=session["user_role"],
                           user_name=session["user_name"],
                           user_home_data=user_home_data)


@cimac_biofx_bp.route('/cimac_biofx/register', methods=['GET'])
@requires_login()
@requires_roles(["CIMAC_BIOFX"])
def register():
    return render_template('register.jinja2')


@cimac_biofx_bp.route('/cimac_biofx/coc', methods=['GET'])
@requires_login()
@requires_roles(["CIMAC_BIOFX"])
def coc():
    return render_template('coc.jinja2')
