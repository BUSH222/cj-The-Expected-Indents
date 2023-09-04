class Game:
    def __init__(self,word,lives,letter):
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
        self.word=word
        self.lives=lives
        self.letter=letter
    def gamelogic(self):
        """
        Parameters

        ----------
        word : string
            Secret Code.
        Returns
        -------
        state : string
            if the user has won or lost.
        """
        guessed_letters = []
        badletter = []
        guessed_letter = self.letter
        letters = list(self.word)
        dis = ['_ ' for i in range(len(self.word))]
        if self.lives == 0:
            return self.lives,"".join(dis),"".join(badletter)
        elif dis == letters:
            return self.lives,"".join(dis),"".join(badletter)
        if guessed_letter in letters and guessed_letter not in guessed_letters:
            i = letters.index(guessed_letter)
            dis[i] = letters[i]
            guessed_letters.append(guessed_letter)
            # unhide part of image function
        elif guessed_letter not in letters and guessed_letter in guessed_letters:
            badletter.append(guessed_letter)
        elif guessed_letter not in letters:
            self.lives -= 1
            # call function to get image peices if there are none then break
            # else look for a random image piece and turn it into pure white or pure black
        return self.lives,"".join(dis),"".join(badletter)
