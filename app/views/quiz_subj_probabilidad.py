from typing import List
from flask import Blueprint, render_template, make_response, request

from app.static.utils import execute_query
from app.lang import pronoun_map_db_hr, pronoun_map_hr_db

bp = Blueprint('quiz-subjuntivo-probabilidad', __name__, template_folder='templates')

path = 'quiz-subjuntivo-probabilidad'

query_question = '''
select frase, palabra_q_falta, solucion_infinitivo, solucion_sujeto
from laserpiente.sentences
where 1=1
    and quiz = 'subjuntivo-probabilidad'
order by random()
limit 1'''

query_solution = '''
select frase
from laserpiente.sentences
where 1=1
    and quiz = 'subjuntivo-probabilidad'
    and frase like %(sentence_first)s || '%%' 
    and frase like '%%' || %(sentence_second)s 
    and palabra_q_falta = %(missing_word_pos)s
    and solucion_sujeto = %(solution_subject)s '''


@bp.route(f'/{path}', methods=['GET'])
def quiz():
    question_row = execute_query(query_question)[0]
    sentence_split: List[str, int] = question_row['frase'].split()
    missing_word_pos: int = question_row['palabra_q_falta']
    solution_infinitive = question_row['solucion_infinitivo']
    solution_subject = question_row['solucion_sujeto']
    sentence_first = ' '.join(sentence_split[:missing_word_pos-1]) + ' '
    sentence_second = ' ' + ' '.join(sentence_split[missing_word_pos:])
    hint = f'{solution_infinitive} ({pronoun_map_db_hr[solution_subject]})'
    input_width = max(len(sentence_split[missing_word_pos - 1]), len(pronoun_map_db_hr[solution_subject]))
    input_width_attr = f'width: calc(var(--textsize)*{input_width}*0.7)'

    return render_template('subjuntivo-probabilidad.html', question_first=sentence_first, question_second=sentence_second,
                           question_hint=hint, quiz_title='Subjuntivo, probabilidad', input_width=input_width_attr)


@bp.route(f'/{path}-submit', methods=['POST'])
def submit():
    answer: str = request.form.get('answer')
    question_first: str = request.form.get('questionFirst').strip()
    question_second: str = request.form.get('questionSecond').strip()
    hint: str = request.form.get('questionHint')
    infinitivo, solution_subject_hr = hint.split(' ')  # the hint is like "infinitivo (pronoun)"
    solution_subject_db = pronoun_map_hr_db[solution_subject_hr[1:-1]]  # there are parentheses around the pronouns

    query_params = {
        'sentence_first': question_first,
        'sentence_second': question_second,
        'missing_word_pos': len(question_first.split(' ')) + 1,
        'solution_subject': solution_subject_db
    }
    solution_sentence = execute_query(query_solution, query_params=query_params)[0].get('frase')
    solution = solution_sentence.split(' ')[len(question_first.split(' '))]

    if answer.strip().lower() == solution.strip().lower():
        response_text = '<p> <span class="correct">¡Correcto!</span></p>'
    else:
        response_text = f'<p> <span class="false">¡Incorrecto! </span>La solución: {solution}</p>'
    return make_response(response_text, 200)
