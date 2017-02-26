function addEventListenerByClass(className, event, fn) {
    var list = document.getElementsByClassName(className);
    for (var i = 0, len = list.length; i < len; i++) {
        list[i].addEventListener(event, fn, false);
    }
}

function fadeinImages() {
    console.log(this);
  this.className += ' fadein-on-load--loaded';
}

function initMediumZoom() {
    mediumZoom('.content img');
}

function onDocumentReady() {
    addEventListenerByClass('fadein-on-load', 'load', fadeinImages);
}

document.addEventListener("DOMContentLoaded", onDocumentReady);
