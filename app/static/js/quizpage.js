function sendRequest(method, url, requestBody) {
    xhr.open(method, url);
    xhr.setRequestHeader('Content-type', 'application/x-www-form-urlencoded');
    xhr.send(requestBody);
}


function handleClickEvent(event) {
    const answerElement = document.getElementById('answer');
    const questionElement = document.getElementById('question');
    const pronounElement = document.getElementById('pronoun');
    const serverResponseParagraph = document.getElementById('result');

    if (serverResponseParagraph.textContent === '') {
        let requestBody = 'answer=' + answerElement.value +
            '&question=' + questionElement.textContent +
            '&pronoun=' + pronounElement.textContent;
        sendRequest('POST', '/submit', requestBody);
    } else {
        window.location.href = '/quiz'
    }
}


// handle response
const xhr = new XMLHttpRequest();
xhr.onload = function () {
    const serverResponseParagraph = document.getElementById('result');
    serverResponseParagraph.innerHTML = this.responseText;
};


// clicking on submit button sends answer to server
const submitButton = document.getElementById('submit');
submitButton.addEventListener('click', handleClickEvent);
