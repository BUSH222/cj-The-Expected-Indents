import os
import random
import secrets
import string

from svd import SVDImage


def make_uid(length=6):
    """Generate a random uid of a set length.

    Args:
        length (int, default=6): The length of the random id. Should be 1 or more.

    Raises:
        AssertionError: Length can't be 0 or lower.

    Returns:
        str: A random uid.
    """
    characters = string.ascii_letters + string.digits
    chars = [secrets.choice(characters) for _ in range(length)]
    random_string = ''.join(chars)
    return random_string


class Game:
    """game class"""

    def __init__(self, lives=6):
        self.word = self._get_random_word()
        print(self.word)
        self.lives = lives
        self.guessed_letters = set()
        self.size = 512
        self.image = SVDImage(self.word, self.size)
        self.alive = True

        self.reward = 0
        # constants used to calculate reward
        # 0 < 2m < u  for best results
        self.m = 20  # number of terms to show after half of the word has been guessed
        self.u = 100  # number of terms to show when full word has been guessed
        # self.u number of terms will actually never be shown
        # when the full word is guessed, the game ends and the actual image is shown
        # but this is just a constant to calculate the reward

    def _get_random_word(self):
        script_dir = os.path.dirname(os.path.abspath(__file__))
        file_path = os.path.join(script_dir, 'nouns-clear.txt')
        with open(file_path) as nounfile:
            rword = random.choice(nounfile.readlines()).strip()
        return rword

    def _construct_word_with_underscores(self):
        ret = ''
        for letter in self.word:
            if letter in self.guessed_letters:
                ret += letter
            else:
                ret += '_'
        return ret

    def _calulate_reward(self):
        # we used an exponential function to calculate the reward
        # the reward is 0 when no letters are guessed
        # the reward is self.m when half of the letters are guessed
        # the reward is self.u when all letters are guessed
        x = sum([letter in self.guessed_letters for letter in self.word])/len(self.word)
        k = (self.u-self.m)/self.m
        coeff = self.m / (k-1)
        self.reward = int(coeff * (k**(2*x) - 1))

    def play(self, guessed_letter):
        """Play the game by guessing a letter.

        Args:
            guessed_letter (str): The letter guessed by the user. Should be a single letter.

        Returns:
            dict: {
                'word': 'e_e_h_n_'  # word with underscores for unguessed letters
                'lives': 5,  # number of lives left
                'delta_lives': 0 if feedback else -1,  # change in lives
                'feedback': True,  # True if letter is in word, False otherwise
            }
        """
        # repeated letters won't come; handled in frontend
        if not self.alive:
            return {
                'word': self.word,
                'lives': 0,
                'delta_lives': 0,
                'feedback': False,
            }
        if guessed_letter in self.word:
            feedback = True
        else:
            feedback = False
            self.lives -= 1

        if self.lives == 0:
            self.alive = False

        self.guessed_letters.add(guessed_letter)
        self._calulate_reward()
        return {
            'word': self._construct_word_with_underscores(),  # 'e_e_h_n_'
            'lives': self.lives,  # 5
            'delta_lives': 0 if feedback else -1,  # 0 or -1
            'feedback': feedback,  # True if letter is in word, False otherwise
        }
