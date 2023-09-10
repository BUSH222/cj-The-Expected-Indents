// Get the button element by its ID
const startGameButton = document.getElementById('startGameButton');

// When the user clicks on the button, go to the next page
startGameButton.addEventListener('click', next_page);

// When the user hits the enter key, go to the next page
document.addEventListener("keydown", function(event) {
    if (event.key === "Enter") {next_page()}
});

// This is how we go to the next page
function next_page() {
    // show the wait text and loader
	var waitTextElement = document.getElementById("wait_text");
    var loaderElement = document.querySelector(".loader");

    // Set their display property to "block" to make them visible
    if (waitTextElement) {
        waitTextElement.style.display = "block";
    }

    if (loaderElement) {
        loaderElement.style.display = "block";
    }

	// Go to the next page
	window.location.href = '/start_game';
}
