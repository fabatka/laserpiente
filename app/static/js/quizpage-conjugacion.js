const pronouns = [
    'yo',
    'tú',
    'él/ella/Ud.',
    'nosotros',
    'vosotros',
    'ellos/ellas/Uds.'
]

function handleSubmitClickEvent(event) {
    const answerElement = document.getElementById('answer');
    const questionElement = document.getElementById('question');
    const questionHintElement = document.getElementById('questionHint') || document.getElementById('question');
    const subtitleElement = document.getElementById('quizbox-subtitle');
    const serverResponseParagraph = document.getElementById('result');

    let noResponse = serverResponseParagraph.textContent === '';
    if (noResponse) {
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
        let errors = JSON.parse(localStorage.getItem('verbos'));
        let numOfErrors = Math.abs(sumErrorPoints(errors))
        let prob = numOfErrors > 10 ? 0.99 : Math.tanh(numOfErrors ** (3 / 2) * 0.0475);

        if (Math.random() > prob) {
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
        } else {
            console.log('TRY AGAIN, DUMMY')
            let error = errors[Math.floor(Math.random() * errors.length)];
            let hint = pronouns[Math.floor(Math.random() * pronouns.length)];
            let subtitle = `${error['mood'].charAt(0).toUpperCase() + error['mood'].slice(1)}, ${error['tense']}`
            newQuestion(subtitle, hint, error['verb'])
        }
    }
}

function sumErrorPoints(errors) {
    let sum = 0;
    for (let error of errors) {
        sum += error['points'];
    }
    return sum
}


const incrementUnit = 0.5;

function changeVerbPoints(verb, mood, tense, correct) {
    let verbs = JSON.parse(localStorage.getItem('verbos'));
    if (verbs === null || verbs === undefined) {
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
    constructTable(errors.sort(compareErrors), '#errorTable')
}

function compareErrors(e1, e2) {
    if (e1['points'] > e2['points']) return 1;
    if (e1['points'] < e2['points']) return -1;
    if (e1['verb'] > e2['verb']) return 1;
    if (e1['verb'] < e2['verb']) return -1;
    return 0;
}

function points2colorClass(point) {
    if (point <= -4) return 'error3'
    if (point <= -2) return 'error2'
    return 'error1'
}

// from https://www.geeksforgeeks.org/how-to-convert-json-data-to-a-html-table-using-javascript-jquery/
// with some changes
function constructTable(list, selector) {
    // don't even create basic structure if list is empty
    if (list.length === 0) return
    // Getting all column names
    const cols = tableHeaders(list, selector);
    $(selector).append($('<tbody>'))
    // Traversing the JSON data
    for (let i = 0; i < list.length; i++) {
        const row = $('<tr/>').addClass(points2colorClass(list[i]['points']));
        for (let colIndex = 0; colIndex < cols.length; colIndex++) {
            let val = list[i][cols[colIndex]];
            // If there is any key, which is matching
            // with the column name
            if (val == null) val = "";
            row.append($('<td/>').html(val));
        }
        // Adding each row to the table
        $(selector + ' tbody').append(row);
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
    $(selector).append($('<thead>').append(header));
    return columns;
}

// flip card on flip button click
$('#flipButton').click(function () {
    $('.card-flip').toggleClass('flipped')
});
$('#flipBackButton').click(function () {
    $('.card-flip').toggleClass('flipped')
});

// reset errors on button click
$('#reset').click(function () {
    localStorage.removeItem('verbos')
    destroyErrorTable()
})

document.addEventListener('DOMContentLoaded', function () {
    checkboxTreeview()
    checkChkboxCookies();
    constructErrorTable()
}, false);
