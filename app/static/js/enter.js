let input = document.getElementById('answer');

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

input.addEventListener("keyup", function (event) {
    let code = getKeyboardEventCode(event);

    if ((code === 13) || (code === 'Enter')) {
        event.preventDefault();
        document.getElementById('submit').click()
    }
});
