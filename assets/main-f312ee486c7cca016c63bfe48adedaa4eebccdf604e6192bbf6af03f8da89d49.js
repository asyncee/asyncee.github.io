function addEventListenerByClass(className, event, fn) {
    var list = document.getElementsByClassName(className);
    for (var i = 0, len = list.length; i < len; i++) {
        list[i].addEventListener(event, fn, false);
    }
}

function fadeinImages() {
  this.className += ' fadein-on-load--loaded'
}

addEventListenerByClass('fadein-on-load', 'load', fadeinImages);
