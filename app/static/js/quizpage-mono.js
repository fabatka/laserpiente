function handleClickEvent(event) {
    const answerElement = document.getElementById('answer');
    const questionElement = document.getElementById('question');
    const questionHintElement = document.getElementById('questionHint');
    const serverResponseParagraph = document.getElementById('result');

    if (serverResponseParagraph.textContent === '') {
        let requestBody = 'answer=' + answerElement.value +
            '&question=' + questionElement.textContent +
            '&questionHint=' + questionHintElement.textContent;
        sendRequest('POST', window.location.pathname + '-submit', requestBody);
    } else {
        window.location.href = window.location.pathname
    }
}