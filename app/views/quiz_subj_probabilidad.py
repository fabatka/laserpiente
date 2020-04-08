from typing import List
from flask import Blueprint, render_template, make_response, request

from app.static.utils import execute_query
from app.lang import pronoun_map_db_hr

bp = Blueprint('quiz-subjuntivo-probabilidad', __name__, template_folder='templates')


query_question = '''
select frase, palabra_q_falta, solucion_infinitivo, solucion_sujeto
from laserpiente.sentences
where 1=1
    and quiz = 'subjuntivo-probabilidad'
order by random()
limit 1'''


@bp.route('/quiz-subj-probabilidad', methods=['GET'])
def quiz():
    question_row = execute_query(query_question)[0]
    sentence_split: List[str, int] = question_row['frase'].split()
    missing_word_pos: int = question_row['palabra_q_falta']
    solution_infinitive = question_row['solucion_infinitivo']
    solution_subject = question_row['solucion_sujeto']
    sentence_first = ' '.join(sentence_split[:missing_word_pos - 1])
    sentence_second = ' '.join(sentence_split[missing_word_pos:])
    hint = f'{solution_infinitive} ({pronoun_map_db_hr[solution_subject]})'

    return render_template('quizpage-mono.html', question_first=sentence_first, question_second=sentence_second,
                           question_hint=hint)


# TODO: implement answer checking
