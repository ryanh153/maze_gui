# Word scramble game
import random


class WordScramble:

    def __init__(self, word):
        word = word.lower()
        self.answer = word

        word_list = list(word)
        while list(word) == word_list:
            random.shuffle(word_list)
        self.scrambled = ''.join(word_list)

    def make_guess(self, guess):
        return self.answer == guess
