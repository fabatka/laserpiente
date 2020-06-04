from typing import List, Optional

from flask import Blueprint, render_template, make_response, request, abort
from markupsafe import escape

from app.lang import pronoun_map_db_hr, pronoun_map_hr_db
from app.static.utils import execute_query

bp = Blueprint('quiz-subjuntivo', __name__, template_folder='templates')

query_question = '''
select f.texto, 
       array_agg(e.palabra_q_falta order by e.palabra_q_falta) as palabra_q_falta,
       array_agg(e.solucion_infinitivo order by e.palabra_q_falta) as solucion_infinitivo,
       array_agg(e.solucion_sujeto order by e.palabra_q_falta) as solucion_sujeto
from laserpiente.ejercicio e
join laserpiente.frase f
    on e.frase_id = f.id
where 1=1
    and e.quiz = %(quiz)s
group by f.texto 
order by random()
limit 1
'''

query_solution = '''
select frase
from laserpiente.sentences
where 1=1
    and quiz = %(quiz)s
    and frase like %(sentence_first)s || '%%' 
    and frase like '%%' || %(sentence_second)s 
    and palabra_q_falta = %(missing_word_pos)s
    and solucion_sujeto = %(solution_subject)s 
'''

query_subjuntivo_quizzes = '''
select distinct quiz
from laserpiente.ejercicio
where quiz like 'subjuntivo%'
'''


@bp.route(f'/quiz-subjuntivo-<quiz_type>', methods=['GET'])
def quiz_page(quiz_type: str):
    """
    Displays a mono quiz page with a question that has the quiz type found in the url.

    :param quiz_type: The url defines what kind of quiz to display. This must be one of the quiz values found in the sentences table
    :type quiz_type: str
    """
    quiz = 'subjuntivo-' + escape(quiz_type)
    page = f'{quiz}.html'
    title = quiz.replace('-', ' - ').replace('_', ' ').capitalize()

    if quiz not in distinct_subjuntivo_quizzes():
        abort(404)

    # we query the whole sentence, and lists of positions of the words to be omitted, their inifnite forms and subjects
    question_row = execute_query(raw_query=query_question, query_params={'quiz': quiz})[0]
    sentence_splits: List[str] = question_row['texto'].split()
    missing_positions: List[Optional[int]] = question_row['palabra_q_falta']
    solutions_infinitive: List[str] = question_row['solucion_infinitivo']
    solutions_subject: List[str] = question_row['solucion_sujeto']
    # we create a list of the sentence parts between the solutions (and omit them)
    # the template will iterate over these
    text_limits = [None] + missing_positions + [None]

    def ending(x: Optional[int]): return None if x is None else x - 1

    sentence_parts = [' '.join(sentence_splits[beg:ending(end)]) + ' '
                      for beg, end in zip(text_limits, text_limits[1:])]
    hints = [f'{inf} ({pronoun_map_db_hr[subj]})'
             for inf, subj in zip(solutions_infinitive, solutions_subject)]
    input_widths = [max(len(sentence_splits[missing_pos - 1]), len(hints[idx]))
                    for idx, missing_pos in enumerate(missing_positions)]
    input_width_attrs = [f'width: calc(var(--textsize)*{input_width}*0.45)'
                         for input_width in input_widths]

    return render_template(page,
                           questions=sentence_parts,
                           input_widths=input_width_attrs,
                           question_hints=hints)


def distinct_subjuntivo_quizzes() -> List[str]:
    return [row['quiz'] for row in execute_query(query_subjuntivo_quizzes)]


@bp.route(f'/quiz-subjuntivo-<quiz_type>-submit', methods=['POST'])
def submit(quiz_type: str):
    quiz = 'subjuntivo-' + escape(quiz_type)
    answer: str = request.form.get('answer')
    question_first: str = request.form.get('questionFirst').strip()
    question_second: str = request.form.get('questionSecond').strip()
    hint: str = request.form.get('questionHint')
    infinitivo, solution_subject_hr = hint.split(' ')  # the hint is like "infinitivo (pronoun)"
    solution_subject_db = pronoun_map_hr_db[solution_subject_hr[1:-1]]  # there are parentheses around the pronouns

    missing_word_pos = len(question_first.split(' ')) if len(question_first) > 0 else 0

    query_params = {
        'quiz': quiz,
        'sentence_first': question_first,
        'sentence_second': question_second,
        'missing_word_pos': missing_word_pos + 1,
        'solution_subject': solution_subject_db
    }
    solution_sentence = execute_query(query_solution, query_params=query_params)[0].get('frase')
    solution = solution_sentence.split(' ')[missing_word_pos]

    if answer.strip().lower() == solution.strip().lower():
        response_text = '<p> <span class="correct">¡Correcto!</span></p>'
    else:
        response_text = f'<p> <span class="false">¡Incorrecto! </span>La solución: {solution}</p>'
    return make_response(response_text, 200)
