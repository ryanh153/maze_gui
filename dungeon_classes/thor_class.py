from dungeon_classes.base_creature_class import BaseCreature


class Thor(BaseCreature):

    def interact(self, player, guess=None):
        # floor 1
        if player.thor_wins == 0:
            if self.started_game:
                return self.play_encounter1(player, guess)
            else:
                return self.begin_encounter1()
        elif player.thor_wins == 1:
            if self.started_game:
                return self.play_encounter2(player, guess)
            else:
                return self.begin_encounter2()
        # ### floor 2
        # elif player.thor_wins == 2:
        #     self.encounter3(player, auto_win)
        # elif player.thor_wins == 3:
        #     self.encounter4(player, auto_win)
        # elif player.thor_wins == 4:
        #     self.encounter5(player, auto_win)
        # ### final floor
        # elif player.thor_wins == 5:
        #     self.encounter6(player, auto_win)
        # elif player.thor_wins == 6:
        #     self.encounter7(player, auto_win)
        # elif player.thor_wins == 7:
        #     self.encounter8(player, auto_win)
        # elif player.thor_wins == 8:
        #     self.encounter9(player, auto_win)
        # elif player.thor_wins == 9:
        #     self.encounter10(player, auto_win)
        # elif player.thor_wins == 10:
        #     self.encounter11(player, auto_win)
        # elif player.thor_wins == 11:
        #     self.encounter12(player, auto_win)
        # elif player.thor_wins == 12:
        #     self.encounter13(player, auto_win)
        # elif player.thor_wins == 13:
        #     self.encounter14(player, auto_win)
        # elif player.thor_wins == 14:
        #     self.encounter15(player, auto_win)

        else:
            raise ValueError("Not coded!")

    def begin_encounter1(self):
        self.current_text = ["You, brave explorer, are the only one who can hope to solve this intricate and devious "
                             "puzzle.",
                             "In what order will you place the tiles?",
                             '']

        text = ["In the room you large confused looking man.",
                "He wields a large hammer and you can see he has been using it on the walls, but to little avail.",
                "\"What do you mean!\" He wails pathetically.",
                "\"I, Thor the mighty, have wandered the maze for hours and can find no way out. All I've found "
                "besides walls and locked doors lie in this room.",
                "On the floor in front of him lie a row of stone tiles.",
                "They spell \"%s\", but that doesn't make much sense." % self.game.scrambled,
                "On the wall above the tiles are a number of square holes. There are the same number of holes as "
                "tiles.",
                "\"I put the tiles in the holes but they just fall back out again! It's impossible!\" Thor "
                "screams angrily.",
                "Enter 'solve puzzle' to attempt to help the poor man.",
                ""]

        return text

    def play_encounter1(self, player, guess):
        text, solved = [], False
        if self.game.make_guess(guess):
            solved = True
            self.encounter1_reward(player)
            text.extend(["Thor stares at you dumbfounded.",
                         "\"But that's the same thing I did! And I pushed on the tiles ten times harder to make them "
                         "stay in place!\"",
                         "\"It's... it's the order of the tiles\" you say. It's amazing to you that this information "
                         "needs to be conveyed still.",
                         "They are supposed to spell \"%s\"." % self.game.answer,
                         "\"So that's the secret!\" Leaping forward Thor grabs the tiles in order puts them in the "
                         "corresponding squares.",
                         "You note that he is still making sure to shove them in at least ten times harder than you "
                         "did, just to be safe.",
                         "The panel opens again and Thor gleefully reaches in and grabs the key.",
                         "\"I will conquer this devilish maze after all! Nothing can stop the almighty!\"",
                         "He runs off to the east, too quickly for you to follow.",
                         "Shaking your head at the hubris of the \"almighty\" you turn back to the tiles to see if "
                         "perhaps you might be able earn a second key",
                         "Placing them again does indeed open the panel, but there is no key this time. Somehow it "
                         "remembers you have already taken from it.",
                         "Shrugging you pocket your new key.",
                         ''])
        else:
            text.extend(["The tiles fall back onto the floor, amazingly into the same order the were originally.",
                         ''])
        return solved, text

    def encounter1_reward(self, player):
        self.started_game = False
        player.small_keys += 1
        player.thor_wins += 1

    def begin_encounter2(self):
        self.current_text = ["You kneel down next to Thor. \"How's it going buddy?\" you gently inquire.",
                             "\"Not well...\" he reluctantly admits.",
                             "\"I can't figure out what to do with the tiles. And they've grown in number!\"",
                             "Looking down you see he is correct. Tiles are spread across the floor spelling %s" % self.game.scrambled,
                             "\"Loki even said he'd help me out.\" Thor mutters. \"But his hint didn't make any "
                             "sense.\"",
                             "\"He said I was the answer, but when I spell my name there are still two tiles left!\"",
                             "\"Perhaps you can help me again?\"",
                             '']

        text = ["You see Thor again. He lies on the ground on his side. He is not looking happy...",
                '"Do you attempt to help this poor man (solve puzzle)?"',
                '']
        return text

    def play_encounter2(self, player, guess):

        text, solved = [], False
        if self.game.make_guess(guess):
            solved = True
            self.encounter2_reward(player)
            text.extend(["A small panel opens next to you revealing a large golden key."
                         "You hastily grab it. Its golden allure is overpowering."
                         ""
                         "\"Aha!\" He shouts. So Loki said I was the answer, but it was he, my brother, who was the "
                         "answer.\" "
                         "\"Such devlish tricks\""
                         "Shaking your head you decide not to stay and see if he can figure out how to spell out the "
                         "word again. "
                         ""])

        else:
            text.extend(["The tiles fall back onto the floor, amazingly into the same order the were originally.",
                         ''])

        return solved, text

    def encounter2_reward(self, player):
        self.started_game = False
        player.large_keys += 1
        player.thor_wins += 1
