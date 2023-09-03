def gamelogic(word):
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
    letters = list(word)
    dis = ['_ ' for i in range(len(word))]
    lives = 6
    while lives >= 0:
        print(dis)
        if lives == 0:
            state = 'lost'
            break
        elif dis == letters:
            state = 'won'
            break
        guessed_letter = input('Guess a letter: ')
        if guessed_letter in letters and guessed_letter not in guessed_letters:
            i = letters.index(guessed_letter)
            dis[i] = letters[i]
            guessed_letters.append(guessed_letter)
            # unhide part of image function
        elif guessed_letter in letters and guessed_letter in guessed_letters:
            print("Already guessed")
        elif guessed_letter not in letters:
            lives -= 1
            # call function to get image peices if there are none then break
            # else look for a random image piece and turn it into pure white or pure black
    return state
