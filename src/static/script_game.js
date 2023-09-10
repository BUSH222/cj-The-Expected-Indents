let lifesign = "❤️";
let uid = document.getElementById("uid").innerText;
// console.log(`uid: ${uid}`);
let liveselement = document.getElementById("lives");
let imageelement = document.getElementById("hint");
let wordtable = document.getElementById("wordtable");
let warning = document.getElementById("warning");
let modal = document.getElementById("winorlose");
let modal_text = document.getElementById("winorlose-text");
let feedback_text = document.getElementById("feedback");
let guessedletters = [];
let lives = 0;
let cache_busting = 0;


function guess_character(guessedLetter) {
	console.log("You entered: " + guessedLetter);

	// Check if the input is valid
	check = check_input(guessedLetter);

	if (check) {
		guessedletters.push(guessedLetter);  // Add the entered letter to the guessedletters array
		console.log(guessedletters);
		fetch(`/guess/${uid}/${guessedLetter}`) // Send a GET request to the API endpoint
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
				const lives_ = data.lives;
				const deltalives = data.delta_lives;
				const feedback = data.feedback;

				// console.log(`lives: ${lives_}\ndeltalives: ${deltalives}, \nfeedback: ${feedback}`);


				// Update the wordtable by decorating the word
				decorate_word(word);

				// Update the lives
				if (lives + deltalives == lives_) {
					lives = lives_;
				} else {
					alert(`lives: ${lives}, lives_: ${lives_}, deltalives: ${deltalives}`);
					// window.location.reload();
				}
				liveselement.innerText = lifesign.repeat(lives);

				// Update the imageelement's src attribute
				imageelement.src = `/image/${uid}?${cache_busting++}`

				// Update the status
				show_status(feedback, lives, word);

				document.getElementById("letter").focus();
			})
			.catch(error => {
				console.error("Error fetching game data:", error);
			});
	}
}

function check_input(guessedLetter) {
	if (guessedletters.includes(guessedLetter)) {
		warning.innerText = "You already guessed this letter!";
		return false;
	} else if (guessedLetter.length != 1) {
		warning.innerText = "Please enter a single letter!";
		return false;
	} else if (!guessedLetter.match(/[a-z]/i)) {
		warning.innerText = "Please enter a valid letter!";
		return false;
	} else {
		warning.innerText = "";
		return true;
	}
}

function decorate_word(inputString) {
	// Clear any existing content inside the table
	wordtable.innerHTML = '';

	// Create a new table element
	const table = document.createElement("table");

	// Split the input string into an array of characters
	const characters = inputString.split('');


	const row1 = document.createElement("tr");
	const row2 = document.createElement("tr");
	for (let j = 0; j < characters.length; j++) {
		const cell1 = document.createElement("th");
		const cell2 = document.createElement("td");
		cell1.textContent = `${j + 1}`;
		cell2.textContent = characters[j];
		row1.appendChild(cell1);
		row2.appendChild(cell2);
	}
	table.appendChild(row1);
	table.appendChild(row2);

	// Append the table to the wordtable element
	wordtable.appendChild(table);
}


// Add an event listener to the form
document.getElementById('guess-form').addEventListener('submit', function (event) {
	event.preventDefault(); // Prevent the default form submission
	const guessedLetter = document.getElementById('letter').value;
	guess_character(guessedLetter);
	document.getElementById('letter').value = '';
});


window.onload = function () {
	// Reset the guessedletters array
	guessedletters = [];
	// Reset the warning
	warning.innerText = "";
	// Reset the wordtable
	word_length = document.getElementById("word_length").innerText;
	decorate_word("_".repeat(word_length));
	// Reset the liveselement
	lives = parseInt(document.getElementById("lives").innerText);
	liveselement.innerText = lifesign.repeat(lives);
}

function show_status(feedback, lives, word) {
	if (lives == 0) {
		// Player has lost
		modal_text.innerText = "You lose! The word was: " + word;
		modal.showModal()
	} else if (!word.includes("_")) {
		// Player has won
		modal_text.innerText = "You win!";
		modal.showModal()
	}

	// Set the feedback text based on the value of 'feedback'
	feedback_text.textContent = feedback ? "Correct guess!" : "Incorrect guess!";
}
