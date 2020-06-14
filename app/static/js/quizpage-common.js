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
    button.innerText = 'Siguiente'
};


// clicking on submit button sends answer to server
// only execute this after complete page load, because handleClickEvent is defined in separate files
window.onload = function () {
    const submitButton = document.getElementById('submit');
    submitButton.addEventListener('click', handleSubmitClickEvent);
};

// TODO: create a common 'handleClickEvent' function that gets a list/map as a parameter

const $tooltipEls = $('[data-toggle="tooltip"]');
$('#infobutton').hover(function (e) {
    $tooltipEls.tooltip('enable');
    $tooltipEls.tooltip('toggle');
    $(this).attr('src', '/static/img/info-color1-color3.svg');
}, function () {
    $tooltipEls.tooltip('toggle');
    $(this).attr('src', '/static/img/info-color1-color4.svg');
    $tooltipEls.tooltip('disable');
});

// from https://www.w3schools.com/js/js_cookies.asp, with minimal modifications
function getCookie(cname) {
    const name = cname + "=";
    const decodedCookie = decodeURIComponent(document.cookie);
    const ca = decodedCookie.split(';');
    for (let i = 0; i < ca.length; i++) {
        let c = ca[i];
        while (c.charAt(0) == ' ') {
            c = c.substring(1);
        }
        if (c.indexOf(name) == 0) {
            return c.substring(name.length, c.length);
        }
    }
    return null;
}

// from https://www.w3schools.com/js/js_cookies.asp, with minimal modifications
function setCookie(cname, cvalue, exdays) {
    const d = new Date();
    d.setTime(d.getTime() + (exdays * 24 * 60 * 60 * 1000));
    const expires = "expires=" + d.toUTCString();
    document.cookie = cname + "=" + cvalue + ";" + expires + "; SameSite=Strict" + ";path=/";
}
