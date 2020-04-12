'use strict';

const constraints = {audio: true, video: false};

const recBtn = document.querySelector("button#recordButton");
const stopBtn = document.querySelector("button#stopButton");


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
                            log("audio track.onended Audio track.readyState=" + track.readyState + ", track.muted=" + track.muted);
                        }
                    }
                    if (track.kind === "video") {
                        track.onended = function (event) {
                            log("video track.onended Audio track.readyState=" + track.readyState + ", track.muted=" + track.muted);
                        }
                    }
                });

                try {
                    window.AudioContext = window.AudioContext || window.webkitAudioContext;
                    window.audioContext = new AudioContext();
                    const source = window.audioContext.createMediaStreamSource(stream);
                    rec = new Recorder(source);
                } catch (e) {
                    log('Web Audio API not supported.');
                }

            }).catch(function (err) {
            /* handle the error */
            log('navigator.getUserMedia error: ' + err);
        });
    }
}


function onBtnRecordClicked() {
    permission();
    if (localStream == null) {
        // alert('Could not get local stream from mic/camera');
    } else {
        recBtn.disabled = true;
        stopBtn.disabled = false;

        /* use the stream */
        log('Start recording...');
        rec.record()
    }
}

navigator.mediaDevices.ondevicechange = function (event) {
    log("mediaDevices.ondevicechange");
    /*
    if (localStream != null){
        localStream.getTracks().forEach(function(track) {
            if(track.kind == "audio"){
                track.onended = function(event){
                    log("audio track.onended");
                }
            }
        });
    }
    */
};

function onBtnStopClicked() {
    rec.stop();
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
            console.log(data);
        });
    });
    rec.clear();
    // mediaRecorder.stop();
    recBtn.disabled = false;
    stopBtn.disabled = true;
}

function log(message) {
    console.log(message)
}

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
