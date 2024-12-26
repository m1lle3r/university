def coded(word, guessed_letters):
    displayed = ' '.join(letter if letter in guessed_letters else '■' for letter in word)
    return displayed