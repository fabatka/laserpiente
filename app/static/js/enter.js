let input = document.getElementById('answer');

input.addEventListener("keyup", function (event) {
    let code;
    console.log('ELKAPTA')

    if (event.key !== undefined) {
        code = event.key;
    } else if (event.keyIdentifier !== undefined) {
        code = event.keyIdentifier;
    } else if (event.keyCode !== undefined) {
        code = event.keyCode;
    }
    console.log('code:', code)

    if ((code === 13) || (code === 'Enter')) {
        event.preventDefault();
        document.getElementById('submit').click()
    }
});
