
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

if (uploadBtn) {
    uploadBtn.disable = true;
    uploadBtn.classList.add('disabled');
}

const checkFileSize = () => {
    const allFiles = [...fileInput.files];
    let totalSize = 0;
    for (let i = 0; i < allFiles.length; i++) {
        totalSize += allFiles[i].size;
        if (allFiles[i].size > 20971520) {
            alert('File exceeds 20 MB limit.')
            return;
        } 
        if (totalSize === 0) return;
        uploadBtn.disabled = false;
        uploadBtn.classList.remove('disabled'); 
    }
}

if (fileInput) {
    fileInput.addEventListener('change', checkFileSize);
}


// Display loader icon on click of upload button.

const collageImg = document.querySelector('.collage__image');

if (collageImg) {
    window.addEventListener('pageshow', () => {
        document.querySelector('.spinner').style.display = 'inline-block';
    });
}

const hideLoader = (event) => {
    console.log(`Image loaded`);
    document.querySelector('.spinner').style.display = 'none';
};

collageImg.addEventListener('load', hideLoader);


// ================

const collageDiv = document.querySelector('.collage');

if (collageDiv) {
    let count = 0;
    const intervalId = setInterval(() => {
        document.querySelector('.spinner').style.display = 'inline-block';
        let collage = document.querySelector('.collage__image');
        console.log(collage.src);
        console.log(count);
        count = count + 1;
        if (collage) {
            document.querySelector('.spinner').style.display = 'none';
            clearInterval(intervalId);
        }
        
    }, 1000);
}
