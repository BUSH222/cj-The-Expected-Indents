# Picturepuzzlers

__Check out the [presentation](presentation.pdf) for this project as well!__

## Project overview
Welcome to an exciting and interactive game experience! In this game, players are challenged to uncover a secret word by guessing its letters (Just like in Hangman!). But here's the twist: there's an intriguing twist! Alongside the letters, you'll also encounter a scrambled image that provides vital clues to help you crack the code.

As you progress through the game, the image becomes more or less scrambled based on your letter guesses. Each correct letter brings you closer to unraveling the mystery, resulting in a clearer image that guides you towards the hidden word. However, an incorrect guess adds an extra layer of complexity, further scrambling the image and putting your deduction skills to the test.


## Objectives
1. Implement Word Guessing Mechanics
    - Develop the core functionality of the game, allowing players to guess letters of a secret word and track their progress. (game.py)

2. Image Scrambling
    - Create a mechanism to scramble the image based on the player's letter guesses, providing visual clues to aid in solving the word. (svd.py)

3. Implement User Interface and Experience
    - Create and improve the user interface design and overall user experience to make the game more engaging and intuitive for players. (templates/)

4. Connect everything together (server.py)
    - Get the game in working order by connecting all parts of the game (server.py)

## Gameplay example

https://github.com/BUSH222/cj-The-Expected-Indents/assets/58144503/1f0f4eb9-b270-4b00-99c1-998f52f6ba55

Here the word "answer" is the solution, and as you can see the player guesses 3 letters incorrectly, making random squares disappear from the image! However, when the player guesses correctly, the image gets slowly more comprehensible.

