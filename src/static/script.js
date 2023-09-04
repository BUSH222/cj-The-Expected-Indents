// Get the button element by its ID
const startGameButton = document.getElementById('startGameButton');

// Add a click event listener to the button
startGameButton.addEventListener('click', function() {
	// Redirect to the "/start_game" URL
	window.location.href = '/start_game';
});

console.log('script.js loaded');