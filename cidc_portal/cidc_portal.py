from flask import Flask

from constants import FLASK_SECRET_KEY

APP = Flask(__name__)
APP.config['SECRET_KEY'] = FLASK_SECRET_KEY


def create_app():

    from cidc_portal.main.views import main_bp
    from cidc_portal.cimac_biofx.views import cimac_biofx_bp
    from cidc_portal.trials_summary.views import trials_summary_bp

    APP.register_blueprint(main_bp)
    APP.register_blueprint(cimac_biofx_bp)
    APP.register_blueprint(trials_summary_bp)

    return APP
