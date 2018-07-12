from flask import Blueprint
from flask import render_template
from flask import session

cimac_biofx_bp = Blueprint('cimac_biofx',
                    __name__,
                    template_folder='templates')


@cimac_biofx_bp.route('/cimac_biofx/home', methods=['GET'])
def home():
    return render_template('home.jinja2', jwt=session["jwt_token"])


@cimac_biofx_bp.route('/cimac_biofx/register', methods=['GET'])
def register():
    return render_template('register.jinja2')


@cimac_biofx_bp.route('/cimac_biofx/coc', methods=['GET'])
def coc():
    return render_template('coc.jinja2')