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
    # Make the map for floor 1
    player_pos = [5, 0]
    goal_pos_arr = [[2, 0]]
    start_pos_arr = [player_pos]
    passphrases = [None]

    floor_map = [[Tile() for _ in range(6)] for _ in range(6)]
    dungeon_map = [floor_map]

    # paths
    # row 0
    floor_map[0][0].add_paths(['n', 'e'])
    floor_map[0][1].add_paths(['e', 'w'])
    floor_map[0][2].add_paths(['e', 'w'])
    floor_map[0][3].add_paths(['e', 'w'])
    floor_map[0][4].add_paths(['e', 'w'])
    floor_map[0][5].add_paths(['n', 'w'])

    # row 1
    floor_map[1][0].add_paths(['s'])
    floor_map[1][1].add_paths(['n'])
    floor_map[1][2].add_paths(['n', 'e'])
    floor_map[1][3].add_paths(['e', 'w'])
    floor_map[1][4].add_paths(['e', 'w'])
    floor_map[1][5].add_paths(['s', 'w'])

    # row 2
    floor_map[2][0].add_paths([])
    floor_map[2][1].add_paths(['s'])
    floor_map[2][2].add_paths(['n', 's'])
    floor_map[2][3].add_paths(['n'])
    floor_map[2][4].add_paths(['e', 'n'])
    floor_map[2][5].add_paths(['n', 'w'])

    # row 3
    floor_map[3][0].add_paths(['n', 'e'])
    floor_map[3][1].add_paths(['e', 'w'])
    floor_map[3][2].add_paths(['s', 'w'])
    floor_map[3][3].add_paths(['e', 's'])
    floor_map[3][4].add_paths(['s', 'w'])
    floor_map[3][5].add_paths(['n', 's'])

    # row 4
    floor_map[4][0].add_paths(['s', 'e'])
    floor_map[4][1].add_paths(['e', 'w'])
    floor_map[4][2].add_paths(['w'])
    floor_map[4][3].add_paths(['e'])
    floor_map[4][4].add_paths(['e', 'w'])
    floor_map[4][5].add_paths(['w', 's'])

    # row 5
    floor_map[5][0].add_paths(['e'])
    floor_map[5][1].add_paths(['e', 'w'])
    floor_map[5][2].add_paths(['e', 'w'])
    floor_map[5][3].add_paths(['e', 'w'])
    floor_map[5][4].add_paths(['e', 'w'])
    floor_map[5][5].add_paths(['w'])

    # doors
    floor_map[5][5].spawn_door('s', 'w')
    floor_map[4][2].spawn_door('e', 'w')
    floor_map[0][1].spawn_door('n', 'w')
    floor_map[2][1].spawn_door('w', 'g')
    maze_funcs.make_doors_2_sided(floor_map)

    # Creatures

    # First thor
    game = WordScramble('word')
    reward = 'small'
    pos = [5, 3]
    pre_text = ["In the room you see a large confused looking man.",
                "He wields a large hammer and you can see he has been using it on the walls, but to little avail.",
                "\"What do you mean!\" He wails pathetically.",
                "\"I, Thor the mighty, have wandered the maze for hours and can find no way out. \"All I've found "
                "besides walls and locked doors lie in this room.\"",
                "On the floor in front of him lie a row of stone tiles.",
                "They spell \"%s\", but that doesn't make much sense." % game.scrambled,
                "On the wall above the tiles are a number of square holes. There are the same number of holes as "
                "tiles.",
                "\"I put the tiles in the holes but they just fall back out again! It's impossible!\" Thor "
                "screams angrily.",
                "Enter 'solve puzzle' to attempt to help the poor man.",
                ""]
    main_text = ["You, brave explorer, are the only one who can hope to solve this intricate and devious "
                 "puzzle.",
                 "Enter the order you wish to place the tiles or \"exit\" to return to the map.",
                 '']
    fail_text = ["The tiles fall back onto the floor, amazingly into the same order the were originally.",
                 '']
    post_text = ["Thor stares at you dumbfounded.",
                 "\"But that's the same thing I did! And I pushed on the tiles ten times harder to make them "
                 "stay in place!\"",
                 "\"It's... it's the order of the tiles\" you say. It's amazing to you that this information "
                 "needs to be conveyed.",
                 "\"They are supposed to spell \'%s\'.\"" % game.answer,
                 "\"So that's the secret!\" Leaping forward Thor grabs the tiles in order and puts them in the "
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
                 '']
    floor_map[pos[0]][pos[1]].spawn_creature(Thor(pos, game, pre_text, main_text, fail_text, post_text, reward))

    # Second thor
    game = WordScramble('brother')
    reward = 'small'
    pos = [3, 2]
    pre_text = ["You see Thor again. He is lying on the ground in the fetal position. He does not look happy...",
                'Do you attempt to help this poor man (solve puzzle)?',
                '']
    main_text = ["You kneel down next to Thor. \"How's it going buddy?\" you gently inquire.",
                 "\"Not well...\" he reluctantly admits.",
                 "\"I can't figure out what to do with the tiles. And they've grown in number!\"",
                 "Looking down you see he is correct. Tiles are spread across the floor spelling %s." % game.scrambled,
                 "\"Loki even said he'd help me out.\" Thor mutters. \"But his hint didn't make any "
                 "sense.",
                 "He said I was the answer, but when I spell my name there are still two tiles left!",
                 "Perhaps you can help me again?\"",
                 "Enter the order you wish to place the tiles or \"exit\" to return to the map.",
                 '']
    fail_text = ["The tiles fall back onto the floor, amazingly into the same order the were originally.",
                 '']
    post_text = ["A small panel opens next to you revealing another silver key."
                 "You hastily grab it. Its golden allure is overpowering."
                 ""
                 "\"Aha!\" he shouts. \"So Loki said I was the answer but it was he, my brother, who was the "
                 "answer. "
                 "Such devilish tricks\" "
                 "Shaking your head you decide not to stay and see if he can figure out how to spell out the "
                 "word again. "
                 ""]
    floor_map[pos[0]][pos[1]].spawn_creature(Thor(pos, game, pre_text, main_text, fail_text, post_text, reward))

    # Audumbla one
    pos = [2, 3]
    game = BCGame('yggdrasil')
    reward = 'small'
    pre_text = ["In the room you see a mighty cow. On the floor next to it lies a piece of parchment.",
                "You bend over and pick it up. Written in smooth, dark ink is a strange set of instructions.",
                "",
                "Before you lies Audumbla, the most ancient and powerful cow in the 9 realms.",
                "The cow's mind is deep and troubled for though it can think of words it cannot speak them.",
                "If you be brave of heart, help the cow in her plight by speaking the word that she is thinking.",
                "To do this you must step up to her and speak a word whose length is equal to the number of children "
                "spawned by Aegir and Ran.",
                "The cow will lick the block of salt in front of it once for every letter in your word that is also "
                "in her word, and in the correct position.",
                "She will then stomp her hoof once for every letter in your word that is in her word, "
                "but not in the correct position.",
                "If you please the cow you will be rewarded.",
                "Enter 'solve puzzle' face this strange challenge.",
                ""]
    main_text = ["The cow's eyes stare into you soul. Their emptiness reflecting your progress thus far.",
                 "You somehow get the feeling Audumbla believes your progress will remain dreadfully low.",
                 "Hoping to prove this primordial cow, and your parents, wrong you step forward.",
                 "Enter the word you think she is thinking of or \"exit\" to return to the map.",
                 '']
    post_text = ["The cow takes a step forward. You flinch but hold your ground.",
                 "It leans forward and licks your palm.",
                 "Looking down you see a shiny silver key.",
                 "Success! You have defeated a mute bovine creature in a game of words and wits. Take that "
                 "world!",
                 "",
                 "The cow bows it's head deeply. Clearly out of respect for you and not to lick the salt "
                 "block one more time (although it does this as well).",
                 "It then fades, seeming to slide out of existence as easily as a primordial knife through "
                 "ancient cow butter.",
                 "You look around the room for a few seconds before deciding there is nothing more to be done "
                 "here.",
                 ""]
    floor_map[pos[0]][pos[1]].spawn_creature(Audumbla(pos, game, pre_text, main_text, post_text, reward))

    # Audumbla two
    pos = [1, 0]
    game = BCGame('nordic')
    reward = 'large'
    pre_text = ["The cow stands before you again.",
                "You scan the ground for another set of instructions but see none.",
                "Do you attempt to meet the cow's challenge again (solve puzzle)?",
                '']
    main_text = ["\"Let's dance you and I.\" you cackle.",
                 "You look at the cow, hoping your witty banter has thrown it off guard.",
                 "The cow blinks 6 times and then simply stares at you.",
                 "Only mildly unnerved you decide it's time to begin guessing.",
                 "Enter the word you think she is thinking of or \"exit\" to return to the map.",
                 '']
    post_text = ["The cow takes a step forward. This time you stand your ground, cool and confident.",
                 "The cow leans forward and licks your palm.",
                 "Looking down you see a giant golden key in your hand. What could this be for?",
                 "",
                 "After a few seconds you look up to find the cow, unsurprisingly, gone.",
                 ""]
    floor_map[pos[0]][pos[1]].spawn_creature(Audumbla(pos, game, pre_text, main_text, post_text, reward))

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
