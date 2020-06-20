function handleSubmitClickEvent(event) {
    const answerElement = document.getElementById('answer');
    const questionElement = document.getElementById('question');
    const questionHintElement = document.getElementById('questionHint') || document.getElementById('question');
    const subtitleElement = document.getElementById('quizbox-subtitle');
    const serverResponseParagraph = document.getElementById('result');

    if (serverResponseParagraph.textContent === '') {
        let requestBody = 'answer=' + answerElement.value +
            '&question=' + questionElement.textContent +
            '&questionHint=' + questionHintElement.textContent +
            '&subtitle=' + subtitleElement.textContent;
        sendRequest('POST', window.location.pathname + '-submit', requestBody, 'application/x-www-form-urlencoded');
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
}, false);
