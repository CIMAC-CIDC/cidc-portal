import logging
from datetime import timedelta

from cidc_utils.loghandler import StackdriverJsonFormatter
from flask import Flask, session
from flask_cdn import CDN

from constants import FLASK_SECRET_KEY, SESSION_TIMEOUT_MINUTES

APP = Flask(__name__, static_folder='static')
APP.config["SECRET_KEY"] = FLASK_SECRET_KEY
APP.config['CDN_DOMAIN'] = "https://storage.googleapis.com/cidc-js-build/"
APP.url_map.strict_slashes = False
CDN_INSTANCE = CDN()


def configure_logging():
    """
    Configures the loghandler to send formatted logs to stackdriver.
    """
    # Configure Stackdriver logging.
    logger = logging.getLogger()
    logger.setLevel("INFO")
    log_handler = logging.StreamHandler()
    log_handler.setFormatter(StackdriverJsonFormatter())
    logger.addHandler(log_handler)
    logging.info({"message": "LOGGER CONFIGURED", "category": "INFO-EVE-LOGGING"})


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
    CDN_INSTANCE.init_app(APP)
    return APP
