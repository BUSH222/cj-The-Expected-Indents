import random
import secrets
import string

from flask import Flask, render_template, request

import imageprocessor  # noqa: F401
from game import Game

app = Flask(__name__)

games = dict()


def make_uid(length=6):
    """Generate a random uid of a set length."""
    characters = string.ascii_letters + string.digits
    chars = [secrets.choice(characters) for _ in range(length)]
    random_string = ''.join(chars)
    return random_string


def random_word():
    """Generate a random word to be used in the game."""
    with open('src/nouns-clear.txt') as nounfile:
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
    return render_template('game.html', uid=game_id, word_length=len(rword), lives='6')


@app.route('/game/<game_id>')
def make_move(game_id):
    """Process and make a move."""
    global games
    cgame = games[game_id]
    letter = request.data.strip()
    gameinfo = cgame.gamelogic(letter)
    return {'word': gameinfo[1],
            'lives': gameinfo[0],
            'delta_lives': int(gameinfo[2])-1,
            'feedback': gameinfo[2],
            'image': 'PLACEHOLDER'}


app.run(debug=True, host='127.0.0.1', port=5000)
