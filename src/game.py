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
        dis = ['_ ' for i in range(len(self.word))]

        if self.lives == 0:
            return self.lives, "".join(dis), self.badletter
        if dis == letters:
            return self.lives, "".join(dis), self.badletter
        if guessed_letter in letters and guessed_letter not in self.guessed_letters:
            i = letters.index(guessed_letter)
            dis[i] = letters[i]
            self.guessed_letters.append(guessed_letter)
            # unhide part of image function
        elif guessed_letter not in letters and guessed_letter in self.guessed_letters:
            self.badletter = True
        elif guessed_letter not in letters:
            self.lives -= 1
            self.badletter = True
            # call function to get image peices if there are none then break
            # else look for a random image piece and turn it into pure white or pure black
        return self.lives, "".join(dis), self.badletter
            # call function to get image peices if there are none then break
            # else look for a random image piece and turn it into pure white or pure black
        return self.lives, "".join(dis), self.badletter
