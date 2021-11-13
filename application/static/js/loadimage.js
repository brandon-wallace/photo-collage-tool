// application/static/js/loadimage.js

let taskStatus = document.querySelector('.task-status');
let taskState = document.querySelector('.task-state');

const getStatus = () => {
    fetch('/queue')
    .then((response) => response.json())
    .then((data) => {
        console.log(data.state);
        document.querySelector('.task-state').textContent = data.state;
        document.querySelector('.task-status').textContent = data.status;
    })
    .catch((error) => {
        console.error(error);
    });
}

const checkStatus = (fileName) => {
    const mseconds = 1000;
    (function reloadImage() {
        let imagePath = '';
        if (fileName.src.indexOf('?') > -1) {
            imagePath = fileName.src.split('?')[0];
        } else {
            imagePath = fileName.src;
        }
        fileName.src = `${imagePath}?t=${new Date().getTime()}`;

        setTimeout(reloadImage, mseconds);
    })();
}

window.onload = function() {
    let imageFile = document.querySelector('.collage__image');
    checkStatus(imageFile);
}
