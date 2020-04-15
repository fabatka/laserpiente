let errorText = document.getElementById('message-text');
let exercise = document.getElementById('quizbox-task');
let answer = document.getElementById('answer');

function submitError() {
    let requestBody =
        'exercise=' + exercise.innerText +
        '&answer=' + answer.value +
        '&message=' + errorText.value;
    sendRequest('POST', '/error', requestBody);
    errorText.value = '';

    $('#errorModal').modal('toggle');
}
