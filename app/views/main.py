from flask import Blueprint, render_template, make_response, request

from app.static.utils import execute_query
from lang import pronoun_map_db_hr, pronoun_map_hr_db

bp = Blueprint('main', __name__, template_folder='templates')


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


@bp.route('/')
@bp.route('/home')
def home():
    pronoun_db: str = execute_query(query_which_pronoun)[0].get('column_name')
    verb: str = execute_query(query_which_verb)[0].get('infinitivo')
    pronoun_hr: str = pronoun_map_db_hr[pronoun_db]
    return render_template('home.html', pronoun=pronoun_hr, verb=verb)


@bp.route('/submit', methods=['POST'])
def submit():
    answer: str = request.form.get('answer')
    question: str = request.form.get('question')
    pronoun_hr: str = request.form.get('pronoun')
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
