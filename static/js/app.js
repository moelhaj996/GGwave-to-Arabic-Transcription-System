document.addEventListener('DOMContentLoaded', () => {
    const startBtn = document.getElementById('startBtn');
    const stopBtn = document.getElementById('stopBtn');
    const statusIndicator = document.getElementById('statusIndicator');
    const statusText = document.getElementById('statusText');
    const originalText = document.getElementById('originalText');
    const translatedText = document.getElementById('translatedText');

    let isListening = false;
    let pollInterval;

    // Function to update the UI with new messages
    function updateMessages() {
        fetch('/messages')
            .then(response => response.json())
            .then(messages => {
                if (messages.length > 0) {
                    messages.forEach(msg => {
                        // Create elements for original text
                        const originalP = document.createElement('p');
                        originalP.textContent = msg.original;
                        originalText.appendChild(originalP);

                        // Create elements for translated text
                        const translatedP = document.createElement('p');
                        translatedP.textContent = msg.translated;
                        translatedText.appendChild(translatedP);

                        // Scroll to bottom
                        originalText.scrollTop = originalText.scrollHeight;
                        translatedText.scrollTop = translatedText.scrollHeight;
                    });
                }
            })
            .catch(error => {
                console.error('Error fetching messages:', error);
                stopListening();
            });
    }

    // Function to start listening
    function startListening() {
        fetch('/start')
            .then(response => response.json())
            .then(data => {
                if (data.status === 'success') {
                    isListening = true;
                    startBtn.disabled = true;
                    stopBtn.disabled = false;
                    statusIndicator.classList.add('active');
                    statusText.textContent = 'Listening for GGwave signals...';
                    
                    // Start polling for new messages
                    pollInterval = setInterval(updateMessages, 1000);
                } else {
                    throw new Error(data.message);
                }
            })
            .catch(error => {
                console.error('Error starting listener:', error);
                alert('Failed to start listening: ' + error.message);
            });
    }

    // Function to stop listening
    function stopListening() {
        fetch('/stop')
            .then(response => response.json())
            .then(data => {
                if (data.status === 'success') {
                    isListening = false;
                    startBtn.disabled = false;
                    stopBtn.disabled = true;
                    statusIndicator.classList.remove('active');
                    statusText.textContent = 'Not listening';
                    
                    // Stop polling for new messages
                    if (pollInterval) {
                        clearInterval(pollInterval);
                    }
                } else {
                    throw new Error(data.message);
                }
            })
            .catch(error => {
                console.error('Error stopping listener:', error);
                alert('Failed to stop listening: ' + error.message);
            });
    }

    // Event listeners for buttons
    startBtn.addEventListener('click', startListening);
    stopBtn.addEventListener('click', stopListening);

    // Clean up when the page is unloaded
    window.addEventListener('beforeunload', () => {
        if (isListening) {
            fetch('/stop').catch(() => {});
        }
    });
}); 