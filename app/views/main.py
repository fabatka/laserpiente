from flask import Blueprint

bp = Blueprint('main', __name__)


@bp.route('/')
@bp.route('/home')
def home():
    return 'Hello!'
