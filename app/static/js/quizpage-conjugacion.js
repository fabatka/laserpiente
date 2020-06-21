function handleSubmitClickEvent(event) {
    const answerElement = document.getElementById('answer');
    const questionElement = document.getElementById('question');
    const questionHintElement = document.getElementById('questionHint') || document.getElementById('question');
    const subtitleElement = document.getElementById('quizbox-subtitle');
    const serverResponseParagraph = document.getElementById('result');

    if (serverResponseParagraph.textContent === '') {
        $.ajax({
            type: 'POST',
            url: window.location.pathname + '-submit',
            data: JSON.stringify({
                'answer': answerElement.value,
                'question': questionElement.textContent,
                'questionHint': questionHintElement.textContent,
                'subtitle': subtitleElement.textContent
            }),
            contentType: 'application/json; charset=utf-8',
            dataType: 'json'
        }).done(function (response) {
            const {message, correct} = response;
            const serverResponseParagraph = document.getElementById('result');
            serverResponseParagraph.innerHTML = message;
            const button = document.getElementById('submit')
            button.innerText = 'Siguiente'
            // tracking errors
            let moodTense = subtitleElement.textContent.toLowerCase().split(', ')
            let mood = moodTense[0]
            let tense = moodTense[1]
            changeVerbPoints(questionElement.textContent, mood, tense, correct)
        }).fail(function (xhr, status, error) {
            // TODO
        })
    } else {
        $.ajax({
            type: 'POST',
            url: window.location.pathname,
            data: JSON.stringify({}),
            contentType: 'application/json; charset=utf-8',
            dataType: 'json'
        }).done(function (response) {
            const {hint, verb, subtitle} = response;
            newQuestion(subtitle, hint, verb);
        }).fail(function (xhr, status, error) {
            // TODO
        })
    }
}

const incrementUnit = 0.5;

function changeVerbPoints(verb, mood, tense, correct) {
    let verbs = JSON.parse(localStorage.getItem('verbos'));
    if (verbs === null) {
        verbs = {}
    }
    if (correct) {
        if (verbs[verb] && verbs[verb][mood] && verbs[verb][mood][tense]) {
            // edit html table accordingly
            verbs[verb][mood][tense] += incrementUnit;
            if (verbs[verb][mood][tense] === 0) {
                // edit html table accordingly
                // we only delete the topmost layer
                delete verbs[verb][mood][tense];
            }
        }
    } else {
        if (verbs[verb] && verbs[verb][mood] && verbs[verb][mood][tense]) {
            // edit html table accordingly
            verbs[verb][mood][tense] -= 1;
        } else {
            // edit html table accordingly
            verbs[verb] = {[mood]: {[tense]: -1}};
        }
    }
    localStorage.setItem('verbos', JSON.stringify(verbs))
    // check if localStorage and html table are in sync
    // if not, redraw html table from localStorage
}

function newQuestion(subtitle, hint, verb) {
    $('#quizbox-subtitle').text(subtitle); // set subtitle
    $('#questionHint').text(hint); // set hint
    $('#question').text(verb); // set question
    $('#result').text(''); // reset prev result
    let inputWidth = Math.max(verb.length, 7) + 6
    const answerEl = $('#answer');
    answerEl.attr('style', `width: calc(var(--textsize)*${inputWidth}*0.5`); // set new input size
    answerEl.prop('value', ''); // reset prev input
    $('#submit').text('Comprobar'); // reset button text
    answerEl.focus(); // focus on input field
}

// to not collapse dropdown when clicked inside
$(document).on('click', '#settingsDropdown.dropdown-menu', function (e) {
    e.stopPropagation();
});

// uncheck checkboxes that are found among cookies
function checkChkboxCookies() {
    let inputEls = $('.treeview input[type="checkbox"]')
    for (let inputEl of inputEls) {
        if (inputEl.parentElement.children.length === 2) {
            if (getCookie(inputEl.name) !== null) {
                const $inputEl = $(`[name=${inputEl.name}]`);
                $inputEl.prop('checked', false);
                $inputEl.trigger('change');
            }
        }
    }
}

// flip card on flip button click
$('#flipButton').click(function () {
    $('.card-flip').toggleClass('flipped')
});
$('#flipBackButton').click(function () {
    $('.card-flip').toggleClass('flipped')
});

document.addEventListener('DOMContentLoaded', function () {
    checkboxTreeview()
    checkChkboxCookies();
    // draw error html table based on localStorage
}, false);
