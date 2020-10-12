class BaseCreature:

	def __init__(self, pos, game, pre_text, main_text, fail_text, post_text, reward):

		self.pos = pos
		self.game = game
		self.pre_text = pre_text
		self.main_text = main_text
		self.fail_text = fail_text
		self.post_text = post_text
		self.reward = reward
		self.started_game = False
		self.name = None

	def give_reward(self, player):
		self.started_game = False
		if self.reward == 'small':
			player.small_keys += 1
		elif self.reward == 'large':
			player.large_keys += 1
		else:
			print("You get... nothing!")
