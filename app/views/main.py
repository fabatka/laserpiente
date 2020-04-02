from flask import Blueprint, render_template

bp = Blueprint('main', __name__, template_folder='templates')


@bp.route('/')
@bp.route('/home')
def home():
    return render_template('home.html')
