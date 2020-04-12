from random import randrange
from flask import Blueprint, render_template, make_response, request
from app.lang import numbers_map


bp = Blueprint('quiz-numeros', __name__, template_folder='templates')

path = 'quiz-numeros'


def translate_int_en_es(number: int) -> str:
    if number < 30:
        return numbers_map[str(number)]
    if number < 100:
        first_part = numbers_map[str((number // 10) * 10)]
        second_part = ' y ' + numbers_map[str(number % 10)] if numbers_map[str(number % 10)] != 'cero' else ''
        return first_part + second_part
    if number == 100:
        return numbers_map[str((number // 100) * 100)]
    if number < 200:
        return numbers_map[str((number // 100) * 100)] + 'to' + ' ' + translate_int_en_es(number % 100)
    if number < 1000:
        return numbers_map[str((number // 100)*100)] + ' ' + translate_int_en_es(number % 100)
    if number < 2000:
        return 'Un mil' + (' ' + translate_int_en_es(number % 1000) if number % 1000 != 0 else '')
    if number < 1e6:
        first_part = translate_int_en_es((number // 1000)) + ' mil'
        second_part = (' ' + translate_int_en_es(number % 1000)) if number % 1000 != 0 else ''
        return first_part + second_part
    if number < 2e6:
        return 'Un millón' + (' ' + translate_int_en_es(number % 1000000) if number % 1000000 != 0 else '')
    if number <= 1e9:
        first_part = translate_int_en_es((number // 1000000)) + ' millones'
        second_part = (' ' + translate_int_en_es(number % 1000000)) if number % 1000000 != 0 else ''
        return first_part + second_part
    else:
        raise ValueError


@bp.route(f'/{path}', methods=['GET'])
def quiz():
    question = randrange(0, 1e6)
    return render_template('quizpage-numeros.html', extra_class='numeros', question=str(question),
                           quiz_title='Práctica de números')


@bp.route(f'/{path}-submit', methods=['POST'])
def submit():
    answer: str = request.form.get('answer')
    question: str = request.form.get('question')
    solution = translate_int_en_es(int(question))
    if answer.strip().lower() == solution.strip().lower():
        response_text = '<p> <span class="correct">¡Correcto!</span></p>'
    else:
        response_text = f'<p> <span class="false">¡Incorrecto! </span>La solución: {solution}</p>'
    return make_response(response_text, 200)


@bp.route('/audio', methods=['POST'])
def speech2text():
    audio = request.files.get('file')
    with open('audio.wav', 'wb') as f:
        f.write(audio.read())

    return make_response('yay!', 200)
