
// Close flash messages.
const closeMessageButton = document.querySelector('.close');

if (closeMessageButton) {
    closeMessageButton.addEventListener('click', () => {
        document.querySelector('.flash-messages').remove();
    });
}

// Display loader icon.
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


// Check the status of a task.

const generateBtn = document.querySelector('.generate');
generateBtn.addEventListener('mouseenter', () => console.log('clicked'));
