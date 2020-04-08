function sendRequest(method, url, requestBody) {
    xhr.open(method, url);
    xhr.setRequestHeader('Content-type', 'application/x-www-form-urlencoded');
    xhr.send(requestBody);
}


// handle response
const xhr = new XMLHttpRequest();
xhr.onload = function () {
    const serverResponseParagraph = document.getElementById('result');
    serverResponseParagraph.innerHTML = this.responseText;
    const button = document.getElementById('submit')
    button.innerText = 'Következő'
};


// clicking on submit button sends answer to server
// only execute this after complete page load, because handleClickEvent is defined in separate files
window.onload = function () {
    const submitButton = document.getElementById('submit');
    submitButton.addEventListener('click', handleClickEvent);
};

// TODO: create a common 'handleClickEvent' function that gets a list/map as a parameter
