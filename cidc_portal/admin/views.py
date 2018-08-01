from flask import Blueprint
from flask import render_template
from flask import session

from cidc_portal.auth.wrapper import requires_login, requires_roles

from cidc_portal.main.services.utils import base_user_info

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
    return render_template('admin_home.jinja2')

