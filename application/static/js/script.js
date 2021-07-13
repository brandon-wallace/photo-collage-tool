console.log('Javascript file enabled');


// Close flash messages.
const closeMessageButton = document.querySelector('.close');

if (closeMessageButton) {
    closeMessageButton.addEventListener('click', () => {
        document.querySelector('.flash-messages').remove();
    });
}
