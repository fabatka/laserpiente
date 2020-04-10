from flask import Blueprint, render_template, make_response, request

from app.static.utils import execute_query
from app.lang import pronoun_map_db_hr, pronoun_map_hr_db

bp = Blueprint('quiz-indicativo-presente', __name__, template_folder='templates')

path = 'quiz-conj-dual-indicativo-presente'

query_which_pronoun = """
select column_name 
from information_schema.columns 
where 1=1
    and table_name = 'v_conj_ind_pres'
    and column_name <> 'infinitivo' 
order by random()
limit 1
"""

query_which_verb = '''
select infinitivo
from laserpiente.v_conj_ind_pres 
order by random() 
limit 1'''

query_pronoun_for_verb = '''
select {pronoun}
from laserpiente.v_conj_ind_pres
where infinitivo = %(verb)s'''


@bp.route('/', methods=['GET'])
@bp.route(f'/{path}', methods=['GET'])
def quiz():
    pronoun_db: str = execute_query(query_which_pronoun)[0].get('column_name')
    verb: str = execute_query(query_which_verb)[0].get('infinitivo')
    pronoun_hr: str = pronoun_map_db_hr[pronoun_db]
    input_width = max(len(pronoun_hr), len(verb))
    input_width_attr = f'width: calc(var(--textsize)*{input_width}*0.7)'
    return render_template('quizpage-dual.html', question_hint=pronoun_hr, question=verb,
                           quiz_title='Conjugación - Indicativo, presente', input_width=input_width_attr)


@bp.route(f'/{path}-submit', methods=['POST'])
def submit():
    answer: str = request.form.get('answer')
    question: str = request.form.get('question')
    pronoun_hr: str = request.form.get('questionHint')
    pronoun_db = pronoun_map_hr_db[pronoun_hr]

    identifier_params = {'pronoun': pronoun_db}
    query_params = {'verb': question}
    solution: str = execute_query(query_pronoun_for_verb,
                                  identifier_params=identifier_params,
                                  query_params=query_params)[0].get(pronoun_db)

    if answer.strip().lower() == solution.strip().lower():
        response_text = '<p> <span class="correct">¡Correcto!</span></p>'
    else:
        response_text = f'<p> <span class="false">¡Incorrecto! </span>La solución: {solution}</p>'
    return make_response(response_text, 200)
