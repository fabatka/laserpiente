import random

from flask import Blueprint, render_template, make_response, request, abort, current_app

from app.lang import pronoun_map_hr_db
from app.static.utils import execute_query

bp = Blueprint('quiz-indicativo-presente', __name__, template_folder='templates')

path = 'quiz-conj-dual-indicativo-presente'

query_which_verb = '''
select infinitivo, modo, tiempo
from laserpiente.verbo
order by random() 
limit 1'''

query_pronoun_for_verb = '''
select {pronoun}
from laserpiente.verbo
where infinitivo = %(verb)s
    and tiempo = %(tense)s
    and modo = %(mood)s'''


@bp.route(f'/{path}', methods=['GET'])
def quiz():
    try:
        question = execute_query(query_which_verb)[0]
        verb: str = question.get('infinitivo')
        mood: str = question.get('modo')
        tense: str = question.get('tiempo')
        possible_pronouns_hr = list(pronoun_map_hr_db.keys())
        if mood == 'imperativo':
            possible_pronouns_hr.remove('yo')
        pronoun_hr: str = random.choice(possible_pronouns_hr)
        input_width = max(len(pronoun_hr), len(verb))
        input_width_attr = f'width: calc(var(--textsize)*{input_width}*1)'
        quiz_subtitle = f'{mood.capitalize()}, {tense}'
        return render_template('quizpage-dual.html', quiz_subtitle=quiz_subtitle, question_hint=pronoun_hr,
                               question=verb,
                               quiz_title='Conjugación', input_width=input_width_attr)
    except TypeError as e:
        current_app.logging.error(f'most likely the query failed: {query_which_verb}. {str(e)}')
        abort(500)


@bp.route(f'/{path}-submit', methods=['POST'])
def submit():
    answer: str = request.form.get('answer')
    question: str = request.form.get('question')
    pronoun_hr: str = request.form.get('questionHint')
    subtitle: str = request.form.get('subtitle')
    # TODO: put quiz info into hidden element and get it from those
    subtitle_list = [word.strip().lower() for word in subtitle.split(', ')]
    mood = subtitle_list[0]
    tense = subtitle_list[1]

    pronoun_db = pronoun_map_hr_db[pronoun_hr]

    identifier_params = {'pronoun': pronoun_db}
    query_params = {'verb': question, 'tense': tense, 'mood': mood}
    solution: str = execute_query(query_pronoun_for_verb, query_params=query_params,
                                  identifier_params=identifier_params)[0].get(pronoun_db)

    if answer.strip().lower() == solution.strip().lower():
        response_text = '<p> <span class="correct">¡Correcto!</span></p>'
    else:
        response_text = f'<p> <span class="false">¡Incorrecto! </span>La solución: {solution}</p>'
    return make_response(response_text, 200)
