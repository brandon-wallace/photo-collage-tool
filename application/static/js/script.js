
// Close flash messages.
const closeMessageButton = document.querySelector('.close');

if (closeMessageButton) {
    closeMessageButton.addEventListener('click', () => {
        document.querySelector('.flash-messages').remove();
    });
}


// Display loader icon on click of upload button.

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

if (uploadForm) {
    uploadForm.addEventListener('submit', displayLoader);
}


// Check upload file size.

const fileInput = document.getElementById('images');
const uploadBtn = document.querySelector('.upload-btn');

const checkFileSize = () => {
    const allFiles = [...fileInput.files];
    let totalSize = 0;
    for (let i = 0; i < allFiles.length; i++) {
        totalSize += allFiles[i].size;
        if (totalSize === 0) {
            return;
        } else {
            uploadBtn.disabled = false;
            uploadBtn.classList.remove('disabled'); 
        }
        if (allFiles[i].size > 5242880) {
            alert('File exceeds 5 MB limit.')
            return;
        } 
    }
}

if (fileInput) {
    uploadBtn.disabled = true;
    fileInput.addEventListener('change', checkFileSize);
}


// Display loader icon on click of upload button.

const collageDiv = document.querySelector('.collage');
const collageImg = document.querySelector('.collage__image');

if (collageImg) {
    window.addEventListener('pageshow', () => {
        document.querySelector('.spinner').style.display = 'inline-block';
    });

    const hideLoader = (event) => {
        document.querySelector('.spinner').style.display = 'none';
    };

    collageImg.addEventListener('load', hideLoader);
}
