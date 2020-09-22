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
