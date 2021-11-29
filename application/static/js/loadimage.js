// application/static/js/loadimage.js

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


const checkStatus = (imageElement) => {

    const mseconds = 1000;

    (function reloadImage() {
        let imagePath = '';
        if (imageElement.src.indexOf('?') > -1) {
            imagePath = imageElement.src.split('?')[0];
        } else {
            imagePath = imageElement.src;
        }
        imageElement.src = `${imagePath}?t=${new Date().getTime()}`;

        async function stopTimeout() {
            let response = await fetch(imageElement.src)
            if (response.status === 200) {
                return;
            } else {
                setTimeout(reloadImage, mseconds);
            }
        }

        stopTimeout();

    })();
}

window.onload = function() {
    let imageFile = document.querySelector('.collage__image');
    imageFile.addEventListener('load', () => {
        imageFile.classList.add('fade-in');
    });
    checkStatus(imageFile);
}
