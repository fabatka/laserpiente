const submitButton = document.getElementById('submit');



// clicking on submit sends
submitButton.addEventListener('click', function (event) {
    const answerElement = document.getElementById('answer');
    const questionElement = document.getElementById('question');
    const pronounElement = document.getElementById('pronoun');

    // this will send a request
    xhr.open('POST', '/submit');
    xhr.setRequestHeader('Content-type', 'application/x-www-form-urlencoded');
    xhr.send('answer=' + answerElement.value +
        '&question=' + questionElement.textContent +
        '&pronoun=' + pronounElement.textContent);
});




const xhr = new XMLHttpRequest();

// this will run when we get a response
xhr.onload = function () {
    const serverResponseParagraph = document.getElementById('serverResponse');
    serverResponseParagraph.innerHTML = this.responseText;
};

