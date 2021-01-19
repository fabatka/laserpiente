function handleSubmitClickEvent(event) {
    const answerElement = document.getElementById('answer');
    const questionElement = document.getElementById('question');
    const serverResponseParagraph = document.getElementById('result');

    if (serverResponseParagraph.textContent === '') {
        let requestBody = 'answer=' + answerElement.value +
            '&question=' + questionElement.textContent;
        sendRequest('POST', window.location.pathname + '-submit', requestBody, 'application/x-www-form-urlencoded');
    } else {
        newQuestion()
    }
}

document.getElementById('messageClose').onclick = function () {
    document.getElementById('message').parentElement.classList.add('hidden')
}

function getRandomInt(max) {
    return Math.floor(Math.random() * Math.floor(max));
}

function newQuestion() {
    generateNum()
    $('#answer').prop('value', '')
    $('#submit').text('Comprobar'); // reset button text
    $('#result').text(''); // reset prev result
}

function generateNum() {
    let numFrom = parseInt(getCookie('numFrom'));
    let numTo = parseInt(getCookie('numTo'));
    const randomNum = getRandomInt(numTo - numFrom) + numFrom;
    $('#question').text(randomNum)
}

$(document).ready(function () {
    // set up triggers for radio buttons
    $('[name="numFrom"]').change(function () {
        setCookie('numFrom', $(this).attr('num'));
        generateNum()
    })
    $('[name="numTo"]').change(function () {
        setCookie('numTo', $(this).attr('num'));
        generateNum()
    })
    // if cookies don't exist, set default radio buttons and trigger creates them
    // otherwise just check radio buttons according to cookies
    if (getCookie('numFrom') === null || getCookie('numTo') === null) {
        // set default cookies and radio buttons
        $('[name="numFrom"][num="0"]').prop('checked', true);
        $('[name="numFrom"][num="0"]').trigger('change');
        $('[name="numTo"][num="100000"]').prop('checked', true);
        $('[name="numTo"][num="100000"]').trigger('change');
    } else {
        $(`[name="numFrom"][num=${getCookie('numFrom')}]`).prop('checked', true);
        $(`[name="numTo"][num=${getCookie('numTo')}]`).prop('checked', true);
    }
    // generate numbers based on cookies
    generateNum();
});

// to not collapse dropdown when clicked inside
$(document).on('click', '#settingsDropdown.dropdown-menu', function (e) {
    e.stopPropagation();
});