## Instructions for use and Installation
### From scratch:
- Clone [the repo](https://github.com/BUSH222/cj-The-Expected-Indents)
- Install the required libraries in `dev-requirements.txt`
- Run `src/server.py` using python
- In your browser, go to [`http://127.0.0.1:5000`](http://127.0.0.1:5000)
### OR Visit the website:
[http://picturepuzzlers.pythonanywhere.com/](http://picturepuzzlers.pythonanywhere.com/ "http://picturepuzzlers.pythonanywhere.com/")


## Code Structure
All the code for the project is located in the [src](https://github.com/BUSH222/cj-The-Expected-Indents/tree/main/src) folder in the repository.

The code uses Python for the backend portion of the game, specifically libraries such as __Flask__ for the server and __numpy__ for image processing.

The program consists of 5 main parts:
- game.py
    - Keeps track of all of the vital parameters of the game in the Game class, such as lives, guessed letters, whether the player won, etc.
- server.py
    - Connects the game logic to the frontend, allowing the user to interact with the frontend.
- svd.py
    - The image processing algorithm used in the game
- HTML/CSS/JS part
    - Handles all the UI and does some valid input checks

## Image Processing
There are two main image processing methods used in the project:

- [Singular Value Decomposition (SVD)](#singular-value-decomposition-svd)
  - [Theoretical Foundation](#theoretical-foundation)
  - [Ordering Singular Values](#ordering-singular-values)
  - [Application in the Project](#application-in-the-project)
- [Masking the Image for Penalty](#masking-the-image-for-penalty)
  - [Penalty Mechanism](#penalty-mechanism)
  - [Maximum Player Life](#maximum-player-life)
  - [Penalty Severity](#penalty-severity)

### Singular Value Decomposition (SVD)

Singular Value Decomposition (SVD) is a matrix factorization method used to decompose a matrix $A$ into three constituent components.

#### Theoretical Foundation

- In SVD, matrix $A$ is decomposed into three matrices: $U$, $S$, and $V$. Here's the representation of this decomposition:

  $$A_{n\times m} = U_{n\times n} \times S_{n\times m} \times V_{m\times m}$$

  - $U$ and $V$ are [unitary matrices](https://en.wikipedia.org/wiki/Unitary_matrix), and $S$ is a diagonal matrix.
  - The diagonal elements of matrix $S$ are referred to as the ["singular values"](https://en.wikipedia.org/wiki/Singular_value) of matrix $A."

- The singular values of matrix $A$ can be obtained from the square roots of the eigenvalues of both $A^*A$ and $AA^*$.

#### Ordering Singular Values

- The singular values $S_i$ of $A$ can be ordered in a non-increasing manner.

- Specifically, $S_a$ is greater than $S_b$ if $a > b$, where $S_i$ represents the $(i,\;i)$th element of matrix $S$.

- The larger the singular value $S_i$, the more significant the $i$th row and column of matrices $U$ and $V$ are in the decomposition.

##### Application in the Project

- In the project, the first term of the SVD is initially considered to reconstruct the image, resulting in a rough representation.

- As more terms are included, the image becomes progressively clearer.

- Recognizing that later terms in the Singular Value Decomposition exert diminishing influence on image quality, transitioning from the first to the second term yields a more substantial improvement than from the 10th to the 11th term. Now, the player should get similar amount of extra information for each correct guess. This is achieved by using an exponential curve.

- Parameters `u` and `m` are introduced to calculate the reward (i.e., the number of terms to display) based on the state of progress. Parameter `u` represents the number of terms to display when the player has guessed the full word, and `m` represents the number of terms to display when the player has guessed half of the word.

- Variable $x$ $(0 \le x \le 1)$ is a measure of how much part of the word has been guessed. The reward calculation is expressed as:

  $$reward(x) = \frac{m}{k-1}(k^{2x}-1),\;\text{ where }\; k = \frac{u-m}{m}$$

- Experimentation determined that `u = 100` and `m = 20` provide effective results for the project. In the initial correct guesses we include less terms than in the later correct guesses.

- The [numpy.linalg.svd](https://numpy.org/doc/stable/reference/generated/numpy.linalg.svd.html) function is utilized to calculate the SVD of the matrix.



### Masking the Image for Penalty

In this game scenario, a binary mask matrix is maintained, which is divided into square grids (in this case, each image is divided into 32x32 grids). Initially, all elements of the matrix are set to 1, representing a clear image. The objective is to obscure parts of the image as a penalty when the player guesses a wrong letter.

#### Penalty Mechanism

- When a player makes an incorrect guess, a penalty is imposed by randomly selecting one of the grid cells in the binary mask matrix.

- Within the chosen grid cell, all elements (pixels) are set to 0 with a predetermined probability, denoted as `p` (in this case, `p = 0.2`).

- This process is repeated each time the player guesses incorrectly, causing additional portions of the image to be obscured.

##### Maximum Player Life

The game's difficulty is designed around the concept of player lives, with a maximum of 6 lives allotted to the player. Each incorrect guess reduces the player's life count.

#### Penalty Severity

- The probability `p` of setting elements to 0 within a grid cell is set to 0.2.

- Calculation reveals that if the player is left with only one life at some point in the game, there is a cumulative effect of obscuring grid cells. This results in approximately 67% of the image being obscured.

- This level of image obscurity is considered an appropriate and challenging penalty for the player's remaining life, adding an element of difficulty to the game.

The design choice of 67% image obscurity aligns with the game's intention to provide an engaging and challenging experience for the player.

## Contributors and their contributions
- Discord: `bush22`; [Github](https://github.com/BUSH222)
    - Created server.py
- Discord: `grn01`; [Github](https://github.com/CodeRulerNo1)
    - Created the game logic in game.py
- Discord: `peithonking`; [Github](https://github.com/PeithonKing)
    - Created the image processing algorithm and the frontend part
- Discord: `dha72`; [Github](https://github.com/dhananjaylatkar)
    - Helped with the frontend and the game logic
- Discord: `zike01`; [Github](https://github.com/Zike01)
    - Contributed heavily to the image processing part

## License

The project is licensed under the MIT License. See the [LICENSE](LICENSE)
