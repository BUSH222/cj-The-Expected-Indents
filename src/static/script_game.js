let lifesign = "❤️";
let uid = document.getElementById("uid").innerText;
// console.log(`uid: ${uid}`);
let liveselement = document.getElementById("lives");
let imageelement = document.getElementById("hint");
let wordtable = document.getElementById("wordtable");
let warning = document.getElementById("warning");
let guessedletters = [];

function foo(inputValue) {
	console.log("You entered: " + inputValue);

	// Check if the input is valid
	check = check_input(inputValue);

	if (check) {
		guessedletters.push(inputValue);  // Add the entered letter to the guessedletters array
		console.log(guessedletters);
		fetch("/game/" + uid)  // fetch the game data
			.then(response => response.json())
			.then(data => {
				/*
				I forgot exactly how we decided the API response should be... so I assume it's like this:
				{
					"word": "w_r_",
					"lives": 5,
					"image": "https://example.com/image.png"
				}
				*/

				// Extract data from the JSON response
				const word = data.word;
				const lives = data.lives;
				const image = data.image;

				// Update the wordtable by decorating the word
				decorate_word(word);

				// Update liveselement with lifesigns
				liveselement.innerText = lifesign.repeat(lives);

				// Update the imageelement's src attribute
				imageelement.src = image;
			})
			.catch(error => {
				console.error("Error fetching game data:", error);
			});
	}
}

function check_input(inputValue) {
	if (guessedletters.includes(inputValue)) {
		warning.innerText = "You already guessed this letter!";
		return false;
	}else if (inputValue.length != 1) {
		warning.innerText = "Please enter a single letter!";
		return false;
	}else if (!inputValue.match(/[a-z]/i)) {
		warning.innerText = "Please enter a valid letter!";
		return false;
	}else {
		warning.innerText = "";
		return true;
	}
}

function decorate_word(word) {
	wordtable.innerHTML = word;
}


// Add an event listener to the form
document.getElementById('guess-form').addEventListener('submit', function (event) {
	event.preventDefault(); // Prevent the default form submission
	const inputValue = document.getElementById('letter').value;
	foo(inputValue);
	document.getElementById('letter').value = '';
});
