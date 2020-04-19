import re
from flask import Blueprint, render_template, request

bp = Blueprint('error_handlers', __name__, template_folder='templates')


@bp.app_errorhandler(404)
def not_found(_):
    return render_template('404.html'), 404


@bp.app_errorhandler(500)
def server_error(error):

    # a quiz-submit requestekre a válasz html, de csak formázott szöveg, és nem egy teljes weboldal
    if re.search(r'/quiz-.*-submit', request.path):
        inline_message = '<strong>Hiba történt!</strong> Az oldal karbantartója értesítve lett, ' \
                         'elnézést a kellemetlenségért'
        return inline_message

    return render_template('500.html'), 500
