import random

from flask import Flask, render_template

app = Flask(__name__)


@app.route('/')
def homepage():
    """Return the homepage for the game."""
    return render_template('index.html')


@app.route('/random_word')
def random_word():
    """Generate a random word to be used in the game."""
    with open('src/nouns-clear.txt') as nounfile:
        rword = random.choice(nounfile.readlines()).strip()
    return rword


app.run(debug=True, host='127.0.0.1', port=5000)
