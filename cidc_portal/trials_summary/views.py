from flask import Blueprint
from flask import render_template
from cidc_portal.auth.auth0 import requires_login, requires_roles

trials_summary_bp = Blueprint('trials_summary',
                           __name__,
                           template_folder='templates')


@trials_summary_bp.route('/trials-summary', methods=['GET'])
@requires_login
@requires_roles("cimac_biofx", "cidc_user")
def home():
    trials_object = [{"trial_name": "Trial 1",
                      "start_date": "01/01/2001",
                      "drug_tested": "DRUG1",
                      "samples": []},
                     {"trial_name": "Trial 2", "start_date": "02/01/2001"}]

    return render_template('trials_summary.jinja2', trials_object=trials_object)
