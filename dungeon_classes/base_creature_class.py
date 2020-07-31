class BaseCreature:

	def __init__(self, pos, game):

		self.pos = pos
		self.game = game
		self.started_game = False
		self.current_text = ''
