from dungeon_classes.base_creature_class import BaseCreature


class Audumbla(BaseCreature):

    def __init__(self, pos, game):
        super(Audumbla, self).__init__(pos, game)
        self.name = 'Audumbla'

    def interact(self, player, guess=None):
        # floor 1
        if player.audumbla_wins == 0:
            if self.started_game:
                return self.play_encounter1(player, guess)
            else:
                return self.begin_encounter1()
        if player.audumbla_wins == 1:
            if self.started_game:
                return self.play_encounter2(player, guess)
            else:
                return self.begin_encounter2()

        # # floor 2
        # elif player.audumbla_wins == 2:
        # 	self.encounter3(player, autoWin)
        # elif player.audumbla_wins == 3:
        # 	self.encounter4(player, autoWin)
        # elif player.audumbla_wins == 4:
        # 	self.encounter5(player, autoWin)
        # # floor 3
        # elif player.audumbla_wins == 5:
        # 	self.encounter6(player, autoWin)
        # elif player.audumbla_wins == 6:
        # 	self.encounter7(player, autoWin)
        # elif player.audumbla_wins == 7:
        # 	self.encounter8(player, autoWin)
        # elif player.audumbla_wins == 8:
        # 	self.encounter9(player, autoWin)
        # elif player.audumbla_wins == 9:
        # 	self.encounter10(player, autoWin)
        # elif player.audumbla_wins == 10:
        # 	self.encounter11(player, autoWin)
        # elif player.audumbla_wins == 11:
        # 	self.encounter12(player, autoWin)
        # elif player.audumbla_wins == 12:
        # 	self.encounter13(player, autoWin)
        # elif player.audumbla_wins == 13:
        # 	self.encounter14(player, autoWin)
        # elif player.audumbla_wins == 14:
        # 	self.encounter15(player, autoWin)

        else:
            raise ValueError("Not coded!")

    def next_reward(self, player):
        if player.audumbla_wins in [0]:
            return 'small'
        elif player.audumbla_wins in [1]:
            return 'large'
        else:
            raise ValueError("There is no next reward!")

    def incorrect_guess_feedback(self, guess):
        bulls, cows, text = 0, 0, []

        for i, char in enumerate(guess):
            if char in self.game.answer:
                if char == self.game.answer[i]:
                    bulls += 1
                else:
                    cows += 1

        if cows == 0 and bulls == 0:
            text.extend(["The cow stares at you blankly. Judgement flowing off it in palpable waves."])
        else:
            if bulls == 1:
                text.extend(["The cow licks a block of salt in front of it once."])
            elif bulls > 1:
                text.extend(["The cow licks a block of salt in front of it %d times" % bulls])

            if cows == 1:
                text.extend(["The cow stomps it front left hoof once"])
            elif cows > 1:
                text.extend(["The cow stomps it front left hoof %d times" % cows])

            text.extend(["You take a step back to process this new information.",
                         ''])

        return text

    def reward(self, player):
        self.started_game = False
        if self.next_reward(player) == 'small':
            player.small_keys += 1
        else:
            player.large_keys += 1
        player.audumbla_wins += 1

    def begin_encounter1(self):
        """Set text to be displayed at the top on each turn (self.current text) and display setup to game"""

        self.current_text = ["The cows eyes stare into you soul. Their emptiness reflecting your progress thus far.",
                             "You somehow get the feeling Audumbla believes your progress will remain dreadfully low.",
                             "Hoping to prove this primordial cow, and your parents, wrong you step forward.",
                             "Enter the order you wish to place the tiles or \"exit\" to return to the map.",
                             '']

        text = ["In the room you see a mighty cow. On the floor next to it lies a piece of parchment.",
                "You bend over and pick it up. Written in smooth, dark ink are a strange set of instructions.",
                "",
                "Before you lies Audumbla, the most ancient and powerful cow in the 9 realms.",
                "The cow's mind is deep and troubled. For though it can think of words it cannot speak them.",
                "If you be brave of heart, help the cow in her plight by speaking the word that she is thinking.",
                "To do this you must step up to her and speak a word whose length is equal to the number of children "
                "spawned by Aegir and Ran.",
                "The cow will lick the block of salt in front of it once for every letter in your word that is also "
                "in her word, and in the correct position.",
                "She will then stomp her hoof once for every other letter in your word that is in her word, "
                "but not in the correct position.",
                "If you please the cow you will be rewarded.",
                "Enter 'solve puzzle' face this strange challenge.",
                ""]

        return text

    def play_encounter1(self, player, guess):
        text, solved = [], False
        if self.game.make_guess(guess):
            solved = True
            self.reward(player)
            text.extend(["The cow takes a step forward. You flinch but hold your ground.",
                         "It leans forward and licks your palm.",
                         "Looking down you see a shiny silver key in your palm.",
                         "Success! You have defeated a mute bovine creature in a game of words and wits. Take that "
                         "world!",
                         "",
                         "The cow bows it's head deeply. Clearly out of respect for you, and not to lick the salt "
                         "block one more time (although it does this as well).",
                         "It then fades. Seeming to slide out of existance as easily as a primordial knife through "
                         "primordial cow butter.",
                         "You look around the room for a few seconds before deciding there is nothing more to be done "
                         "here.",
                         ""])
        else:
            if len(guess) != len(self.game.answer):  # Wrong number of letters, can't really play
                text.extend(["The cow looks at you imploringly. Perhaps you did not remember your norse mythology as "
                             "well as you had though...",
                             ""])
            else:  # Play a round
                text.extend(self.incorrect_guess_feedback(guess))

        return solved, text

    def begin_encounter2(self):
        """Set text to be displayed at the top on each turn (self.current text) and display setup to game"""

        self.current_text = ["The cow stands before you again",
                             "You scan the ground for another set of instructions but see none.",
                             "Enter the order you wish to place the tiles or \"exit\" to return to the map.",
                             '']

        text = ["\"Let's dance you and I.\" you cackle.",
                "You look at the cow, hoping your witty banter has thrown it off guard.",
                "The cow blinks 6 times and then simply stares at you.",
                "Only mildly unnerved you decide it's time to begin guessing.",
                '']

        return text

    def play_encounter2(self, player, guess):
        text, solved = [], False
        if self.game.make_guess(guess):
            solved = True
            self.reward(player)
            text.extend(["The cow takes a step forward. This time you stand your ground, cool and confident.",
                         "The cow leans forward and licks your palm.",
                         "Looking down you see a giant golden key in your hand. What could this be for?",
                         "",
                         "After a few seconds you look up to find the cow, unsurprisingly, gone.",
                         ""])
        else:
            if len(guess) != len(self.game.answer):  # Wrong number of letters, can't really play
                text.extend(["The cow looks at you imploringly. Perhaps something about your guess does not allow her "
                             "to give feedback",
                             ""])
            else:  # Play a round
                text.extend(self.incorrect_guess_feedback(guess))

        return solved, text

    # def encounter2(self, player, autoWin):
    # 	if not autoWin:
    # 		print "The cow stands before you again"
    # 		print "You scan the ground for another set of instructions but see none."
    #
    # 		decided = False
    # 		while not decided:
    # 			playGame = raw_input("Do you attempt to speak to the cow? (y/n)? ")
    # 			print ""
    #
    # 			if playGame == "y":
    # 				print "\"Let's dance you and I.\" you cackle."
    # 				print "You look at the cow, hoping your witty banter has thrown it off guard."
    # 				print "The cow blinks 6 times and then simply stares at you."
    # 				print "Only midly unnerved you decide it's time to begin guessing."
    # 				self.game.play(player)
    #
    # 				print "The cow takes a step forward. This time you stand your ground, cool and confident."
    # 				print "The cow leans forward and licks your palm."
    # 				print "Looking down you see a giant golden key in your hand. What could this be for?"
    # 				print ""
    # 				print "After a few seconds you look up to find the cow, unsurprisingly, gone."
    # 				print ""
    # 				decided = True
    #
    # 			elif playGame == "n":
    # 				print "You're not sure if this is some kind of joke, but talking to a cow doesn't seem like a productive use of your time."
    # 				print ""
    # 				decided = True
    #
    # 			else:
    # 				print "Please answer yes or no (y/n)."
    # 				print ""
    #
    # 	# autowin goes here
    # 	if autoWin or self.game.won:
    # 		player.largeKeys += 1
    # 		player.audumbla_wins += 1
    #
    #
    # def encounter3(self, player, autoWin):
    # 	if not autoWin:
    # 		print "The cow stands before you. You both know what is expected."
    #
    # 		decided = False
    # 		while not decided:
    # 			playGame = raw_input("Do you attempt to aid the cow again? (y/n)? ")
    # 			print ""
    #
    # 			if playGame == "y":
    # 				print "The cow blinks %d times. It has begun." % (len(self.game.answer))
    # 				print ""
    # 				self.game.play(player)
    #
    # 				print "The cow leans forward and deposits a silver key in your hand."
    # 				print "You feel like the gesture has a little more affection in it than before. But maybe you're just getting lonely."
    # 				print ""
    # 				decided = True
    #
    # 			elif playGame == "n":
    # 				print "You don't have time play this game again, there is too much left unexplored!"
    # 				print ""
    # 				decided = True
    #
    # 			else:
    # 				print "Please answer yes or no (y/n)."
    # 				print ""
    #
    # 	# autowin goes here
    # 	if autoWin or self.game.won:
    # 		player.smallKeys += 1
    # 		player.audumbla_wins += 1
    #
    #
    # def encounter4(self, player, autoWin):
    # 	if not autoWin:
    # 		print "The cow stands before you. You both know what is expected."
    #
    # 		decided = False
    # 		while not decided:
    # 			playGame = raw_input("Do you attempt to aid the cow again? (y/n)? ")
    # 			print ""
    #
    # 			if playGame == "y":
    # 				print "The cow blinks %d times. It has begun." % (len(self.game.answer))
    # 				print ""
    # 				self.game.play(player)
    #
    # 				print "The cow leans forward and deposits a silver key in your hand."
    # 				print "You feel like the gesture has a little more affection in it than before. But maybe you're just getting lonely."
    # 				print ""
    # 				decided = True
    #
    # 			elif playGame == "n":
    # 				print "You don't have time play this game again, there is too much left unexplored!"
    # 				print ""
    # 				decided = True
    #
    # 			else:
    # 				print "Please answer yes or no (y/n)."
    # 				print ""
    #
    # 	# autowin goes here
    # 	if autoWin or self.game.won:
    # 		player.smallKeys += 1
    # 		player.audumbla_wins += 1
    #
    #
    # def encounter5(self, player, autoWin):
    # 	if not autoWin:
    # 		print "The cow stands before you. You both know what is expected."
    #
    # 		decided = False
    # 		while not decided:
    # 			playGame = raw_input("Do you attempt to aid the cow again? (y/n)? ")
    # 			print ""
    #
    # 			if playGame == "y":
    # 				print "The cow blinks %d times. It has begun." % (len(self.game.answer))
    # 				print ""
    # 				self.game.play(player)
    # 				print "You hope this awfully numbery word is not a prelude of things to come..."
    # 				print "But you take the key the cow offers you, happy to find it is of the golden variety."
    # 				print ""
    # 				decided = True
    #
    # 			elif playGame == "n":
    # 				print "You don't have time play this game again, there is too much left unexplored!"
    # 				print ""
    # 				decided = True
    #
    # 			else:
    # 				print "Please answer yes or no (y/n)."
    # 				print ""
    #
    # 	# autowin goes here
    # 	if autoWin or self.game.won:
    # 		player.largeKeys += 1
    # 		player.audumbla_wins += 1
    #
    #
    # def encounter6(self, player, autoWin):
    # 	if not autoWin:
    # 		print "The cow stands before you. You both know what is expected."
    #
    # 		decided = False
    # 		while not decided:
    # 			playGame = raw_input("Do you attempt to aid the cow again? (y/n)? ")
    # 			print ""
    #
    # 			if playGame == "y":
    # 				print "The cow blinks %d times. It has begun." % (len(self.game.answer))
    # 				print ""
    # 				self.game.play(player)
    # 				print "The cow deposits a silver key in your hand."
    # 				print ""
    # 				decided = True
    #
    # 			elif playGame == "n":
    # 				print "You don't have time play this game again, there is too much left unexplored!"
    # 				print ""
    # 				decided = True
    #
    # 			else:
    # 				print "Please answer yes or no (y/n)."
    # 				print ""
    #
    # 	# autowin goes here
    # 	if autoWin or self.game.won:
    # 		player.smallKeys += 1
    # 		player.audumbla_wins += 1
    #
    #
    # def encounter7(self, player, autoWin):
    # 	if not autoWin:
    # 		print "The cow stands before you. You both know what is expected."
    #
    # 		decided = False
    # 		while not decided:
    # 			playGame = raw_input("Do you attempt to aid the cow again? (y/n)? ")
    # 			print ""
    #
    # 			if playGame == "y":
    # 				print "The cow blinks %d times. It has begun." % (len(self.game.answer))
    # 				print ""
    # 				self.game.play(player)
    # 				print "The cow deposits a silver key in your hand."
    # 				print ""
    # 				decided = True
    #
    # 			elif playGame == "n":
    # 				print "You don't have time play this game again, there is too much left unexplored!"
    # 				print ""
    # 				decided = True
    #
    # 			else:
    # 				print "Please answer yes or no (y/n)."
    # 				print ""
    #
    # 	# autowin goes here
    # 	if autoWin or self.game.won:
    # 		player.smallKeys += 1
    # 		player.audumbla_wins += 1
    #
    #
    # def encounter8(self, player, autoWin):
    # 	if not autoWin:
    # 		print "The cow stands before you. You both know what is expected."
    #
    # 		decided = False
    # 		while not decided:
    # 			playGame = raw_input("Do you attempt to aid the cow again? (y/n)? ")
    # 			print ""
    #
    # 			if playGame == "y":
    # 				print "The cow blinks %d times. It has begun." % (len(self.game.answer))
    # 				print ""
    # 				self.game.play(player)
    # 				print "The cow deposits a silver key in your hand."
    # 				print ""
    # 				decided = True
    #
    # 			elif playGame == "n":
    # 				print "You don't have time play this game again, there is too much left unexplored!"
    # 				print ""
    # 				decided = True
    #
    # 			else:
    # 				print "Please answer yes or no (y/n)."
    # 				print ""
    #
    # 	# autowin goes here
    # 	if autoWin or self.game.won:
    # 		player.smallKeys += 1
    # 		player.audumbla_wins += 1
    #
    #
    # def encounter9(self, player, autoWin):
    # 	if not autoWin:
    # 		print "The cow stands before you. You both know what is expected."
    #
    # 		decided = False
    # 		while not decided:
    # 			playGame = raw_input("Do you attempt to aid the cow again? (y/n)? ")
    # 			print ""
    #
    # 			if playGame == "y":
    # 				print "The cow blinks %d times. It has begun." % (len(self.game.answer))
    # 				print ""
    # 				self.game.play(player)
    # 				print "The cow deposits a silver key in your hand."
    # 				print ""
    # 				decided = True
    #
    # 			elif playGame == "n":
    # 				print "You don't have time play this game again, there is too much left unexplored!"
    # 				print ""
    # 				decided = True
    #
    # 			else:
    # 				print "Please answer yes or no (y/n)."
    # 				print ""
    #
    # 	# autowin goes here
    # 	if autoWin or self.game.won:
    # 		player.smallKeys += 1
    # 		player.audumbla_wins += 1
    #
    #
    # def encounter10(self, player, autoWin):
    # 	if not autoWin:
    # 		print "The cow stands before you. You both know what is expected."
    #
    # 		decided = False
    # 		while not decided:
    # 			playGame = raw_input("Do you attempt to aid the cow again? (y/n)? ")
    # 			print ""
    #
    # 			if playGame == "y":
    # 				print "The cow blinks %d times. It has begun." % (len(self.game.answer))
    # 				print ""
    # 				self.game.play(player)
    # 				print "The cow deposits a silver key in your hand."
    # 				print ""
    # 				decided = True
    #
    # 			elif playGame == "n":
    # 				print "You don't have time play this game again, there is too much left unexplored!"
    # 				print ""
    # 				decided = True
    #
    # 			else:
    # 				print "Please answer yes or no (y/n)."
    # 				print ""
    #
    # 	# autowin goes here
    # 	if autoWin or self.game.won:
    # 		player.smallKeys += 1
    # 		player.audumbla_wins += 1
    #
    #
    # def encounter11(self, player, autoWin):
    # 	if not autoWin:
    # 		print "The cow stands before you. You both know what is expected."
    #
    # 		decided = False
    # 		while not decided:
    # 			playGame = raw_input("Do you attempt to aid the cow again? (y/n)? ")
    # 			print ""
    #
    # 			if playGame == "y":
    # 				print "The cow blinks %d times. It has begun." % (len(self.game.answer))
    # 				print ""
    # 				self.game.play(player)
    # 				print "The cow deposits a silver key in your hand."
    # 				print ""
    # 				decided = True
    #
    # 			elif playGame == "n":
    # 				print "You don't have time play this game again, there is too much left unexplored!"
    # 				print ""
    # 				decided = True
    #
    # 			else:
    # 				print "Please answer yes or no (y/n)."
    # 				print ""
    #
    # 	# autowin goes here
    # 	if autoWin or self.game.won:
    # 		player.smallKeys += 1
    # 		player.audumbla_wins += 1
    #
    #
    # def encounter12(self, player, autoWin):
    # 	if not autoWin:
    # 		print "The cow stands before you. You both know what is expected."
    #
    # 		decided = False
    # 		while not decided:
    # 			playGame = raw_input("Do you attempt to aid the cow again? (y/n)? ")
    # 			print ""
    #
    # 			if playGame == "y":
    # 				print "The cow blinks %d times. It has begun." % (len(self.game.answer))
    # 				print ""
    # 				self.game.play(player)
    # 				print "The cow deposits a silver key in your hand."
    # 				print ""
    # 				decided = True
    #
    # 			elif playGame == "n":
    # 				print "You don't have time play this game again, there is too much left unexplored!"
    # 				print ""
    # 				decided = True
    #
    # 			else:
    # 				print "Please answer yes or no (y/n)."
    # 				print ""
    #
    # 	# autowin goes here
    # 	if autoWin or self.game.won:
    # 		player.smallKeys += 1
    # 		player.audumbla_wins += 1
    #
    #
    # def encounter13(self, player, autoWin):
    # 	if not autoWin:
    # 		print "The cow stands before you. You both know what is expected."
    #
    # 		decided = False
    # 		while not decided:
    # 			playGame = raw_input("Do you attempt to aid the cow again? (y/n)? ")
    # 			print ""
    #
    # 			if playGame == "y":
    # 				print "The cow blinks %d times. It has begun." % (len(self.game.answer))
    # 				print ""
    # 				self.game.play(player)
    # 				print "The cow deposits a golden key in your hand."
    # 				print ""
    # 				decided = True
    #
    # 			elif playGame == "n":
    # 				print "You don't have time play this game again, there is too much left unexplored!"
    # 				print ""
    # 				decided = True
    #
    # 			else:
    # 				print "Please answer yes or no (y/n)."
    # 				print ""
    #
    # 	# autowin goes here
    # 	if autoWin or self.game.won:
    # 		player.largeKeys += 1
    # 		player.audumbla_wins += 1
    #
    #
    # def encounter14(self, player, autoWin):
    # 	if not autoWin:
    # 		print "The cow stands before you. You both know what is expected."
    #
    # 		decided = False
    # 		while not decided:
    # 			playGame = raw_input("Do you attempt to aid the cow again? (y/n)? ")
    # 			print ""
    #
    # 			if playGame == "y":
    # 				print "The cow blinks %d times. It has begun." % (len(self.game.answer))
    # 				print ""
    # 				self.game.play(player)
    # 				print "The cow deposits a silver key in your hand."
    # 				print ""
    # 				decided = True
    #
    # 			elif playGame == "n":
    # 				print "You don't have time play this game again, there is too much left unexplored!"
    # 				print ""
    # 				decided = True
    #
    # 			else:
    # 				print "Please answer yes or no (y/n)."
    # 				print ""
    #
    # 	# autowin goes here
    # 	if autoWin or self.game.won:
    # 		player.smallKeys += 1
    # 		player.audumbla_wins += 1
    #
    #
    # def encounter15(self, player, autoWin):
    # 	if not autoWin:
    # 		print "The cow stands before you. You both know what is expected."
    #
    # 		decided = False
    # 		while not decided:
    # 			playGame = raw_input("Do you attempt to aid the cow again? (y/n)? ")
    # 			print ""
    #
    # 			if playGame == "y":
    # 				print "The cow blinks %d times. It has begun." % (len(self.game.answer))
    # 				print ""
    # 				self.game.play(player)
    # 				print "The cow deposits a golden key in your hand."
    # 				print ""
    # 				decided = True
    #
    # 			elif playGame == "n":
    # 				print "You don't have time play this game again, there is too much left unexplored!"
    # 				print ""
    # 				decided = True
    #
    # 			else:
    # 				print "Please answer yes or no (y/n)."
    # 				print ""
    #
    # 	# autowin goes here
    # 	if autoWin or self.game.won:
    # 		player.largeKeys += 1
    # 		player.audumbla_wins += 1
