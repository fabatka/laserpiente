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
        window.location.href = window.location.pathname
    }
}

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

document.addEventListener('DOMContentLoaded', function () {
    checkboxTreeview()
    checkChkboxCookies();
}, false);