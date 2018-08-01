from flask import Blueprint
from flask import render_template
from flask import session

from cidc_portal.auth.wrapper import requires_login, requires_roles

from cidc_portal.main.services.utils import base_user_info

from constants import ADMIN_ROLE
from constants import CIMAC_BIOFX_ROLE

trials_summary_bp = Blueprint('trials_summary',
                           __name__,
                           template_folder='templates')


@trials_summary_bp.context_processor
def build_main_context():
    return base_user_info(session)


@trials_summary_bp.route('/trials-summary', methods=['GET'])
@requires_login()
@requires_roles([CIMAC_BIOFX_ROLE, ADMIN_ROLE])
def home():

    trials_object = [{"trial_name": "Trial 1",
                      "start_date": "01/01/2001",
                      "drug_tested": "DRUG1",
                      "samples": []},
                     {"trial_name": "Trial 2", "start_date": "02/01/2001"}]

    return render_template('trials_summary.jinja2',
                           trials_object=trials_object)
