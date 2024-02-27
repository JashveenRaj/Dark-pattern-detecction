document.addEventListener('DOMContentLoaded', function() {
    var startButton = document.getElementById('start');
    startButton.addEventListener('click', function() {
        // Send HTTP request to Python server
        fetch('http://localhost:8000/run', { method: 'GET' })
            .then(response => response.text())
            .then(data => {
                console.log("Received response from server:", data);
                // Handle response if needed
            })
            .catch(error => console.error('Error:', error));
    });
  });