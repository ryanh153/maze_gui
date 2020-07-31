# Word scramble game
import random


class WordScramble:

    def __init__(self, word):
        word = word.lower()
        self.answer = word

        wordList = list(word)
        random.shuffle(wordList)
        self.scrambled = ''.join(wordList)
        self.won = False

    def make_guess(self, guess):
        return self.answer == guess
