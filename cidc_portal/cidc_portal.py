from flask import Flask

app = Flask(__name__)


def create_app():

    from cidc_portal.main.views import main_bp
    from cidc_portal.cimac_biofx.views import cimac_biofx_bp

    app.register_blueprint(main_bp)
    app.register_blueprint(cimac_biofx_bp)

    return app
