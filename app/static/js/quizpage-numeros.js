function handleSubmitClickEvent(event) {
    const answerElement = document.getElementById('answer');
    const questionElement = document.getElementById('question');
    const serverResponseParagraph = document.getElementById('result');

    if (serverResponseParagraph.textContent === '') {
        let requestBody = 'answer=' + answerElement.value +
            '&question=' + questionElement.textContent;
        sendRequest('POST', window.location.pathname + '-submit', requestBody, 'application/x-www-form-urlencoded');
    } else {
        window.location.href = window.location.pathname
    }
}
