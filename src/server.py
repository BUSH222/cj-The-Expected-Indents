from io import BytesIO

from flask import Flask, render_template, send_file
from PIL import Image

from game import Game, make_uid

app = Flask(__name__)

games = dict()


@app.route('/')
def homepage():
    """Return the homepage for the game."""
    return render_template('home.html')


@app.route('/start_game')
def start_game():
    """Start the game."""
    global games
    uid = make_uid()
    game = Game()  # make a new game
    games[uid] = game
    return render_template(
        'game.html',
        uid=uid,
        word_length=len(game.word),
        lives=game.lives
    )


@app.route('/guess/<game_id>/<letter>')
def make_move(game_id, letter):
    """Process and make a move.

    Args:
        game_id (str): The id for the game in which the move was made.
    Raises:
        AssertionError: Game must exist, game_id must be a key the games dictionary.
    Returns:
        dict: Updated data after the move: word status, lives, change in lives,
                if the user guessed a letter in a word (feedback), image link.
    """
    cgame = games.get(game_id)
    if cgame is None:
        return {'error': 'game does not exist'}
    return cgame.play(letter)


@app.route('/image/<game_id>')
def get_image(game_id):
    """Return an image for the current game.

    Args:
        game_id (str): The id for the game in which the move was made.

    Raises:
        AssertionError: Game must exist, game_id must be a key the games_images dictionary.

    Returns:
        JPEG file: image for the game with an id game_id.
    """
    cgame = games.get(game_id)
    if cgame is None:
        return {'error': 'game does not exist'}
    img_io = BytesIO()
    np_image = cgame.get_image()
    pil_img = Image.fromarray(np_image)
    pil_img.save(img_io, 'JPEG', quality=70)
    img_io.seek(0)
    return send_file(img_io, mimetype='t')


app.run(debug=True, host='127.0.0.1', port=5000)
