import os
import random
import secrets
import string
from io import BytesIO

from flask import Flask, render_template, request, send_file

import imageprocessor  # noqa: F401
from game import Game

app = Flask(__name__)

games = dict()
game_images = dict()


def make_uid(length=6):
    """Generate a random uid of a set length."""
    characters = string.ascii_letters + string.digits
    chars = [secrets.choice(characters) for _ in range(length)]
    random_string = ''.join(chars)
    return random_string


def random_word():
    """Generate a random word to be used in the game."""
    script_dir = os.path.dirname(os.path.abspath(__file__))
    file_path = os.path.join(script_dir, 'nouns-clear.txt')
    with open(file_path) as nounfile:
        rword = random.choice(nounfile.readlines()).strip()
    return rword


@app.route('/')
def homepage():
    """Return the homepage for the game."""
    return render_template('home.html')


@app.route('/game')
def game_start():
    """Start the game."""
    global games
    rword = random_word()
    game_id = make_uid(games)
    games[game_id] = Game(rword, 6)
    game_images[game_id] = None
    return render_template('game.html', uid=game_id, word_length=len(rword), lives='6')


@app.route('/game/<game_id>')
def make_move(game_id):
    """Process and make a move."""
    global games, game_images
    assert game_id in games.keys()
    cgame = games[game_id]
    letter = request.data.strip()
    gameinfo = cgame.gamelogic(letter)
    game_images[game_id] = gameinfo[3]  # PIL Image
    return {'word': gameinfo[1],
            'lives': gameinfo[0],
            'delta_lives': int(gameinfo[2])-1,
            'feedback': gameinfo[2],
            'image': f'{request.url_root}image/{game_id}'}


@app.route('/image/<game_id>')
def get_image(game_id):
    """Return an image for the current game."""
    global game_images
    assert game_id in game_images.keys()
    img_io = BytesIO()
    pil_img = game_images[game_id]
    pil_img.save(img_io, 'JPEG', quality=70)
    img_io.seek(0)
    return send_file(img_io, mimetype='image/jpeg')


app.run(debug=True, host='127.0.0.1', port=9000)
