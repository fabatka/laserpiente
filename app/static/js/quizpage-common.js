function sendRequest(method, url, requestBody, contentType = 'application/x-www-form-urlencoded') {
    xhr.open(method, url);
    xhr.setRequestHeader('Content-type', contentType);
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
    submitButton.addEventListener('click', handleSubmitClickEvent);
};

// TODO: create a common 'handleClickEvent' function that gets a list/map as a parameter

$('#infobutton').hover(function (e) {
    $('[data-toggle="tooltip"]').tooltip('enable');
    $('[data-toggle="tooltip"]').tooltip('toggle');
    $(this).attr('src', '/static/img/info-color1-color3.svg');
}, function () {
    $('[data-toggle="tooltip"]').tooltip('toggle');
    $(this).attr('src', '/static/img/info-color1-color4.svg');
    $('[data-toggle="tooltip"]').tooltip('disable');
});
