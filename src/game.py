import imageprocessor
import requests
import io
from PIL import Image


class Game:
    """
    game class

    2 functions and 3 data members
    """

    def __init__(self, word, lives, guessed_letters, badletter):
        """
        Parameters

        ----------
        word : string
            Secret Code.
        lives : int
            no game no lives.
        letter : e
            E.

        Returns
        -------
        None.

        """
        self.word = word
        self.lives = lives
        self.guessed_letters = guessed_letters
        self.badletter = badletter

    def gamelogic(self, guessed_letter):
        """
        Parameters

        ----------
        self : word(str),lives(int),guessed_letter(string)
        Returns
        -------
        lives(int),display(str),badletter(str)
        """
        letters = list(self.word)
        dis = ['_' for i in range(len(self.word))]
        res = requests.get(f"https://loremflickr.com/1024/1024/{self.word}")
        img = Image.open(io.BytesIO(res.content))
        self.badletter = False
        img = imageprocessor.Im(self.image)
        if self.lives == 0:
            return self.lives, "".join(dis), self.badletter
        if dis == letters:
            return self.lives, "".join(dis), self.badletter
        if guessed_letter in letters and guessed_letter not in self.guessed_letters:
            i = letters.index(guessed_letter)
            dis[i] = letters[i]
            self.guessed_letters.append(guessed_letter)
        elif guessed_letter not in letters and guessed_letter in self.guessed_letters:
            self.badletter = True
        elif guessed_letter not in letters:
            self.lives -= 1
            self.badletter = True
        return self.lives, "".join(dis), self.badletter
        elif guessed_letter not in letters:
            self.lives -= 1
            self.badletter = True
        return self.lives, "".join(dis), self.badletter
