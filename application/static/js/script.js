console.log('Javascript file enabled');


// Close flash messages.
const closeMessageButton = document.querySelector('.close');

if (closeMessageButton) {
    closeMessageButton.addEventListener('click', () => {
        document.querySelector('.flash-messages').remove();
    });
}

// Loader.
const loader = document.querySelector('.spinner');
const uploadForm = document.querySelector('.uploads');

if (loader) {
    window.addEventListener('pageshow', () => {
        document.querySelector('.spinner').style.display = 'none';
    });
}

const displayLoader = () => {
    document.querySelector('.spinner').style.display = 'inline-block';
};

uploadForm.addEventListener('submit', displayLoader);
