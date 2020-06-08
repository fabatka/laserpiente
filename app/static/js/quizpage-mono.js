function handleSubmitClickEvent(event) {
    const inputElements = document.getElementsByClassName('form__field');
    const serverResponseParagraph = document.getElementById('result');

    let answers = [];
    let questionIds = [];
    for (let inputEl of inputElements) {
        answers.push(inputEl.value)
        questionIds.push(inputEl.getAttribute('data-identity'))
    }

    if (serverResponseParagraph.textContent === '') {
        $.ajax({
            type: 'POST',
            url:  window.location.pathname + '-submit',
            data: JSON.stringify({
                'answers': answers,
                'questionIds': questionIds}),
            contentType: 'application/json; charset=utf-8',
            dataType: 'json'
        }).done(function (resultMessage, status) {
            serverResponseParagraph.innerHTML = resultMessage;
        }).fail(function (xhr, status, error) {
            serverResponseParagraph.innerHTML += xhr.responseText;
        })
    } else {
        window.location.href = window.location.pathname
    }
}