#
# def encounter3(self, player, auto_win):
# 	if not auto_win:
# 		print "Thor stands in the room, a tile in each hand. Looking at his face you see his brow is furrowed in frustration."
# 		print "\"The puzzles have gotten harder\" he states simply."
# 		print "\"I don't think even you can solve this one. It must have been put here as a punishment to me for using the help of a mere mortal.\""
# 		print "Sighing, Thor tosses the two pieces in his hands aside. \"You may as well try though\" he says with a shrug."
#
# 		decided = False
# 		while not decided:
# 			playGame = raw_input("Do you try to solve the puzzle despite the amount of shade in the dark dungeon (y/n)? ")
# 			print ""
#
# 			if playGame == "y":
# 				print "Scrambled: %s" % (self.game.scrambled)
# 				self.game.play(player)
#
# 				print "A door slides back to reveal a large, golden key."
# 				print "You both stare at in in awe, marveling at its beauty."
# 				print "As you take it from its hole in the wall you notice Thor seems to be regarding you with more respect than usual."
# 				print "Puffing out your chest slightly you turn to him \"No puzzle is too hard for me\" you state calmly."
# 				print "You turn and leave the room. Resisting the strong urge to look back and see his reaction."
# 				print ""
# 				decided = True
#
# 			elif playGame == "n":
# 				print "Maybe if you come back later Thor will learn to appreciate your help...but you doubt it."
# 				print ""
# 				decided = True
#
# 			else:
# 				print "Please answer yes or no (y/n)."
# 				print ""
#
# 	# auto_win goes here
# 	if auto_win or self.game.won:
# 		player.largeKeys += 1
# 		player.thor_wins += 1
#
# def encounter4(self, player, auto_win):
# 	if not auto_win:
# 		print "Thor stands in the center of the room. A smile on his face and large grin on his face seem out of place at this point."
# 		print "\"I solved this on one my own!\" he annonces proudly. \"There were so many possible solutions, but I picked the correct one."
# 		print "\"I stuck around though to see if you could match my mighty feat.\""
# 		print "With a non-negligable amount doubt in your mind you consider whether or not to give the man what he's waited for. What if you can't solve it?"
#
# 		decided = False
# 		while not decided:
# 			playGame = raw_input("Do you attempt to solve the puzzle (y/n)? ")
# 			print ""
#
# 			if playGame == "y":
# 				print "Scrambled: %s" % (self.game.scrambled)
# 				self.game.play(player)
#
# 				print "The panel opens as expected and you pocket a silver key."
# 				print "Before leaving however you turn to Thor."
# 				print "\"Did you actually solve the puzzle? I didn't think so at first but that talk of 'so many solutions' is making me think I was wrong.\""
# 				print "\"Of course I did! I gave you that...clue as a hint. Yes, it was brilliant was it not?\""
# 				print "\"It was if you did it on purpose. But I guess you wouldn't have said it unless you knew plethora meant 'begins with p' right?\""
# 				print "\"Oh absolutely. I'm just glad I was able to help you after everything you've done for me. I guess we're even now.\""
# 				print "Smiling, you shake your head. \"Sure buddy, I'll see you at the next one.\""
# 				print ""
# 				decided = True
#
# 			elif playGame == "n":
# 				print "Best not you decide. If you can't figure out the puzzle you're sure you would never hear the end of it."
# 				print ""
# 				decided = True
#
# 			else:
# 				print "Please answer yes or no (y/n)."
# 				print ""
#
# 	# auto_win goes here
# 	if auto_win or self.game.won:
# 		player.smallKeys += 1
# 		player.thor_wins += 1
#
# def encounter5(self, player, auto_win):
# 	if not auto_win:
# 		print "You enter a room with tiles scattered across the floor."
# 		print "You look around for the large figure you know must be in one of the corners."
# 		print "Instead all you see is a small not tucked into a square where the tiles go."
# 		print "Well, tucked may be the wrong word. As you approach you notice the paper has been is heavily creased."
# 		print "Clearly it took a few times to get it to stay."
# 		print "You chuckle at the image of Thor screaming at the small slip of parchement as it falls to the floor over and over."
# 		print "Still smiling, you pick up the note and read"
# 		print "'Dear... explorer. I have been called away to aid in a dangerous conflict in a realm you cannot imagine."
# 		print "Unfortunately this means I can no longer aid in you in this dungeon."
# 		print "However I will let you know that you have proved nearly and equal to me, at least in mental endevours."
# 		print "As a token of friendship I will tell you that this word is not a plethora, and wish you luck. Thor'"
# 		print "Looking down at the tiles you see there is not a single 'p'."
# 		print "Not exactly a useful hint, but you're mildly impressed that he remembered what you said at all."
#
# 		decided = False
# 		while not decided:
# 			playGame = raw_input("Do solve the puzzle in memory? You know he would be here if there was not another matter of the gravest importance (y/n). ")
# 			print ""
#
# 			if playGame == "y":
# 				print "Scrambled: %s" % (self.game.scrambled)
# 				self.game.play(player)
#
# 				print "You are rewarded with a silver key."
# 				print "It's not quite the same on your own, but at least you know you did it."
# 				print ""
# 				decided = True
#
# 			elif playGame == "n":
# 				print "Maybe later, this wound is still too fresh."
# 				print ""
# 				decided = True
#
# 			else:
# 				print "Please answer yes or no (y/n)."
# 				print ""
#
# 	# auto_win goes here
# 	if auto_win or self.game.won:
# 		player.smallKeys += 1
# 		player.thor_wins += 1
#
#
# def encounter6(self, player, auto_win):
# 	if not auto_win:
# 		print "You enter a room with tiles scattered across the floor."
#
# 		decided = False
# 		while not decided:
# 			playGame = raw_input("Do solve attempt to unscramble them? (y/n). ")
# 			print ""
#
# 			if playGame == "y":
# 				print "Scrambled: %s" % (self.game.scrambled)
# 				self.game.play(player)
#
# 				print "You are rewarded with a silver key."
# 				print ""
# 				decided = True
#
# 			elif playGame == "n":
# 				print "You probably don't need to solve this one..."
# 				print ""
# 				decided = True
#
# 			else:
# 				print "Please answer yes or no (y/n)."
# 				print ""
#
# 	# auto_win goes here
# 	if auto_win or self.game.won:
# 		player.smallKeys += 1
# 		player.thor_wins += 1
#
#
# def encounter7(self, player, auto_win):
# 	if not auto_win:
# 		print "You enter a room with tiles scattered across the floor."
#
# 		decided = False
# 		while not decided:
# 			playGame = raw_input("Do solve attempt to unscramble them? (y/n). ")
# 			print ""
#
# 			if playGame == "y":
# 				print "Scrambled: %s" % (self.game.scrambled)
# 				self.game.play(player)
#
# 				print "You are rewarded with a silver key."
# 				print ""
# 				decided = True
#
# 			elif playGame == "n":
# 				print "You probably don't need to solve this one..."
# 				print ""
# 				decided = True
#
# 			else:
# 				print "Please answer yes or no (y/n)."
# 				print ""
#
# 	# auto_win goes here
# 	if auto_win or self.game.won:
# 		player.smallKeys += 1
# 		player.thor_wins += 1
#
#
# def encounter8(self, player, auto_win):
# 	if not auto_win:
# 		print "You enter a room with tiles scattered across the floor."
#
# 		decided = False
# 		while not decided:
# 			playGame = raw_input("Do solve attempt to unscramble them? (y/n). ")
# 			print ""
#
# 			if playGame == "y":
# 				print "Scrambled: %s" % (self.game.scrambled)
# 				self.game.play(player)
#
# 				print "You are rewarded with a large, golden key."
# 				print ""
# 				decided = True
#
# 			elif playGame == "n":
# 				print "You probably don't need to solve this one..."
# 				print ""
# 				decided = True
#
# 			else:
# 				print "Please answer yes or no (y/n)."
# 				print ""
#
# 	# auto_win goes here
# 	if auto_win or self.game.won:
# 		player.largeKeys += 1
# 		player.thor_wins += 1
#
#
# def encounter9(self, player, auto_win):
# 	if not auto_win:
# 		print "You enter a room with tiles scattered across the floor."
#
# 		decided = False
# 		while not decided:
# 			playGame = raw_input("Do solve attempt to unscramble them? (y/n). ")
# 			print ""
#
# 			if playGame == "y":
# 				print "Scrambled: %s" % (self.game.scrambled)
# 				self.game.play(player)
#
# 				print "You are rewarded with a silver key."
# 				print ""
# 				decided = True
#
# 			elif playGame == "n":
# 				print "You probably don't need to solve this one..."
# 				print ""
# 				decided = True
#
# 			else:
# 				print "Please answer yes or no (y/n)."
# 				print ""
#
# 	# auto_win goes here
# 	if auto_win or self.game.won:
# 		player.smallKeys += 1
# 		player.thor_wins += 1
#
#
# def encounter10(self, player, auto_win):
# 	if not auto_win:
# 		print "You enter a room with tiles scattered across the floor."
#
# 		decided = False
# 		while not decided:
# 			playGame = raw_input("Do solve attempt to unscramble them? (y/n). ")
# 			print ""
#
# 			if playGame == "y":
# 				print "Scrambled: %s" % (self.game.scrambled)
# 				self.game.play(player)
#
# 				print "You are rewarded with a silver key."
# 				print ""
# 				decided = True
#
# 			elif playGame == "n":
# 				print "You probably don't need to solve this one..."
# 				print ""
# 				decided = True
#
# 			else:
# 				print "Please answer yes or no (y/n)."
# 				print ""
#
# 	# auto_win goes here
# 	if auto_win or self.game.won:
# 		player.smallKeys += 1
# 		player.thor_wins += 1
#
#
# def encounter11(self, player, auto_win):
# 	if not auto_win:
# 		print "You enter a room with tiles scattered across the floor."
#
# 		decided = False
# 		while not decided:
# 			playGame = raw_input("Do solve attempt to unscramble them? (y/n). ")
# 			print ""
#
# 			if playGame == "y":
# 				print "Scrambled: %s" % (self.game.scrambled)
# 				self.game.play(player)
#
# 				print "You are rewarded with a silver key."
# 				print ""
# 				decided = True
#
# 			elif playGame == "n":
# 				print "You probably don't need to solve this one..."
# 				print ""
# 				decided = True
#
# 			else:
# 				print "Please answer yes or no (y/n)."
# 				print ""
#
# 	# auto_win goes here
# 	if auto_win or self.game.won:
# 		player.smallKeys += 1
# 		player.thor_wins += 1
#
#
# def encounter12(self, player, auto_win):
# 	if not auto_win:
# 		print "You enter a room with tiles scattered across the floor."
#
# 		decided = False
# 		while not decided:
# 			playGame = raw_input("Do solve attempt to unscramble them? (y/n). ")
# 			print ""
#
# 			if playGame == "y":
# 				print "Scrambled: %s" % (self.game.scrambled)
# 				self.game.play(player)
#
# 				print "You are rewarded with a silver key."
# 				print ""
# 				decided = True
#
# 			elif playGame == "n":
# 				print "You probably don't need to solve this one..."
# 				print ""
# 				decided = True
#
# 			else:
# 				print "Please answer yes or no (y/n)."
# 				print ""
#
# 	# auto_win goes here
# 	if auto_win or self.game.won:
# 		player.smallKeys += 1
# 		player.thor_wins += 1
#
#
# def encounter13(self, player, auto_win):
# 	if not auto_win:
# 		print "You enter a room with tiles scattered across the floor."
#
# 		decided = False
# 		while not decided:
# 			playGame = raw_input("Do solve attempt to unscramble them? (y/n). ")
# 			print ""
#
# 			if playGame == "y":
# 				print "Scrambled: %s" % (self.game.scrambled)
# 				self.game.play(player)
#
# 				print "You are rewarded with a silver key."
# 				print ""
# 				decided = True
#
# 			elif playGame == "n":
# 				print "You probably don't need to solve this one..."
# 				print ""
# 				decided = True
#
# 			else:
# 				print "Please answer yes or no (y/n)."
# 				print ""
#
# 	# auto_win goes here
# 	if auto_win or self.game.won:
# 		player.smallKeys += 1
# 		player.thor_wins += 1
#
#
# def encounter14(self, player, auto_win):
# 	if not auto_win:
# 		print "You enter a room with tiles scattered across the floor."
#
# 		decided = False
# 		while not decided:
# 			playGame = raw_input("Do solve attempt to unscramble them? (y/n). ")
# 			print ""
#
# 			if playGame == "y":
# 				print "Scrambled: %s" % (self.game.scrambled)
# 				self.game.play(player)
#
# 				print "You are rewarded with a silver key."
# 				print ""
# 				decided = True
#
# 			elif playGame == "n":
# 				print "You probably don't need to solve this one..."
# 				print ""
# 				decided = True
#
# 			else:
# 				print "Please answer yes or no (y/n)."
# 				print ""
#
# 	# auto_win goes here
# 	if auto_win or self.game.won:
# 		player.smallKeys += 1
# 		player.thor_wins += 1
#
#
# def encounter15(self, player, auto_win):
# 	if not auto_win:
# 		print "You enter a room with tiles scattered across the floor."
#
# 		decided = False
# 		while not decided:
# 			playGame = raw_input("Do solve attempt to unscramble them? (y/n). ")
# 			print ""
#
# 			if playGame == "y":
# 				print "Scrambled: %s" % (self.game.scrambled)
# 				self.game.play(player)
#
# 				print "You are rewarded with a large, golden key."
# 				print ""
# 				decided = True
#
# 			elif playGame == "n":
# 				print "You probably don't need to solve this one..."
# 				print ""
# 				decided = True
#
# 			else:
# 				print "Please answer yes or no (y/n)."
# 				print ""
#
# 	# auto_win goes here
# 	if auto_win or self.game.won:
# 		player.largeKeys += 1
# 		player.thor_wins += 1
