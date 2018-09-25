import datetime
import logging

from flask import Blueprint
from flask import render_template
from flask import session

from cidc_portal.auth.wrapper import requires_login, requires_roles

from cidc_portal.main.services.trials import fetch_trials
from cidc_portal.main.services.utils import base_user_info

from constants import ADMIN_ROLE
from constants import CIMAC_BIOFX_ROLE

trials_summary_bp = Blueprint("trials_summary", __name__, template_folder="templates")


@trials_summary_bp.context_processor
def build_main_context():

    return base_user_info(session)


@trials_summary_bp.route("/trials-summary", methods=["GET"])
@requires_login()
@requires_roles([CIMAC_BIOFX_ROLE, ADMIN_ROLE])
def home():
    trials = fetch_trials(session["jwt_token"])

    for trial in trials:
        try:
            trial["start_date"] = datetime.datetime.strptime(
                trial["start_date"], "%a, %d %b %Y %H:%M:%S GMT"
            ).date()

        except ValueError:
            logging.info(
                {
                    "message": "Error converting datetime to date for Trial.",
                    "category": "INFO-PORTAL",
                }
            )

        trial["assays_planned"] = 0

    return render_template("trials_summary.jinja2", trials=trials)
