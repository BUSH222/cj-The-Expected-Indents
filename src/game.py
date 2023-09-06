from io import BytesIO
import requests
from PIL import Image
from imageprocessor import Im


class Game:
    """
    game class

    2 functions and 3 data members
    """

    def __init__(self, word, lives):
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
        self.guessed_letters = []
        self.wlen = len(word)
        self.dis = ["_"] * len(self.word)

    def play(self, guessed_letter):
        """
        Parameters

        ----------
        self : word(str),lives(int),guessed_letter(string)
        Returns
        -------
        lives(int),display(str),badletter(str)
        """
        res = requests.get(f"https://loremflickr.com/1024/1024/{self.word}")
        img = Image.open(BytesIO(res.content))
        Im1 = Im(img)
        Im1.split_image()
        letters = self.word
        self.badletter = False
        if self.lives == 0:
            return self.lives, "".join(self.dis), self.badletter, Im1.image_new
        if self.dis == letters:
            return self.lives, "".join(self.dis), self.badletter, Im1.image_new
        if guessed_letter in letters and guessed_letter not in self.guessed_letters:
            for j, lttr in enumerate(letters):
                if guessed_letter == lttr:
                    self.dis[j] = letters[j]
            Im1.place_tiles(letters, self.guessed_letters)
            self.guessed_letters.append(guessed_letter)
        if guessed_letter not in letters and guessed_letter in self.guessed_letters:
            self.badletter = True
        if guessed_letter not in letters:
            self.lives -= 1
            self.badletter = True
            Im1.remove_tiles()
        return self.lives, "".join(self.dis), self.badletter, Im1.image_new
        if guessed_letter not in letters:
            self.lives -= 1
            self.badletter = True
        return self.lives, "".join(dis), self.badletter
