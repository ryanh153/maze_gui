class Player:

	def __init__(self, position):

		self.pos = position
		self.smallKeys = 0
		self.largeKeys = 0
		self.thorWins = 0
		self.audumblaWins = 0
		self.mathGameWins = 0
		self.lokiWins = 0

	def move(self, direction):
		if direction == "n":
			self.pos[0] += 1
		elif direction == "e":
			self.pos[1] += 1
		elif direction == "s":
			self.pos[0] -= 1
		elif direction == "w":
			self.pos[1] -= 1
