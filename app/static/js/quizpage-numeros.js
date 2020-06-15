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

function getRandomInt(max) {
  return Math.floor(Math.random() * Math.floor(max));
}

function newQuestion() {
    $('#question').text(getRandomInt(1e4))
    $('#answer').prop('value', '')
    $('#submit').text('Comprobar'); // reset button text
    $('#result').text(''); // reset prev result
}

// generate random number when page loads
$(document).ready(function(){
    $('#question').text(getRandomInt(1e4))
});

// to not collapse dropdown when clicked inside
$(document).on('click', '#settingsDropdown.dropdown-menu', function (e) {
    e.stopPropagation();
});
