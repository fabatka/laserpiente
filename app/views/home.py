import secrets

from flask import Blueprint, render_template, make_response

from app.static.utils import add_security_headers

bp = Blueprint('home', __name__, template_folder='templates')


@bp.route('/', methods=['GET'])
def home():
    nonce = secrets.token_urlsafe()
    return add_security_headers(make_response(render_template('home.html', nonce=nonce), 200), nonce)
