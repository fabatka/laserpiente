let input = document.getElementById('answer');

input.addEventListener("keyup", function (event) {
    let code;

    if (event.key !== undefined) {
        code = event.key;
    } else if (event.keyIdentifier !== undefined) {
        code = event.keyIdentifier;
    } else if (event.keyCode !== undefined) {
        code = event.keyCode;
    }

    if ((code === 13) || (code === 'Enter')) {
        event.preventDefault();
        document.getElementById('submit').click()
    }
});
