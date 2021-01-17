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
            url: window.location.pathname + '-submit',
            data: JSON.stringify({
                'answers': answers,
                'questionIds': questionIds
            }),
            contentType: 'application/json; charset=utf-8',
            dataType: 'json'
        }).done(function (resultMessage, status) {
            serverResponseParagraph.innerHTML = resultMessage;
        }).fail(function (xhr, status, error) {
            serverResponseParagraph.innerHTML += xhr.responseText;
        })
    } else {
        $.ajax({
            type: 'POST',
            url: window.location.pathname,
            data: JSON.stringify({}),
            contentType: 'application/json; charset=utf-8',
            dataType: 'json'
        }).done(function (response) {
            const {texts, hints, ids, widths} = response;
            newQuestion(texts, hints, ids, widths);
        }).fail(function (xhr, status, error) {
            // TODO
        })
    }
}

questionTemplate = (id, text) => `<div id="question${id}" class="question">${text}</div>`;
inputTemplate = (width, id, identifier, text) => `
    <div class="form__group">
    <input type="text" class="form__field" placeholder="dummy placeholder" 
           name="answer_input" id="answer${id}" style="${width}" 
           data-identity="${identifier}">
    <label id="questionHint${id}" for="answer${id}" class="form__label">${text}</label>
    </div>
`;

function newQuestion(texts, hints, ids, inputWidths) {
    for (let index = 0, id = 1; index < texts.length; index++, id++) {
        if ($(`#question${id}`).length === 0) {
            // no need to fill in details, we'll do it anyway
            $(`#answer${id-1}`).parent().after(questionTemplate(id, ''))
        }
        const $currQuestionEl = $(`#question${id}`);

        if ($(`#questionHint${id}`).length === 0 && id !== texts.length) {
            // no need to fill in details, we'll do it anyway
            $currQuestionEl.after(inputTemplate('', id, '', ''))
            submitOnEnter($(`#answer${id}`).get(0))
        }
        const $currHintEl = $(`#questionHint${id}`);
        const $currAnsEl = $(`#answer${id}`);
        $currQuestionEl.text(texts[index])
        $currHintEl.text(hints[index])
        $currAnsEl.attr('style', inputWidths[index]); // set new input size('value')
        $currAnsEl.prop('value', '');
        $currAnsEl.attr('data-identity', ids[index]);
    }

    let lastId = texts.length + 1
    while ($(`#question${lastId}`).length > 0) {
        $(`#question${lastId}`).remove()
        $(`#answer${lastId-1}`).remove()
        $(`#questionHint${lastId-1}`).remove()
        ++lastId
    }

    $('#result').text(''); // reset prev result
    $('#submit').text('Comprobar'); // reset button text
    $(`#answer1`).focus(); // focus on first input field
}
