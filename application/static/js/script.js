
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

// AJAX Check task status.

const taskCheck = () => {
    fetch(`/queue`)
    .then(response => {
        // console.log(response.ok);
        return response.json();
    })
    .then(data => {
        console.log(data);
        let html = '<h2>Task Status: </h2>';
        data.forEach(elem => {
            html += `
                <ul>
                  <li>${elem}</li>
                </ul>
            `;
        });
        document.getElementById('status').innerHTML = html;
    })
    .catch(error => console.error())
}

const generateBtn = document.querySelector('.generate');

if (generateBtn) {
    generateBtn.addEventListener('mouseover', taskCheck);
}
