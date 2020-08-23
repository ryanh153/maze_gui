# Bull Cow Game Class
class BCGame:

	def __init__(self, word):
		word.lower()
		self.answer = word
		self.numLetters = len(word)

	# TODO: Put in base class? So simple
	def make_guess(self, guess):
		return self.answer == guess
