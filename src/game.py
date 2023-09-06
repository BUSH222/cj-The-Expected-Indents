from io import BytesIO

import requests
from PIL import Image

from imageprocessor import Im


class Game:
    """game class"""

    def __init__(self, word, lives):
        self.word = word
        self.lives = lives
        self.guessed_letters = []
        self.wlen = len(word)
        self.dis = ["_"] * len(self.word)
        self.size = 1024
        self.im = self.fetch_image()

    def fetch_image(self):
        """Fetch image from loremflickr using word

        Returns:
            Im object
        """
        res = requests.get(
            f"https://loremflickr.com/{self.size}/{self.size}/{self.word}", timeout=10
        )
        im = Im(Image.open(BytesIO(self.res.content)))
        im.split_image()
        return im

    def play(self, guessed_letter):
        """Play the next move

        Args:
            guessed_letter (string): guessed letter by user
        Returns:
            Tuple(int, str, bool, PIL Image): (remaining_lives, display, badletter, image)
        """
        badletter = False

        if guessed_letter in self.word and guessed_letter not in self.guessed_letters:
            # New letter guessed correctly
            for j, lttr in enumerate(self.word):
                if guessed_letter == lttr:
                    self.dis[j] = self.word[j]
            self.im.place_tiles(letters, guessed_letter)

        elif guessed_letter not in self.word:
            # Wrong letter guessed
            badletter = True

            if guessed_letter not in self.guessed_letters:
                # Deduct lives only for first time wrong guess
                self.lives -= 1
                self.im.remove_tiles()

        # Remember guessed_letter
        self.guessed_letters.add(guessed_letter)

        if "".join(self.dis) == self.word:
            # Guessed correct word. WIN!!!
            return self.lives, "".join(self.dis), badletter, self.im.image

        if self.lives == 0:
            # No more lives. Game Over!
            # TODO: return "game over" image
            return self.lives, "".join(self.dis), badletter, self.im.image_new

        return self.lives, "".join(self.dis), badletter, self.im.image_new
