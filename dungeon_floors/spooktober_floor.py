import services.level_service as maze_funcs
from dungeon_classes.tile_class import Tile
from dungeon_classes.dungeon_class import Dungeon
from dungeon_classes.player_class import Player

from dungeon_classes.thor_class import Thor
from dungeon_classes.word_scramble_class import WordScramble

from dungeon_classes.bull_cow_class import BCGame
from dungeon_classes.audumbla_class import Audumbla

TILE_SIZE = 75


def make_map():
    player_pos = [1, 7]
    goal_pos_arr = [[1, 8]]
    start_pos_arr = [player_pos]
    passphrases = [None]

    floor_map = [[Tile() for _ in range(16)] for _ in range(11)]
    paths = [['', '', '', 's', 'es', 'sw', 'e', 'sw', 'es', 'ew', 'ew', 'ew', 'w', '', '', ''],
             ['', '', 'es', 'nw', 'ns', 'ns', 's', 'ns', 'n', 'es', 'ew', 'ew', 'ew', 'sw', '', ''],
             ['', 'es', 'nw', 'es', 'nw', 'ne', 'nw', 'n', 's', 'ne', 'ew', 'ew', 'w', 'ns', 's', ''],
             ['es', 'nsw', 'e', 'nsw', '', '', 's', 'e', 'new', 'sw', '', '', 'es', 'nsw', 'nes', 'w'],
             ['ns', 'ne', 'w', 'ns', '', '', 'ns', 'e', 'sw', 'ns', '', '', 'n', 'n', 'ne', 'sw'],
             ['ne', 'ew', 'w', 'n', 'e', 'sw', 'ne', 'ew', 'nw', 'ns', 'es', 'ew', 'ew', 'ew', 'ew', 'nsw'],
             ['es', 'ew', 'w', 's', 'es', 'nw', 'e', 'ew', 'ew', 'new', 'nw', 'es', 'w', 'es', 'w', 'ns'],
             ['ne', 'esw', 'w', 'ns', 'ns', '', '', '', '', '', '', 'nes', 'ew', 'nsw', 'es', 'nw'],
             ['', 'ne', 'sw', 'ns', 'ne', 'w', '', '', '', '', 'e', 'nw', 's', 'ns', 'n', ''],
             ['', '', 'ne', 'nw', 's', 's', 's', 's', '', 'e', 'ew', 'ew', 'nesw', 'nw', '', ''],
             ['', '', '', 'n', 'ne', 'nw', 'ne', 'nw', 'e', 'ew', 'ew', 'w', 'n', '', '', '']]
    paths.reverse()  # since we index from bottom

    for r, row in enumerate(paths):
        for c, path_str in enumerate(row):
            floor_map[r][c].add_paths([d for d in path_str])

    # spawn doors
    wood = [(0, 11, 'e'), (4, 3, 'n'), (4, 13, 'n'), (5, 3, 'w'), (5, 3, 'e'), (5, 13, 'n'), (7, 6, 'e'), (9, 8, 'e')]
    gold = [(1, 3, 'e'), (1, 5, 'e'), (7, 7, 'n'), (9, 6, 'n')]
    for r, c, d in wood:
        floor_map[r][c].spawn_door(d, 'w')
    for r, c, d in gold:
        floor_map[r][c].spawn_door(d, 'g')
    maze_funcs.make_doors_2_sided(floor_map)

    # add special text
    floor_map[1][7].special_text = ["Upon entering the room you are immediately enraptured by the ominously effulgent "
                                    "door on "
                                    "the far side of the chamber. It fills an entire wall and is made only of "
                                    "ivory and gold with the exception of an ebony raven at its center. Above the "
                                    "raven in the same flowing script as on the tiles you have collected are the "
                                    "words \"What is my name?\" Below the raven are five empty slots in which you may "
                                    "place tiles. If you have all the tiles you may enter the order in which you wish "
                                    "to place them. Otherwise your journey is not over yet.", '']

    floor_map[8][8].special_text = ["You are acutely aware of the singularly constricting nature of the space you are "
                                    "in. Its grotesquely and insipidly blanks walls pulse and pound around you "
                                    "creating an inescapable "
                                    "and altogether unholy urgency for escape within you.", ""]

    floor_map[8][14].special_text = ["A more cacophonous confinement you have never found yourself in. The walls "
                                     "reverberate with a "
                                     "palpably persistent pounding and the air itself is pregnant with a"
                                     " preternaturally dark and "
                                     "prehistoric terror so consuming that now to still the beating of your heart "
                                     "you stand repeating \"Tis some visitor entreating entrance at my dungeon door. "
                                     "Some apocryphal creature that hath never been seen by man before, and will bother"
                                     " me nevermore.\" "
                                     "After an eternal confinement in this claustrophobic state and enumerable "
                                     "repetitions of this morbid mantra your heartbeat "
                                     "begins to return to a more nominal rhythm. As this transpires the beating of "
                                     "the room ebbs as "
                                     "well until it resumes an appearance and character more like the rest of the "
                                     "dungeon. After "
                                     "relegating the experience to being a mere reflection of your own nervous "
                                     "nature "
                                     "you deem it best not to dwell on the event and consign the debate over "
                                     "whether the experience was wholly within the confines of the waking world to a "
                                     "time and place "
                                     "where such academic questions may be pursued at a more languid pace."]

    floor_map[10][6].special_text = ["Well this is just ridiculous.", '']  # second golden door in like 3 tiles

    # Creatures

    # set up common text fields
    scramble_main_text = ["Enter the letters in the correct order or enter 'exit' to stop playing.", '']
    scramble_fail_text = ["The tiles spontaneously throw themselves into the same jumbled pile they were in when you "
                          "entered the room. "
                          "Perhaps that wasn't correct..",
                          '']
    scramble_post_template = ["The tiles glow with an eerie light that steadily grows until it nearly blinds you. You "
                              "raise your hands to shield your eyes but after a few seconds the unexplained "
                              "brilliance fades.",
                              '',  # replace this with the reward specific text
                              "You pick up the key and put it in your pocket. It may be useful soon.",
                              '']

    bc_post_template = ["Cowthulhu bows its head and licks your hand.",
                        'As its tongue pulls away you you feel a familiar shape in your palm.',
                        '']

    solutions = ['ghastly', 'morbid', 'odious', 'ebony', 'spectral', 'ominous', 'debauch', 'atrocity', 'effulgent',
                 'impunity', 'phantasm', 'sepulchre', 'immolation', 'plutonian', 'malodorous', 'pestilence',
                 'sagacious', 'masquerade']

    solutions = iter(solutions)

    pos = [6, 6]
    solution = next(solutions)  # ghastly
    game = WordScramble(solution)
    reward = 'small'
    scramble_pre_text1 = ["As you enter the room a feeling of decay seeps into you. Looking around you see "
                          "that even the walls seem to be rotten and putrescent. Some of the bricks that "
                          "make "
                          "up the chamber have even fallen out and lie strewn across the floor. Upon "
                          "closer inspection you realize that some of these bricks are not the normal blank "
                          "masonry that makes up the dungeon. Instead they display faint but indelible markings. "
                          "Closer "
                          "inspection reveal them to be the outlines of letters. Maybe if you "
                          "place them back in the "
                          "wall in the correct order they will give you some clue as to the origin of your current "
                          "confinement (solve puzzle).", '']
    scramble_post_text1 = scramble_post_template[0:-3] + ["On the ground in front of you is a small silver key."] + \
                          scramble_post_template[-2::]
    floor_map[pos[0]][pos[1]].spawn_creature(Thor(pos, game, scramble_pre_text1, scramble_main_text, scramble_fail_text,
                                                  scramble_post_text1, reward))

    pos = [4, 6]
    solution = next(solutions)  # morbid
    game = WordScramble(solution)
    reward = 'small'
    scramble_pre_text2 = ["This small, lugubrious corner of your twisting tomb offers no relief from your restless "
                          "toil. Instead it contains more mysterious labors in the form of a series of scrambled tiles "
                          "in the center of the room. Perhaps solving them will bring you closer to some kind of "
                          "resolution (solve puzzle).", '']
    scramble_post_text2 = scramble_post_template[0:-3] + ["On the ground in front of you is a small silver key."] + \
                          scramble_post_template[-2::]
    floor_map[pos[0]][pos[1]].spawn_creature(Thor(pos, game, scramble_pre_text2, scramble_main_text, scramble_fail_text,
                                                  scramble_post_text2, reward))

    pos = [10, 12]
    solution = next(solutions)  # odious
    game = WordScramble(solution)
    reward = 'large'
    scramble_pre_text3 = ["As you enter the room you feel inundated with waves of unbridled rage that come from all "
                          "sides. The walls themselves pulse with tempestuous fury and a dark red glow hangs in the "
                          "air. Through this you see a set of tiles on the floor and a familiar set of holes in the "
                          "far wall. Do you attempt to use them despite the malignant presence (solve puzzle)?", '']
    scramble_post_text3 = scramble_post_template[0:-3] + ["On the ground in front of you is a glittering golden key."] + \
                          scramble_post_template[-2::]
    floor_map[pos[0]][pos[1]].spawn_creature(Thor(pos, game, scramble_pre_text3, scramble_main_text, scramble_fail_text,
                                                  scramble_post_text3, reward))

    pos = [2, 14]
    solution = next(solutions)  # ebony
    game = WordScramble(solution)
    reward = 'small'
    scramble_pre_text3 = ["You enter a room full of a darkness so deep and complete that you are immediately "
                          "disoriented. Unsure of how the inky void you are in can even be connected to the room "
                          "you just left you are nevertheless determined to find your way through. You lower yourself "
                          "slowly onto your hands and knees. The damp, mossy earth that makes up the floor sends a "
                          "chill through you as you begin to methodically map your surroundings. As you pick your "
                          "way along a winding wall that seems longer than you thought possible you encounter a square "
                          "brick on the floor in front of you. Knowing the familiar shape all to well you "
                          "realize you are in a puzzle room and that the other tiles must also be somewhere "
                          "in the same starless void that envelops you. You continue your exploration of the "
                          "room, eschewing the center and hoping that a sedulous inspection of the outer perimeter "
                          "will yield all the tools you seek. Against all odds this does indeed seem to be the case "
                          "and you encounter one tile after another. Upon collecting what you assume to be the final "
                          "tile a soft ruddy glow begins to shine from a set of small square holes, not in the far "
                          "wall this time, but in the center of the floor. Do you insert your hard won tiles into "
                          "these luminescent pits (solve puzzle)?", '']
    scramble_post_text4 = scramble_post_template[0:-3] + ["On the ground in front of you is a small silver key."] + \
                          scramble_post_template[-2::]
    floor_map[pos[0]][pos[1]].spawn_creature(Thor(pos, game, scramble_pre_text3, scramble_main_text, scramble_fail_text,
                                                  scramble_post_text4, reward))

    pos = [2, 10]
    solution = next(solutions)  # spectral
    game = WordScramble(solution)
    reward = 'small'
    scramble_pre_text5 = ['As you enter this room you are immediately aware of an otherworldly and altogether unholy '
                          'presence. '
                          'Looking around you see nothing of form or substance but are sure that suspended in the '
                          'surrounding ether is an intelligence not of this world. Looking down you see a set '
                          'of jumbled tiles. Do you attempt to use them (solve puzzle)?', '']
    scramble_post_text5 = scramble_post_template[0:-3] + ["On the ground in front of you is a small silver key."] + \
                          scramble_post_template[-2::]
    floor_map[pos[0]][pos[1]].spawn_creature(Thor(pos, game, scramble_pre_text5, scramble_main_text, scramble_fail_text,
                                                  scramble_post_text5, reward))

    pos = [1, 9]
    solution = next(solutions)  # ominous
    game = WordScramble(solution)
    reward = 'H'
    scramble_pre_text6 = ["In this dismal, dreaded passage you encounter a dead end. Sighing you turn around and "
                          "prepare to begin the long trudge back to the last intersection when you hear a barely "
                          "audible click followed by a charnel sound you have only previously heard in "
                          "midnight strolls through abandoned and decrepit graveyards; old masonry falling onto "
                          "worm-eaten earth. "
                          "Turning you see a pile of tiles by the far wall with letters "
                          "on them. Do you try and repair the structure by putting them back into the wall in "
                          "the correct order (solve puzzle)?", '']
    scramble_post_text6 = scramble_post_template[0:-3] + [f"Looking down you see not another key, but another tile, "
                                                          f"this one made of ivory gold. Inscribed on it in a flowing "
                                                          f"script is the letter '{reward}'. You pocket the tile. "
                                                          f"Certainly "
                                                          f"it's purpose will be made clear soon.", ''] + \
                          scramble_post_template[-2::]
    floor_map[pos[0]][pos[1]].spawn_creature(Thor(pos, game, scramble_pre_text6, scramble_main_text, scramble_fail_text,
                                                  scramble_post_text6, reward))

    pos = [10, 4]
    solution = next(solutions)  # debauch
    game = WordScramble(solution)
    reward = 'small'
    scramble_pre_text7 = ['Your senses are immediately assailed by a cataclysm of conflicting smells that induce a '
                          'singularly unpleasant sensation in your stomach. Looking around you see why. The floor and '
                          'walls '
                          'are smeared with the wretched remnants of a thousand days of unrestrained revelry. '
                          'Shattered '
                          'bottles are piled in the corners and enough of their contents has been spilled on the '
                          'floor to more than fill the few unbroken vessels that remain on a squat three legged table '
                          'that stands in the room\'s center. Mixed with this is the end result of the the '
                          'consumption of such copious amounts of drink and food. You try not to think about its '
                          'journey to its current state. Next to '
                          'the bottles though you see the familiar shape '
                          'of stone tiles and know you will likely have to stomach the room and it\'s odorous '
                          'contents long enough to place them. Do you do this now (solve puzzle)?', '']
    scramble_post_text7 = scramble_post_template[0:-3] + ["On the ground in front of you is a small silver key."] + \
                          scramble_post_template[-2::]
    floor_map[pos[0]][pos[1]].spawn_creature(Thor(pos, game, scramble_pre_text7, scramble_main_text, scramble_fail_text,
                                                  scramble_post_text7, reward))

    pos = [7, 2]
    solution = next(solutions)  # atrocity
    game = WordScramble(solution)
    reward = 'Q'
    scramble_pre_text8 = ["Entering yet another room in this sprawling labyrinth you find a dead end. Cursing your "
                          "luck "
                          "and whatever demoniac deity deigned to drudge up such a diabolical damnation you see "
                          "another set of lettered tiles. Do you continue to painstakingly ponder these pernicious "
                          "puzzles (solve puzzle)?", '']
    scramble_post_text8 = scramble_post_template[0:-3] + [f"Looking down you see not another key, but another tile, "
                                                          f"this one made of ivory gold. Inscribed on it in a flowing "
                                                          f"script is the letter '{reward}'. You pocket the tile. "
                                                          f"Certainly "
                                                          f"it's purpose will be made clear soon.", ''] + \
                          scramble_post_template[-2::]
    floor_map[pos[0]][pos[1]].spawn_creature(Thor(pos, game, scramble_pre_text8, scramble_main_text, scramble_fail_text,
                                                  scramble_post_text8, reward))

    pos = [2, 5]
    solution = next(solutions)  # effulgent
    game = WordScramble(solution)
    reward = 'small'
    scramble_pre_text9 = ['As you enter the room you notice a soft glow that comes from the air itself. You can\'t '
                          'put your finger on the source but it throws the roughly hewn walls into sharp relief and '
                          'in these walls you see a series of square holes. Already knowing what you will find you '
                          'cast your '
                          'eyes downward. They immediately seize upon a small set of tiles. Do you try and place '
                          'them in the holes (solve puzzle)? Maybe the additional light will make things easier.', '']
    scramble_post_text9 = scramble_post_template[0:-3] + ["On the ground in front of you is a small silver key."] + \
                          scramble_post_template[-2::]
    floor_map[pos[0]][pos[1]].spawn_creature(Thor(pos, game, scramble_pre_text9, scramble_main_text, scramble_fail_text,
                                                  scramble_post_text9, reward))

    pos = [8, 12]
    solution = next(solutions)  # impunity
    game = BCGame(solution)
    reward = 'U'
    bc_pre_text1 = ["In front of you you see the almighty Cowthulhu. You are sure it's great and terrible mind can "
                    "envision "
                    "enumerable examples of human suffering and that it is prepared to unleash them all upon you. "
                    "Unless, "
                    "that is, you can guess the word it is thinking of. Do you dare try to undertake such a task ("
                    "solve puzzle)?", '']
    bc_main_text = [f"Guess the word Cowthulhu is thinking of or enter 'exit' to stop playing.",
                    f'The word has {len(solution)} letters', '']
    bc_post_text1 = bc_post_template[::-2] + [f"Looking down you see not another key, but a tile, "
                                              f"this one made of ivory gold. Inscribed on it in a flowing "
                                              f"script is the letter '{reward}'. You pocket the tile. "
                                              f"Certainly "
                                              f"it's purpose will be made clear soon.", '']
    floor_map[pos[0]][pos[1]].spawn_creature(Audumbla(pos, game, bc_pre_text1, bc_main_text, bc_post_text1, reward))

    pos = [7, 15]
    solution = next(solutions)  # phantasm
    game = BCGame(solution)
    reward = 'small'
    bc_pre_text2 = ["You see Cowthulhu in the center of an eerily lit room. The presence of a low, creeping fog makes "
                    "it seems like the supernatural entity is floating a few inches off the floor. Do you attempt "
                    "to engage the bewildering beast despite these new theatrics (solve puzzle)?", '']
    bc_main_text = [f"Guess the word Cowthulhu is thinking of. or enter 'exit' to stop playing.",
                    f'The word has {len(solution)} letters', '']
    bc_post_text2 = bc_post_template[::-2] + ["Looking down you see a small silver key.", '']
    floor_map[pos[0]][pos[1]].spawn_creature(Audumbla(pos, game, bc_pre_text2, bc_main_text, bc_post_text2, reward))

    pos = [4, 12]
    solution = next(solutions)  # sepulchre
    game = BCGame(solution)
    reward = 'T'
    bc_pre_text3 = ["Cowthulhu stands before you on a low hummock. From it's slightly raised vantage point its ominous "
                    "eyes cast both a ruddy light into the room and an umbrous darkness into you soul. You take a "
                    "step forward and stand before your challenger. Do you attempt to "
                    "solve its perplexing puzzle (solve puzzle)?", '']
    bc_main_text = [f"Guess the word Cowthulhu is thinking of. or enter 'exit' to stop playing.",
                    f'The word has {len(solution)} letters', '']
    bc_post_text3 = bc_post_template[::-2] + [f"Looking down you see not another key, but a tile, "
                                              f"this one made of ivory gold. Inscribed on it in a flowing "
                                              f"script is the letter '{reward}'. You pocket the tile. "
                                              f"Certainly "
                                              f"it's purpose will be made clear soon.", '']
    floor_map[pos[0]][pos[1]].spawn_creature(Audumbla(pos, game, bc_pre_text3, bc_main_text, bc_post_text3, reward))

    pos = [0, 8]
    solution = next(solutions)  # immolation
    game = BCGame(solution)
    reward = 'large'
    bc_pre_text4 = ["Cowthulhu's presence looms before you. Its dark, piercing gaze cuts through you and you feel as "
                    "though "
                    "your very soul is on trial in this Lovecraftian labyrinth. Your impending judgement causes you to "
                    "begin perspiring. "
                    "The room itself begins to feel more infernal. Wait... that's not just because of the imposing "
                    "adjudicator. The room is slowly getting hotter, you're sure of it now. Hopefully you can "
                    "solve the current conundrum before you are forced from the room by the hellish heat "
                    "(solve puzzle).", '']
    bc_main_text = [f"Guess the word Cowthulhu is thinking of. or enter 'exit' to stop playing.",
                    f'The word has {len(solution)} letters', '']
    bc_post_text4 = bc_post_template[::-2] + [
        "Looking down you see a glittering golden key.", '']
    floor_map[pos[0]][pos[1]].spawn_creature(Audumbla(pos, game, bc_pre_text4, bc_main_text, bc_post_text4, reward))

    pos = [8, 6]
    solution = next(solutions)  # plutonian
    game = BCGame(solution)
    reward = 'O'
    bc_pre_text5 = ["In the middle of the winding hallway in which you find yourself you see a familiar form. "
                    "Cowthulhu stands before you. You grow worried that it will not let you pass and that your "
                    "progress "
                    "in this dark dimension will come to a halt. However, as you walk forward the beast seems to slide "
                    "into "
                    "some hidden dimension and become a dark silhouette. Maybe you should solve the puzzle anyways "
                    "though. The creature may give you guidance or safe passage. Probably not, but maybe. You should "
                    "at least get a key. "
                    "(solve puzzle).", '']
    bc_main_text = [f"Guess the word Cowthulhu is thinking of. or enter 'exit' to stop playing.",
                    f'The word has {len(solution)} letters', '']
    bc_post_text5 = bc_post_template[::-2] + [f"Looking down you see not another key, but a tile, "
                                              f"this one made of ivory gold. Inscribed on it in a flowing "
                                              f"script is the letter '{reward}'. You pocket the tile. "
                                              f"Certainly "
                                              f"it's purpose will be made clear soon.", '']
    floor_map[pos[0]][pos[1]].spawn_creature(Audumbla(pos, game, bc_pre_text5, bc_main_text, bc_post_text5, reward))

    pos = [6, 2]
    solution = next(solutions)  # malodorous
    game = BCGame(solution)
    reward = 'small'
    bc_pre_text6 = ["As you enter this room a you are overwhelmed by a conglomeration of sensorial inputs that is "
                    "singularly unpleasant. The air feels moist and clings to your skin. The shadows in the corners "
                    "constantly shift and slither into a series of malformed half monsters. There is a constant low "
                    "voice but its ethereal nature prevents you from quite making out its words. The ghoulish taste of "
                    "death lingers on your tongue with every breath. But worst of all is the smell. It is truly "
                    "revolting and you know whoever is putting you through this Miltonian nightmare has truly outdone "
                    "themselves here. So strong are all of these sensory signals that you have failed to notice "
                    "Cowthulhu, who stands in the center of the room, until now. Do you attempt to answer its call "
                    "before your body becomes overwhelmed (solve puzzle)?", '']
    bc_main_text = [f"Guess the word Cowthulhu is thinking of. or enter 'exit' to stop playing.",
                    f'The word has {len(solution)} letters', '']
    bc_post_text6 = bc_post_template[::-2] + ["Looking down you see a small silver key.", '']
    floor_map[pos[0]][pos[1]].spawn_creature(Audumbla(pos, game, bc_pre_text6, bc_main_text, bc_post_text6, reward))

    pos = [10, 3]
    solution = next(solutions)  # pestilence
    game = BCGame(solution)
    reward = 'large'
    bc_pre_text7 = ["As you enter this room you notice that everything in it looks sickly. The walls are covered in "
                    "rot and in places where bricks have fallen away you see a putrid, pulsing slime. Even Cowthulhu, "
                    "who stands at the room's center, has fallen to the vile curse and is covered in pustules "
                    "and open sores. Do you try and help Cowthulhu in the hope that it will remove the blight from the "
                    "chamber (solve puzzle)?"]
    bc_main_text = [f"Guess the word Cowthulhu is thinking of. or enter 'exit' to stop playing.",
                    f'The word has {len(solution)} letters', '']
    bc_post_text7 = bc_post_template[::-2] + ["Looking down you see a glittering golden key. After pocketing your "
                                              "well deserved prize you "
                                              "look around the room. Cowthulhu is gone and the rot appears to "
                                              "have left returning the room to its nominal state of simply dim "
                                              "and unsettling. You hope Cowthulhu is also feeling better.", '']
    floor_map[pos[0]][pos[1]].spawn_creature(Audumbla(pos, game, bc_pre_text7, bc_main_text, bc_post_text7, reward))

    pos = [3, 2]
    solution = next(solutions)  # sagacious
    game = BCGame(solution)
    reward = 'small'
    bc_pre_text8 = ["In the center of the room stands Cowthulhu. You don't notice anything strange about the mighty "
                    "beast this time but you feel wary and watched. Do you attempt to discern the creature's inner "
                    "thoughts once more (solve puzzle)?"]
    bc_main_text = [f"Guess the word Cowthulhu is thinking of. or enter 'exit' to stop playing.",
                    f'The word has {len(solution)} letters', '']
    bc_post_text8 = bc_post_template[::-2] + ["Looking down you see a small silver key. Pocketing the key you smile. "
                                              "You "
                                              "know you can't have many more of these to collect.", '']
    floor_map[pos[0]][pos[1]].spawn_creature(Audumbla(pos, game, bc_pre_text8, bc_main_text, bc_post_text8, reward))

    pos = [4, 2]
    solution = next(solutions)  # masquerade
    game = BCGame(solution)
    reward = 'large'
    bc_pre_text9 = ["Cowthulhu stands at the center of the room. On the walls around it are an assortment of colored "
                    "tapestries. Their edges almost touch and their colors, blue, purple, green, orange, white, "
                    "violet, and deep scarlet, seem to flow into one another. Despite this array of colors they "
                    "give off a somber and crepuscular air. The "
                    "shadows from them seem longer and more sinister than can be logically explained. Tenebrous "
                    "tendrils reach out from them, twisting across the floor towards you. Swallowing the fear that "
                    "has chilled your blood you step farther into the room. Do you talk to Cowthulhu (solve puzzle)?"]
    bc_main_text = [f"Guess the word Cowthulhu is thinking of. or enter 'exit' to stop playing.",
                    f'The word has {len(solution)} letters', '']
    bc_post_text9 = bc_post_template[::-2] + [
        "Looking down you see a glittering golden key.", '']
    floor_map[pos[0]][pos[1]].spawn_creature(Audumbla(pos, game, bc_pre_text9, bc_main_text, bc_post_text9, reward))

    dungeon_map = [floor_map]

    return dungeon_map, player_pos, start_pos_arr, goal_pos_arr, passphrases


def initialize():
    dungeon_map, player_pos, start_pos_arr, goal_pos_arr, passphrases = make_map()

    im_path = maze_funcs.get_image_path()
    maze_funcs.make_black_map(dungeon_map[0], im_path, TILE_SIZE)

    # Create the player
    player = Player(player_pos)

    # Create the dungeon
    dungeon = Dungeon(player, goal_pos_arr, start_pos_arr, passphrases, dungeon_map)

    # Draw the player's starting room
    maze_funcs.draw_current_tile(dungeon.map, player, im_path, TILE_SIZE)

    return dungeon, player
