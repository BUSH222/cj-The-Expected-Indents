let lifesign = "❤️";
let uid = document.getElementById("uid").innerText;
// console.log(`uid: ${uid}`);
let liveselement = document.getElementById("lives");
let imageelement = document.getElementById("hint");
let wordtable = document.getElementById("wordtable");
let warning = document.getElementById("warning");
let guessedletters = [];

function guess_character(inputValue) {
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

function decorate_word(inputString) {
    // Clear any existing content inside the table
    wordtable.innerHTML = '';

    // Create a new table element
    const table = document.createElement("table");

    // Split the input string into an array of characters
    const characters = inputString.split('');

    // Create the table rows
    for (let i = 0; i < 2; i++) {
        const row = document.createElement("tr");

        // Create table cells (th elements for the first row, td elements for the second row)
        for (let j = 0; j < characters.length; j++) {
            const cell = i === 0 ? document.createElement("th") : document.createElement("td");
            cell.textContent = characters[j];
            row.appendChild(cell);
        }

        table.appendChild(row);
    }

    // Append the table to the wordtable element
    wordtable.appendChild(table);
}


// Add an event listener to the form
document.getElementById('guess-form').addEventListener('submit', function (event) {
	event.preventDefault(); // Prevent the default form submission
	const inputValue = document.getElementById('letter').value;
	guess_character(inputValue);
	document.getElementById('letter').value = '';
});


window.onload =  function () {
	// Reset the guessedletters array
	guessedletters = [];
	// Reset the warning
	warning.innerText = "";
	// Reset the wordtable
	word_length  = document.getElementById("word_length").innerText;
	decorate_word("_".repeat(word_length));
	// Reset the liveselement
	lives = parseInt(document.getElementById("lives").innerText);
	liveselement.innerText = lifesign.repeat(lives);
}
