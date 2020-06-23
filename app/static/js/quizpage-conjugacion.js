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
        verbs = [];
    }

    if (correct) {
        for (let error of verbs) {
            if (error['verb'] === verb && error['mood'] === mood && error['tense'] === tense) {
                // edit html table accordingly
                error['points'] += incrementUnit;
                break;
            }
        }
    } else {
        let found = false;
        for (let error of verbs) {
            if (error['verb'] === verb && error['mood'] === mood && error['tense'] === tense) {
                // edit html table accordingly
                error['points'] -= 1;
                found = true;
            }
        }
        if (!found) {
            // edit html table accordingly
            verbs[verb] = {[mood]: {[tense]: -1}};
            verbs.push({'verb': verb, 'mood': mood, 'tense': tense, 'points': -1})
        }
    }
    // remove words that have 0 points
    verbs = verbs.filter(function (el) {
        return el['points'] !== 0;
    });
    // write back into localStorage
    localStorage.setItem('verbos', JSON.stringify(verbs))
    // redraw html table
    destroyErrorTable();
    constructErrorTable()
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

function destroyErrorTable() {
    let errorTable = document.getElementById('errorTable');
    while (errorTable.firstChild) {
        errorTable.removeChild(errorTable.firstChild)
    }
}

function constructErrorTable() {
    let errors = JSON.parse(localStorage.getItem('verbos')) || []
    constructTable(errors, '#errorTable')
}

// from https://www.geeksforgeeks.org/how-to-convert-json-data-to-a-html-table-using-javascript-jquery/
// with some changes
function constructTable(list, selector) {
    // Getting all column names
    const cols = tableHeaders(list, selector);
    // Traversing the JSON data
    for (let i = 0; i < list.length; i++) {
        const row = $('<tr/>');
        for (let colIndex = 0; colIndex < cols.length; colIndex++) {
            let val = list[i][cols[colIndex]];
            // If there is any key, which is matching
            // with the column name
            if (val == null) val = "";
            row.append($('<td/>').html(val));
        }
        // Adding each row to the table
        $(selector).append(row);
    }
}
// this is from https://www.geeksforgeeks.org/how-to-convert-json-data-to-a-html-table-using-javascript-jquery/
// with some changes
function tableHeaders(list, selector) {
    const columns = [];
    const header = $('<tr/>');
    for (let i = 0; i < list.length; i++) {
        const row = list[i];
        for (const k in row) {
            if ($.inArray(k, columns) === -1) {
                columns.push(k);
                // Creating the header
                header.append($('<th/>').html(k));
            }
        }
    }
    // Appending the header to the table
    $(selector).append(header);
    return columns;
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
    constructErrorTable()
}, false);
