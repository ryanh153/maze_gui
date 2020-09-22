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
    floor_map[5][3].spawn_creature(Thor([5, 3], WordScramble('word')))
    floor_map[3][2].spawn_creature(Thor([3, 2], WordScramble("brother")))
    floor_map[2][3].spawn_creature(Audumbla([2, 3], BCGame('yggdrasil')))
    floor_map[1][0].spawn_creature(Audumbla([1, 0], BCGame('nordic')))

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
