from flask import Blueprint, render_template, request

bp = Blueprint('error_handlers', __name__, template_folder='templates')


@bp.app_errorhandler(404)
def not_found(_):
    return render_template('404.html'), 404


@bp.app_errorhandler(500)
def server_error(error):
    request.url
    return render_template('500.html'), 500
