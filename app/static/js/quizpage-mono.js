function handleClickEvent(event) {
    const answerElement = document.getElementById('answer');
    const questionFirstElement = document.getElementById('questionFirst');
    const questionSecondElement = document.getElementById('questionSecond');
    const questionHintElement = document.getElementById('questionHint');
    const serverResponseParagraph = document.getElementById('result');

    if (serverResponseParagraph.textContent === '') {
        let requestBody = 'answer=' + answerElement.value +
            '&questionFirst=' + questionFirstElement.textContent +
            '&questionSecond=' + questionSecondElement.textContent +
            '&questionHint=' + questionHintElement.textContent;
        sendRequest('POST', window.location.pathname + '-submit', requestBody);
    } else {
        window.location.href = window.location.pathname
    }
}