document.addEventListener('DOMContentLoaded', function () {
    const sendButton = document.getElementById('send-btn');
    const userInput = document.getElementById('user-input');
    const chat = document.getElementById('chat');

    sendButton.addEventListener('click', function () {
        const message = userInput.value;
        if (message.trim() !== '') {
            appendMessage('You', message, 'user-message');
            userInput.value = '';
            
            // Send the message to the backend
            fetch('/get_response', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({ message: message })
            })
            .then(response => response.json())
            .then(data => {
                appendMessage('Bot', data.response, 'bot-message');
            });
        }
    });

    function appendMessage(sender, message, className) {
        const messageDiv = document.createElement('div');
        messageDiv.classList.add(className);
        messageDiv.innerHTML = `<strong>${sender}:</strong> ${message}`;
        chat.appendChild(messageDiv);
        chat.scrollTop = chat.scrollHeight;
    }
});


