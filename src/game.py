class Game:
    """
    game class

    2 functions and 3 data members
    """

    def __init__(self, word, lives, guessed_letters):
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
        self.wlen = len(word)

    def play(self, guessed_letter):
        """
        Parameters

        ----------
        self : word(str),lives(int),guessed_letter(string)
        Returns
        -------
        lives(int),display(str),badletter(str)
        """
        letters = list(self.word)
        dis = ["_"] * len(self.word)
        self.badletter = False
        if self.lives == 0:
            return self.lives, "".join(dis), self.badletter
        if dis == letters:
            return self.lives, "".join(dis), self.badletter
        if guessed_letter in letters and guessed_letter not in self.guessed_letters:
            for j, lttr in enumerate(letters):
                if guessed_letter == lttr:
                    dis[j] = letters[j]
            self.guessed_letters.append(guessed_letter)
        if guessed_letter not in letters and guessed_letter in self.guessed_letters:
            self.badletter = True
        if guessed_letter not in letters:
            self.lives -= 1
            self.badletter = True
        return self.lives, "".join(dis), self.badletter
