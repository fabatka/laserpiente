import random
import secrets

from flask import Blueprint, render_template, make_response, request, abort, current_app, jsonify

from app.lang import pronoun_map_hr_db
from app.static.utils import execute_query, add_security_headers

bp = Blueprint('quiz-indicativo-presente', __name__, template_folder='templates')

path = 'quiz-conjugacion'

query_which_verb = '''
select infinitivo, modo, tiempo
from laserpiente.verbo
where modo || '_' || tiempo in ({modos_tiempos})
order by random() 
limit 1
'''

query_pronoun_for_verb = '''
select {pronoun}
from laserpiente.verbo
where infinitivo = %(verb)s
    and tiempo = %(tense)s
    and modo = %(mood)s
'''

query_tenses_for_moods = '''
select modo,
       array_agg(distinct tiempo) as tiempos
from laserpiente.verbo
group by modo
order by modo
'''

query_moods_tenses = '''
select distinct modo || '_' || tiempo as mood_tense,
       initcap(modo) || initcap(tiempo) as moodtense
from laserpiente.verbo
'''


@bp.route(f'/{path}', methods=['GET', 'POST'])
def quiz():
    nonce = secrets.token_urlsafe()
    # the options for what kind mood and tense to NOT use are stored in cookies
    # the cookie format is "mood_tense" without the double quotes
    # if for a combination there is no cookie, it means that it can be used
    # a cookie only exists if the given mood-tense pair can't be used
    try:
        # find out what moods and tenses to ask, format query and gen query params
        moods_tenses = [row['mood_tense'] for row in execute_query(query_moods_tenses)]
        MoodTenses = [row['moodtense'] for row in execute_query(query_moods_tenses)]
        moods_tenses = [m_t for m_t, MT in zip(moods_tenses, MoodTenses) if not request.cookies.get(MT)]
        current_app.logger.debug(f'{moods_tenses=}')
        tenses_for_moods = {
            row['modo'].capitalize(): [tiempo.capitalize() for tiempo in row['tiempos']]
            for row in execute_query(query_tenses_for_moods)
        }
        if len(moods_tenses) == 0:
            template = render_template('quizpage-conjugacion.html', moods=tenses_for_moods,
                                       quiz_subtitle='No ha seleccionado modos y tiempos verbales', question_hint='',
                                       question=':(', quiz_title='Conjugación', input_width='')
            response = add_security_headers(make_response(template, 200), nonce)
            return response
        param_name = 'm_t'
        param_fmt = f'%({param_name}{{i}})s'
        m_t_params = ', '.join([param_fmt.format(i=i) for i in range(len(moods_tenses))])
        query_which_verb_fmt = query_which_verb.format(modos_tiempos=m_t_params)
        query_params = {f'{param_name}{i}': m_t for i, m_t in enumerate(moods_tenses)}

        current_app.logger.debug(f'{query_which_verb_fmt=}')
        current_app.logger.debug(f'{query_params=}')
        question = execute_query(query_which_verb_fmt, query_params=query_params)[0]
        verb: str = question.get('infinitivo')
        mood: str = question.get('modo')
        tense: str = question.get('tiempo')
        possible_pronouns_hr = list(pronoun_map_hr_db.keys())
        if mood == 'imperativo':
            possible_pronouns_hr.remove('yo')
        pronoun_hr: str = random.choice(possible_pronouns_hr)
        input_width = max(len(verb), 7) + 6
        input_width_attr = f'width: calc(var(--textsize)*{input_width} * 0.5)'
        quiz_subtitle = f'{mood.capitalize()}, {tense}'
        if request.method == 'POST':
            resp_data = {'hint': pronoun_hr, 'verb': verb, 'subtitle': quiz_subtitle}
            response = make_response(jsonify(resp_data), 200)
            return response

        template = render_template('quizpage-conjugacion.html', quiz_subtitle=quiz_subtitle, question_hint=pronoun_hr,
                                   question=verb, quiz_title='Conjugación', input_width=input_width_attr,
                                   moods=tenses_for_moods, nonce=nonce)
        response = add_security_headers(make_response(template, 200), nonce)
        return response
    except TypeError as e:
        current_app.logger.error(f'most likely one of the queries failed... {str(e)}')
        abort(500)


@bp.route(f'/{path}-submit', methods=['POST'])
def submit():
    data = request.get_json()
    answer: str = data['answer']
    question: str = data['question']
    if question == ':(':
        return make_response(':(', 200)
    pronoun_hr: str = data['questionHint']
    subtitle: str = data['subtitle']
    # TODO: put quiz info into hidden element and get it from those
    subtitle_list = [word.strip().lower() for word in subtitle.split(', ')]
    mood = subtitle_list[0]
    tense = subtitle_list[1]

    pronoun_db = pronoun_map_hr_db[pronoun_hr]

    identifier_params = {'pronoun': pronoun_db}
    query_params = {'verb': question, 'tense': tense, 'mood': mood}
    current_app.logger.debug(f'{query_pronoun_for_verb=}')
    current_app.logger.debug(f'{query_params=}')
    current_app.logger.debug(f'{identifier_params=}')
    solution: str = execute_query(query_pronoun_for_verb, query_params=query_params,
                                  identifier_params=identifier_params)[0].get(pronoun_db)

    if answer.strip().lower() == solution.strip().lower():
        response_text = '<span> <span class="correct">¡Correcto!</span></span>'
        correct = 1
    else:
        response_text = f'<span> <span class="false">¡Incorrecto! </span>La solución: {solution}</span>'
        correct = 0
    resp_data = {'message': response_text, 'correct': correct}
    response = make_response(jsonify(resp_data), 200)
    return response
