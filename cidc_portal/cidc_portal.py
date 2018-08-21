from flask import Flask
from flask import session
from datetime import timedelta

from constants import FLASK_SECRET_KEY
from constants import SESSION_TIMEOUT_MINUTES

from cidc_utils.loghandler import StackdriverJsonFormatter

import logging

APP = Flask(__name__)
APP.config['SECRET_KEY'] = FLASK_SECRET_KEY


def configure_logging():
    """
    Configures the loghandler to send formatted logs to stackdriver.
    """
    # Configure Stackdriver logging.
    logger = logging.getLogger()
    logger.setLevel('INFO')
    log_handler = logging.StreamHandler()
    log_handler.setFormatter(StackdriverJsonFormatter())
    logger.addHandler(log_handler)
    logging.info({
        'message': 'LOGGER CONFIGURED',
        'category': 'INFO-EVE-LOGGING'
    })


@APP.before_request
def make_session_permanent():
    """
    Sets the Flask session to expire based on a timeout.
    :return:
    """
    session.permanent = True
    APP.permanent_session_lifetime = timedelta(minutes=SESSION_TIMEOUT_MINUTES)


def create_app():

    from cidc_portal.main.views import main_bp
    from cidc_portal.cimac_biofx.views import cimac_biofx_bp
    from cidc_portal.trials_summary.views import trials_summary_bp
    from cidc_portal.admin.views import admin_bp

    APP.register_blueprint(main_bp)
    APP.register_blueprint(cimac_biofx_bp)
    APP.register_blueprint(trials_summary_bp)
    APP.register_blueprint(admin_bp)

    configure_logging()

    return APP
