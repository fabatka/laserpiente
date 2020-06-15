import json
import os
from datetime import datetime
from random import randrange
from requests import post, exceptions
from flask import Blueprint, render_template, make_response, request, current_app
from app.lang import numbers_map

from werkzeug.datastructures import FileStorage


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
    return render_template('quizpage-numeros.html', quiz_title='Práctica de números')


@bp.route(f'/{path}-submit', methods=['POST'])
def submit():
    answer: str = request.form.get('answer')
    question: str = request.form.get('question')
    solution = translate_int_en_es(int(question))
    if answer.strip().lower() == solution.strip().lower():
        response_text = '<span> <span class="correct">¡Correcto!</span></span>'
    else:
        response_text = f'<span> <span class="false">¡Incorrecto! </span>La solución: {solution}</span>'
    return make_response(response_text, 200)


@bp.route('/audio', methods=['POST'])
def speech2text():
    raw_audio: FileStorage = request.files.get('file')
    audio: bytes = raw_audio.read()

    # if the recording is too short, we don't even try to process it
    if (len(audio) / 1024) < 200:
        return make_response('', 200)

    filename = datetime.now().strftime('%Y-%m-%d_%H.%M.%S')
    if not os.path.exists('audio'):
        os.mkdir('audio')
    with open(f'audio/{filename}.wav', 'wb') as f:
        f.write(audio)

    azure_key = current_app.config['file']['azure']['key']
    azure_host = current_app.config['file']['azure']['host']
    azure_headers = {'Ocp-Apim-Subscription-Key': azure_key,
                     'Content-Type': 'audio/wav; codecs=audio/pcm; samplerate=16000'}
    azure_payload = audio
    current_app.logger.info('Sending audio to Azure for speech recognition')
    error_response_text = 'Hiba'
    try:
        speech2text_req = post(azure_host, headers=azure_headers, data=azure_payload)
        if speech2text_req.ok:
            current_app.logger.debug(speech2text_req.text)
            current_app.logger.info('Speech recognition request successful')
            response = json.loads(speech2text_req.text)
            speech2text_result = response['NBest'][0]['Lexical']
            return make_response(speech2text_result, 200)
        else:
            current_app.logger.error(f'Speect-to-text request unsuccessful. '
                                     f'Status code:{speech2text_req.status_code} '
                                     f'Reason:{speech2text_req.reason}')
            return make_response(error_response_text, 500)
    except exceptions.MissingSchema as err:
        current_app.logger.error(f'Unable to send speech-to-text request'
                                 f'Error: {err}')
        return make_response(error_response_text, 500)
