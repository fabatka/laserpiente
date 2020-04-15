from flask import Blueprint, make_response, request

bp = Blueprint('common', __name__, template_folder='templates')


@bp.route(f'/error', methods=['POST'])
def error_report():
    answer: str = request.form.get('answer')
    exercise: str = request.form.get('exercise')
    message: str = request.form.get('message')

    return make_response('', 200)
