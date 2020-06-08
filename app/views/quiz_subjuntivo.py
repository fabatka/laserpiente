import re
from typing import List, Optional, Tuple

import psycopg2 as pg
from flask import Blueprint, render_template, make_response, request, abort, jsonify
from markupsafe import escape

from app.lang import pronoun_map_db_hr
from app.static.utils import execute_query

punctuations = '-–.,:?'

bp = Blueprint('quiz-subjuntivo', __name__, template_folder='templates')

query_question = '''
select f.texto,
       array_agg(e.id order by e.palabra_q_falta) as id,
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
select e.palabra_q_falta,
       f.texto
from laserpiente.ejercicio e
join laserpiente.frase f
    on e.frase_id = f.id
where 1=1
    and e.id = %(id)s
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
    text: str = question_row['texto']
    missing_pos: List[Optional[int]] = question_row['palabra_q_falta']
    solutions_infinitive: List[str] = question_row['solucion_infinitivo']
    solutions_subject: List[str] = question_row['solucion_sujeto']
    ids: List[int] = question_row['id']

    # handle newlines
    text = text.replace('\r\n', ' \r\n ')
    for idx, word in enumerate(text.split(' ')):
        if re.search(r'\r\n', word):
            missing_pos = [pos+1 if pos > idx else pos for pos in missing_pos]

    # handle punctuations
    sentence_splits: List[str] = text.split(' ')
    sentence_splits_mod, missing_pos_mod = handle_punctuations(sentence_splits, missing_pos)

    # we create a list of the sentence parts between the solutions (and omit them)
    # the template will iterate over these and create html elements with the
    # appropriate attributes and content
    text_limits = [None] + missing_pos_mod + [None]
    def ending(x: Optional[int]): return None if x is None else x - 1
    sentence_parts = [' '.join(sentence_splits_mod[beg:ending(end)]) + ' '
                      for beg, end in zip(text_limits, text_limits[1:])]

    hints = [f'{inf} ({pronoun_map_db_hr[subj]})'
             for inf, subj in zip(solutions_infinitive, solutions_subject)]
    input_widths = [max(len(sentence_splits_mod[missing_pos_mod - 1]), len(hints[idx]))
                    for idx, missing_pos_mod in enumerate(missing_pos_mod)]
    input_width_attrs = [f'width: calc(var(--textsize)*{input_width}*0.45)'
                         for input_width in input_widths]

    return render_template(page,
                           questions=sentence_parts,
                           input_widths=input_width_attrs,
                           question_hints=hints,
                           question_ids=ids,
                           quiz_title=title)


def handle_punctuations(sentence_splits: List[str], missing_pos: List[int]) -> Tuple[List[str], List[Optional[int]]]:
    missing_pos_mod = missing_pos.copy()
    sentence_splits_mod = []
    for word in sentence_splits:
        k = len(sentence_splits_mod)
        if word[0] in punctuations:
            sentence_splits_mod.extend([word[0], word[1:]])
            missing_pos_mod = [m + 1 if m >= k + 1 else m for m in missing_pos_mod]
        elif word[-1] in punctuations:
            sentence_splits_mod.extend([word[:-1], word[-1]])
            missing_pos_mod = [m + 1 if m > k + 1 else m for m in missing_pos_mod]
        else:
            sentence_splits_mod.append(word)
    return sentence_splits_mod, missing_pos_mod


def distinct_subjuntivo_quizzes() -> List[str]:
    return [row['quiz'] for row in execute_query(query_subjuntivo_quizzes)]


@bp.route(f'/quiz-subjuntivo-<_quiz_type>-submit', methods=['POST'])
def submit(_quiz_type: str):
    data = request.get_json()
    answers: List[str] = data['answers']
    question_ids: List[str] = data['questionIds']

    results = []
    solutions = []
    try:
        for question_id, answer in zip(question_ids, answers):
            solution_row = execute_query(query_solution, query_params={'id': question_id})[0]
            sentence: str = solution_row['texto']
            missing_place: int = solution_row['palabra_q_falta']
            solution = sentence.split()[missing_place-1]
            solution_clean = solution.strip().strip(punctuations).lower()
            answer_clean = answer.strip().strip(punctuations).lower()
            solutions.append(solution_clean)
            results.append(answer_clean == solution_clean)

        if all(results):
            response_text = '<p> <span class="correct">¡Correcto!</span></p>'
        else:
            response_text = f'<p> <span class="false">¡Incorrecto! </span>La solución: {", ".join(solutions)}</p>'
        return make_response(jsonify(response_text), 200)
    except pg.Error as e:
        return make_response(jsonify(e), 500)
