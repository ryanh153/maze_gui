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

	def play(self):
		while not self.won:
			guess = input("Enter your guess if you dare! ").lower()
			print()
			self.make_guess(guess)

	def make_guess(self, guess):
		print(f'player guessed: {guess}')
		if self.answer == guess:
			self.game_won()
		else:
			print("The tiles fall back onto the floor, amazingly into the same order the were originally.")

	def game_won(self):
		print('You win!')
		self.won = True
