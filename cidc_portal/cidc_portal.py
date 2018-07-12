from flask import Flask

APP = Flask(__name__)


def create_app():

    from cidc_portal.main.views import main_bp
    from cidc_portal.cimac_biofx.views import cimac_biofx_bp

    APP.register_blueprint(main_bp)
    APP.register_blueprint(cimac_biofx_bp)

    return APP
