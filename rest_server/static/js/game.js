let token = new URLSearchParams(window.location.search).get('token');
let lastUpdated = Date.now();

function updateTopOfBook() {
    fetch('/top-of-book')
    .then(response => {
        if (!response.ok) {
            throw new Error('Network response was not ok');
        }
        return response.json();
    })
    .then(data => {
        document.getElementById('best_bid').value = data[0];
        document.getElementById('num_bids').value = data[1];
        document.getElementById('best_ask').value = data[2];
        document.getElementById('num_asks').value = data[3];
        lastUpdated = Date.now();
    })
    .catch(error => console.error('There has been a problem with your fetch operation: ', error));
}

setInterval(function() {
    if (Date.now() - lastUpdated > 10000) {
        updateTopOfBook();
    }
}, 5000);

document.getElementById('quoteButton').addEventListener('click', function() {
    fetch('/quote', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
            bid: document.getElementById('bid').value,
            ask: document.getElementById('ask').value,
            token: token
        })
    })
    .then(response => {
        if (!response.ok) {
            throw new Error('Network response was not ok');
        }
        return response.json();
    })
    .then(data => {
        document.getElementById('status').value = data.message;
        updateTopOfBook();
    })
    .catch(error => console.error('There has been a problem with your fetch operation: ', error));
});

updateTopOfBook();
