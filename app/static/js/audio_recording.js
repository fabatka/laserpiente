'use strict';

const constraints = {audio: true, video: false};

const recBtn = document.querySelector("div#recordButton");
const ansTextBox = document.getElementById('answer');

let rec;
let localStream = null;

function permission() {
    if (!navigator.mediaDevices.getUserMedia) {
        alert('navigator.mediaDevices.getUserMedia not supported on your browser, use the latest version of Firefox or Chrome');
    } else {
        navigator.mediaDevices.getUserMedia(constraints)
            .then(function (stream) {
                localStream = stream;

                localStream.getTracks().forEach(function (track) {
                    if (track.kind === "audio") {
                        track.onended = function (event) {
                            console.log("audio track.onended Audio track.readyState=" + track.readyState + ", track.muted=" + track.muted);
                        }
                    }
                    if (track.kind === "video") {
                        track.onended = function (event) {
                            console.log("video track.onended Audio track.readyState=" + track.readyState + ", track.muted=" + track.muted);
                        }
                    }
                });

                try {
                    window.AudioContext = window.AudioContext || window.webkitAudioContext;
                    window.audioContext = new AudioContext();
                    const source = window.audioContext.createMediaStreamSource(stream);
                    rec = new Recorder(source);
                } catch (e) {
                    console.log('Web Audio API not supported.');
                }

            }).catch(function (err) {
            /* handle the error */
            console.log('navigator.getUserMedia error: ' + err);
        });
    }
}

permission();

$(recBtn).mousedown(function () {
    startRec()
});

$(recBtn).on('touchstart', function () {
    startRec()
})

$(recBtn).mouseup(function () {
    stopRec()
});

$(recBtn).on('touchend', function () {
    stopRec()
})

document.addEventListener("keydown", function (event) {
    let code = getKeyboardEventCode(event);
    if (((code === 97) || (code === 'a')) && !(Array.from(document.getElementsByTagName('textarea')).includes(document.activeElement))) {
        startRec()
    }
});

document.addEventListener("keyup", function (event) {
    let code = getKeyboardEventCode(event);
    if (((code === 97) || (code === 'a')) && !(Array.from(document.getElementsByTagName('textarea')).includes(document.activeElement))) {
        stopRec()
    }
});

function startRec() {
    if (recBtn.className === 'recordingStopped') {
        if (localStream == null) {
            // alert('Could not get local stream from mic/camera');
        } else {
            rec.record();
            recBtn.className = 'recordingStarted';
            console.log('Start recording...');
        }
    }
}

function stopRec() {
    if (recBtn.className === 'recordingStarted') {
        console.log('Stop recording')
        rec.stop();
        recBtn.className = 'recordingAnalyze';
        rec.exportWAV(function (blob) {
            let form = new FormData();
            form.append('file', blob, 'filename.wav');
            $.ajax({
                type: 'POST',
                url: '/audio',
                data: form,
                cache: false,
                processData: false,
                contentType: false
            }).done(function (data) {
                // write response into textarea
                // maybe return a non-200 status code and based on that write an output stating there was an error
                // in speech recognition?
                ansTextBox.value += data;
            }).fail(function (xhr, status, error) {
                // write error message into textarea
                ansTextBox.value += xhr.responseText;
            }).always(function () {
                recBtn.className = 'recordingStopped';
            });
        });
        rec.clear();
    }
}

navigator.mediaDevices.ondevicechange = function (event) {
    console.log("mediaDevices.ondevicechange");
    /*
    if (localStream != null){
        localStream.getTracks().forEach(function(track) {
            if(track.kind == "audio"){
                track.onended = function(event){
                    console.log("audio track.onended");
                }
            }
        });
    }
    */
};

//browser ID
function getBrowser() {
    const nVer = navigator.appVersion;
    const nAgt = navigator.userAgent;
    let browserName = navigator.appName;
    let fullVersion = '' + parseFloat(navigator.appVersion);
    let majorVersion = parseInt(navigator.appVersion, 10);
    let nameOffset, verOffset, ix;

    // In Opera, the true version is after "Opera" or after "Version"
    if ((verOffset = nAgt.indexOf("Opera")) !== -1) {
        browserName = "Opera";
        fullVersion = nAgt.substring(verOffset + 6);
        if ((verOffset = nAgt.indexOf("Version")) !== -1)
            fullVersion = nAgt.substring(verOffset + 8);
    }
    // In MSIE, the true version is after "MSIE" in userAgent
    else if ((verOffset = nAgt.indexOf("MSIE")) !== -1) {
        browserName = "Microsoft Internet Explorer";
        fullVersion = nAgt.substring(verOffset + 5);
    }
    // In Chrome, the true version is after "Chrome"
    else if ((verOffset = nAgt.indexOf("Chrome")) !== -1) {
        browserName = "Chrome";
        fullVersion = nAgt.substring(verOffset + 7);
    }
    // In Safari, the true version is after "Safari" or after "Version"
    else if ((verOffset = nAgt.indexOf("Safari")) !== -1) {
        browserName = "Safari";
        fullVersion = nAgt.substring(verOffset + 7);
        if ((verOffset = nAgt.indexOf("Version")) !== -1)
            fullVersion = nAgt.substring(verOffset + 8);
    }
    // In Firefox, the true version is after "Firefox"
    else if ((verOffset = nAgt.indexOf("Firefox")) !== -1) {
        browserName = "Firefox";
        fullVersion = nAgt.substring(verOffset + 8);
    }
    // In most other browsers, "name/version" is at the end of userAgent
    else if ((nameOffset = nAgt.lastIndexOf(' ') + 1) <
        (verOffset = nAgt.lastIndexOf('/'))) {
        browserName = nAgt.substring(nameOffset, verOffset);
        fullVersion = nAgt.substring(verOffset + 1);
        if (browserName.toLowerCase() === browserName.toUpperCase()) {
            browserName = navigator.appName;
        }
    }
    // trim the fullVersion string at semicolon/space if present
    if ((ix = fullVersion.indexOf(";")) !== -1)
        fullVersion = fullVersion.substring(0, ix);
    if ((ix = fullVersion.indexOf(" ")) !== -1)
        fullVersion = fullVersion.substring(0, ix);

    majorVersion = parseInt('' + fullVersion, 10);
    if (isNaN(majorVersion)) {
        fullVersion = '' + parseFloat(navigator.appVersion);
        majorVersion = parseInt(navigator.appVersion, 10);
    }


    return browserName;
}
