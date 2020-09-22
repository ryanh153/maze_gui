class Player:

	def __init__(self, position):

		self.pos = position
		self.small_keys = 100
		self.large_keys = 100
		self.thor_wins = 0
		self.audumbla_wins = 0
		self.math_game_wins = 0
		self.loki_wins = 0

	def move(self, direction):
		if direction == "n":
			self.pos[0] += 1
		elif direction == "e":
			self.pos[1] += 1
		elif direction == "s":
			self.pos[0] -= 1
		elif direction == "w":
			self.pos[1] -= 1
