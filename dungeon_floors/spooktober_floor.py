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
    player_pos = [6, 7]
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
    floor_map[1][7].special_text = ["Upon entereing the room you are immediately enraptured by the effulgent door on "
                                    "the far side of the room. It fills and entire wall and is made of purely of "
                                    "ivory and gold with the exception of an ebony raven at its center. Above the "
                                    "raven in the same flowing script as on the tiles you have collected are the "
                                    "words. What is my name? Below the raven are five empty slots in which you may "
                                    "place tiles. If you have all the tiles you may enter the order in which you wish "
                                    "to place them. Otherwise your journey is not over yet.", '']
    # Creatures

    # set up common text fields
    scramble_pre_text = ["On the floor you see a set of jumbled tiles.",
                         "Perhaps if you put them into the proper order there will be a reward.",
                         "Would you like to try (solve puzzle)?", '']
    scramble_main_text = ["Enter the letters in the correct order or enter 'exit' to stop playing.", '']
    scramble_fail_text = ["The tiles spontaneously throw themselves into the same jumbled pile they were in when you "
                          "entered the room."
                          "Perhaps that wasn't correct..",
                          '']
    scramble_post_template = ["The tiles glow with an eerie light that steadily grows until it nearly blinds you. You "
                              "raise your hands to shield your eyes but after a few seconds the unexplained "
                              "brilliance fades.",
                              '',  # replace this with the reward specific text
                              "You pick up the key and put it in your pocket. It may be useful soon.",
                              '']

    bc_pre_text = ['In the room you see an all too familiar cow.',
                   'You know its tricks well now and approach confidently, ready to meet its challenge (solve puzzle).',
                   '']
    bc_post_template = ["The cow bows its head and licks your palm.",
                        'As its tongue pulls away you you feel a familiar shape in your palm.',
                        '']

    solutions = ['ghastly', 'morbid', 'odious', 'ebony', 'spectral', 'ominous', 'debauch', 'atrocity', 'effulgent',
                 'impunity', 'phantasm', 'sepulchre', 'immolation', 'plutonian', 'malodorous', 'pestilence',
                 'sagacious', 'masquerade']
    # solutions = []
    solutions = iter(solutions)

    pos = [6, 6]
    solution = next(solutions)
    game = WordScramble(solution)
    reward = 'small'
    scramble_pre_text1 = ["As you enter the room a feeling of decay seeps into you. Looking around you see "
                          "that even the walls seem to be rotten and putrescent. Some of the bricks that "
                          "make "
                          "up the far wall have even fallen out and lie strewn across the floor. Upon "
                          "closer inspection you realize that some of these bricks are not the normal blank "
                          "masonry but contain the faint outline of a letter. Maybe if you place them back in the "
                          "wall in the correct order they will give you some clue as to the origin of your current "
                          "confinement (solve puzzle).", '']
    scramble_post_text1 = scramble_post_template[0:-3] + ["On the ground in front of you is a small silver key."] + \
                          scramble_post_template[-2::]
    floor_map[pos[0]][pos[1]].spawn_creature(Thor(pos, game, scramble_pre_text1, scramble_main_text, scramble_fail_text,
                                                  scramble_post_text1, reward))

    pos = [4, 6]
    solution = next(solutions)
    game = WordScramble(solution)
    reward = 'small'
    scramble_post_text2 = scramble_post_template[0:-3] + ["On the ground in front of you is a small silver key."] + \
                          scramble_post_template[-2::]
    floor_map[pos[0]][pos[1]].spawn_creature(Thor(pos, game, scramble_pre_text, scramble_main_text, scramble_fail_text,
                                                  scramble_post_text2, reward))

    pos = [10, 12]
    solution = next(solutions)
    game = WordScramble(solution)
    reward = 'large'
    scramble_post_text3 = scramble_post_template[0:-3] + ["On the ground in front of you is a glittering golden key."] + \
                          scramble_post_template[-2::]
    floor_map[pos[0]][pos[1]].spawn_creature(Thor(pos, game, scramble_pre_text, scramble_main_text, scramble_fail_text,
                                                  scramble_post_text3, reward))

    pos = [2, 14]
    solution = next(solutions)
    game = WordScramble(solution)
    reward = 'small'
    scramble_post_text4 = scramble_post_template[0:-3] + ["On the ground in front of you is a small silver key."] + \
                          scramble_post_template[-2::]
    floor_map[pos[0]][pos[1]].spawn_creature(Thor(pos, game, scramble_pre_text, scramble_main_text, scramble_fail_text,
                                                  scramble_post_text4, reward))

    pos = [2, 10]
    solution = next(solutions)
    game = WordScramble(solution)
    reward = 'small'
    scramble_post_text5 = scramble_post_template[0:-3] + ["On the ground in front of you is a small silver key."] + \
                          scramble_post_template[-2::]
    floor_map[pos[0]][pos[1]].spawn_creature(Thor(pos, game, scramble_pre_text, scramble_main_text, scramble_fail_text,
                                                  scramble_post_text5, reward))

    pos = [1, 9]
    solution = next(solutions)
    game = WordScramble(solution)
    reward = 'H'
    scramble_post_text6 = scramble_post_template[0:-3] + [f"Looking down you see not another key, but another tile, "
                                                          f"this one made of ivory gold. Inscribed on it in a flowing "
                                                          f"script is the letter '{reward}'. You pocket the tile. "
                                                          f"Certainly "
                                                          f"it's purpose will be made clear soon.", ''] + \
                          scramble_post_template[-2::]
    floor_map[pos[0]][pos[1]].spawn_creature(Thor(pos, game, scramble_pre_text, scramble_main_text, scramble_fail_text,
                                                  scramble_post_text6, reward))

    pos = [10, 4]
    solution = next(solutions)
    game = WordScramble(solution)
    reward = 'small'
    scramble_post_text7 = scramble_post_template[0:-3] + ["On the ground in front of you is a small silver key."] + \
                          scramble_post_template[-2::]
    floor_map[pos[0]][pos[1]].spawn_creature(Thor(pos, game, scramble_pre_text, scramble_main_text, scramble_fail_text,
                                                  scramble_post_text7, reward))

    pos = [7, 2]
    solution = next(solutions)
    game = WordScramble(solution)
    reward = 'Q'
    scramble_post_text8 = scramble_post_template[0:-3] + [f"Looking down you see not another key, but another tile, "
                                                          f"this one made of ivory gold. Inscribed on it in a flowing "
                                                          f"script is the letter '{reward}'. You pocket the tile. "
                                                          f"Certainly "
                                                          f"it's purpose will be made clear soon.", ''] + \
                          scramble_post_template[-2::]
    floor_map[pos[0]][pos[1]].spawn_creature(Thor(pos, game, scramble_pre_text, scramble_main_text, scramble_fail_text,
                                                  scramble_post_text8, reward))

    pos = [2, 5]
    solution = next(solutions)
    game = WordScramble(solution)
    reward = 'small'
    scramble_post_text9 = scramble_post_template[0:-3] + ["On the ground in front of you is a small silver key."] + \
                          scramble_post_template[-2::]
    floor_map[pos[0]][pos[1]].spawn_creature(Thor(pos, game, scramble_pre_text, scramble_main_text, scramble_fail_text,
                                                  scramble_post_text9, reward))

    pos = [8, 12]
    solution = next(solutions)
    game = BCGame(solution)
    reward = 'U'
    bc_main_text = [f"Guess the word the cow is thinking of or enter 'exit' to stop playing.",
                    f'The word has {len(solution)} letters', '']
    bc_post_text1 = bc_post_template[::-2] + [f"Looking down you see not another key, but a tile, "
                                              f"this one made of ivory gold. Inscribed on it in a flowing "
                                              f"script is the letter '{reward}'. You pocket the tile. "
                                              f"Certainly "
                                              f"it's purpose will be made clear soon.", '']
    floor_map[pos[0]][pos[1]].spawn_creature(Audumbla(pos, game, bc_pre_text, bc_main_text, bc_post_text1, reward))

    pos = [7, 15]
    solution = next(solutions)
    game = BCGame(solution)
    reward = 'small'
    bc_main_text = [f"Guess the word the cow is thinking of. or enter 'exit' to stop playing.",
                    f'The word has {len(solution)} letters', '']
    bc_post_text2 = bc_post_template[::-2] + ["Looking down you see a small silver key.", '']
    floor_map[pos[0]][pos[1]].spawn_creature(Audumbla(pos, game, bc_pre_text, bc_main_text, bc_post_text2, reward))

    pos = [4, 12]
    solution = next(solutions)
    game = BCGame(solution)
    reward = 'T'
    bc_main_text = [f"Guess the word the cow is thinking of. or enter 'exit' to stop playing.",
                    f'The word has {len(solution)} letters', '']
    bc_post_text3 = bc_post_template[::-2] + [f"Looking down you see not another key, but a tile, "
                                              f"this one made of ivory gold. Inscribed on it in a flowing "
                                              f"script is the letter '{reward}'. You pocket the tile. "
                                              f"Certainly "
                                              f"it's purpose will be made clear soon.", '']
    floor_map[pos[0]][pos[1]].spawn_creature(Audumbla(pos, game, bc_pre_text, bc_main_text, bc_post_text3, reward))

    pos = [0, 8]
    solution = next(solutions)
    game = BCGame(solution)
    reward = 'large'
    bc_main_text = [f"Guess the word the cow is thinking of. or enter 'exit' to stop playing.",
                    f'The word has {len(solution)} letters', '']
    bc_post_text4 = bc_post_template[::-2] + ["Looking down you see a glittering golden key.", '']
    floor_map[pos[0]][pos[1]].spawn_creature(Audumbla(pos, game, bc_pre_text, bc_main_text, bc_post_text4, reward))

    pos = [8, 6]
    solution = next(solutions)
    game = BCGame(solution)
    reward = 'O'
    bc_main_text = [f"Guess the word the cow is thinking of. or enter 'exit' to stop playing.",
                    f'The word has {len(solution)} letters', '']
    bc_post_text5 = bc_post_template[::-2] + [f"Looking down you see not another key, but a tile, "
                                              f"this one made of ivory gold. Inscribed on it in a flowing "
                                              f"script is the letter '{reward}'. You pocket the tile. "
                                              f"Certainly "
                                              f"it's purpose will be made clear soon.", '']
    floor_map[pos[0]][pos[1]].spawn_creature(Audumbla(pos, game, bc_pre_text, bc_main_text, bc_post_text5, reward))

    pos = [6, 2]
    solution = next(solutions)
    game = BCGame(solution)
    reward = 'small'
    bc_main_text = [f"Guess the word the cow is thinking of. or enter 'exit' to stop playing.",
                    f'The word has {len(solution)} letters', '']
    bc_post_text6 = bc_post_template[::-2] + ["Looking down you see a small silver key.", '']
    floor_map[pos[0]][pos[1]].spawn_creature(Audumbla(pos, game, bc_pre_text, bc_main_text, bc_post_text6, reward))

    pos = [10, 3]
    solution = next(solutions)
    game = BCGame(solution)
    reward = 'large'
    bc_main_text = [f"Guess the word the cow is thinking of. or enter 'exit' to stop playing.",
                    f'The word has {len(solution)} letters', '']
    bc_post_text7 = bc_post_template[::-2] + ["Looking down you see a glittering golen key.", '']
    floor_map[pos[0]][pos[1]].spawn_creature(Audumbla(pos, game, bc_pre_text, bc_main_text, bc_post_text7, reward))

    pos = [3, 2]
    solution = next(solutions)
    game = BCGame(solution)
    reward = 'small'
    bc_main_text = [f"Guess the word the cow is thinking of. or enter 'exit' to stop playing.",
                    f'The word has {len(solution)} letters', '']
    bc_post_text8 = bc_post_template[::-2] + ["Looking down you see a small silver key.", '']
    floor_map[pos[0]][pos[1]].spawn_creature(Audumbla(pos, game, bc_pre_text, bc_main_text, bc_post_text8, reward))

    pos = [4, 2]
    solution = next(solutions)
    game = BCGame(solution)
    reward = 'large'
    bc_main_text = [f"Guess the word the cow is thinking of. or enter 'exit' to stop playing.",
                    f'The word has {len(solution)} letters', '']
    bc_post_text9 = bc_post_template[::-2] + ["Looking down you see a glittering golden key.", '']
    floor_map[pos[0]][pos[1]].spawn_creature(Audumbla(pos, game, bc_pre_text, bc_main_text, bc_post_text9, reward))

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
