let errorText = document.getElementById('message-text');
let exerciseElements = document.getElementsByClassName('form__field');
let answer = document.getElementById('answer');

ids = [];
answers = [];
for (let exerciseEl of exerciseElements) {
    ids.push(exerciseEl.getAttribute('data-identity'));
    answers.push(exerciseEl.value);
}

function submitError() {
    // TODO: handle other types of quiz pages as well
    let requestBody =
        'exercise=' + ids.join(', ') +
        '&answer=' + answers.join(', ') +
        '&message=' + errorText.value;
    sendRequest('POST', '/error', requestBody);
    errorText.value = '';

    $('#errorModal').modal('toggle');
}

$(document).ready(function () {
    $("#submitError").on("click", function () {
        submitError()
    });
});
