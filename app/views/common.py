from flask_mail import Message
from flask import Blueprint, make_response, request, current_app
from app import mail

bp = Blueprint('common', __name__, template_folder='templates')


@bp.route(f'/error', methods=['POST'])
def error_report():
    domain = current_app.config['MAIL_DOMAIN']
    recipient = current_app.config['MAIL_RECIPIENT']
    msg = Message(subject="La Serpiente felhasználói hibajelentés",
                  sender=f"webmaster@{domain}",
                  recipients=[recipient])

    answer: str = request.form.get('answer')
    exercise: str = request.form.get('exercise')
    message: str = request.form.get('message')

    msg.body = f"üzenet: {message} \n\n" \
               f"gyakorlat: {exercise} \n\n" \
               f"válasz: {answer}"
    mail.send(msg)

    return make_response('', 200)
