let inputEls = $('[name="answer_input"]');

function getKeyboardEventCode(event) {
    let code;

    if (event.key !== undefined) {
        code = event.key;
    } else if (event.keyIdentifier !== undefined) {
        code = event.keyIdentifier;
    } else if (event.keyCode !== undefined) {
        code = event.keyCode;
    }
    return code;
}

for (let inputEl of inputEls) {
    inputEl.addEventListener("keyup", function (event) {
        let code = getKeyboardEventCode(event);

        if ((code === 13) || (code === 'Enter')) {
            event.preventDefault();
            document.getElementById('submit').click()
        }
    });
}
