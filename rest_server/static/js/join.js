document.getElementById('joinButton').addEventListener('click', function() {
    let name = document.getElementById('user').value;
    if (!name) {
        alert("Please enter a name.");
        return;
    }

    fetch('/join', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ name: name })
    })
    .then(response => {
        if (!response.ok) {
            throw new Error('Network response was not ok');
        }
        return response.json();
    })
    .then(data => {
        if (data.token) {
            window.location.href = "/game?token=" + data.token;
        } else {
            alert("Failed to join. Please try again.");
        }
    })
    .catch(error => {
        console.error('There has been a problem with your fetch operation: ', error);
    });
});
