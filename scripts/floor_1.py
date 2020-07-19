import numpy as np

import scripts.generate_maze as maze_funcs
from dungeon_classes.tile_class import Tile

oppositeDirs = {"n": "s", "e": "w", "s": "n", "w": "e"}


def make_doors_2_sided(dungeon_map):
    m_rows, m_cols = np.shape(dungeon_map)

    for row in range(m_rows):  # search through tiles
        for col in range(m_cols):
            if dungeon_map[row][col].doors:  # if a tile has doors
                for door in dungeon_map[row][col].doors:  # go through them
                    tile = get_adjacent_tile(row, col, door.direction, dungeon_map)  # get adjacent tile
                    tile.spawn_door(oppositeDirs[door.direction],
                                   door.type)  # make a companion door (so they're 2 sided)


def get_adjacent_tile(row, col, direction, dungeon_map):
    if direction == "n" and row <= np.shape(dungeon_map)[0] - 1:
        tile = dungeon_map[row + 1][col]
    elif direction == "e" and col <= np.shape(dungeon_map)[1] - 1:
        tile = dungeon_map[row][col + 1]
    elif direction == "s" and row > 0:
        tile = dungeon_map[row - 1][col]
    elif direction == "w" and col > 0:
        tile = dungeon_map[row][col - 1]
    else:
        raise ValueError("Can't get tile adjacent to %d, %d in map creation." % (row, col))
    return tile


def move(direction):
    tile = dungeon_map[player_pos[0]][player_pos[1]]
    if direction in tile.paths:
        if direction == "n":
            player_pos[0] += 1
        elif direction == "e":
            player_pos[1] += 1
        elif direction == "s":
            player_pos[0] -= 1
        elif direction == "w":
            player_pos[1] -= 1

        maze_funcs.make_map_image(dungeon_map, player_pos)


player_pos = [5, 0]
passphrases = ["humble beginnings", "good start", "crushing it", "beast mode"]

dungeon_map = [[Tile() for _ in range(6)] for _ in range(6)]

# paths
# row 0
dungeon_map[0][0].add_paths(['n', 'e'])
dungeon_map[0][1].add_paths(['e', 'w'])
dungeon_map[0][2].add_paths(['e', 'w'])
dungeon_map[0][3].add_paths(['e', 'w'])
dungeon_map[0][4].add_paths(['e', 'w'])
dungeon_map[0][5].add_paths(['n', 'w'])

# row 1
dungeon_map[1][0].add_paths(['s'])
dungeon_map[1][1].add_paths(['n'])
dungeon_map[1][2].add_paths(['n', 'e'])
dungeon_map[1][3].add_paths(['e', 'w'])
dungeon_map[1][4].add_paths(['e', 'w'])
dungeon_map[1][5].add_paths(['s', 'w'])

# row 2
dungeon_map[2][0].add_paths([])
dungeon_map[2][1].add_paths(['s'])
dungeon_map[2][2].add_paths(['n', 's'])
dungeon_map[2][3].add_paths(['n'])
dungeon_map[2][4].add_paths(['e', 'n'])
dungeon_map[2][5].add_paths(['n', 'w'])

# row 3
dungeon_map[3][0].add_paths(['n', 'e'])
dungeon_map[3][1].add_paths(['e', 'w'])
dungeon_map[3][2].add_paths(['s', 'w'])
dungeon_map[3][3].add_paths(['e', 's'])
dungeon_map[3][4].add_paths(['s', 'w'])
dungeon_map[3][5].add_paths(['n', 's'])

# row 4
dungeon_map[4][0].add_paths(['s', 'e'])
dungeon_map[4][1].add_paths(['e', 'w'])
dungeon_map[4][2].add_paths(['w'])
dungeon_map[4][3].add_paths(['e'])
dungeon_map[4][4].add_paths(['e', 'w'])
dungeon_map[4][5].add_paths(['w', 's'])

# row 5
dungeon_map[5][0].add_paths(['e'])
dungeon_map[5][1].add_paths(['e', 'w'])
dungeon_map[5][2].add_paths(['e', 'w'])
dungeon_map[5][3].add_paths(['e', 'w'])
dungeon_map[5][4].add_paths(['e', 'w'])
dungeon_map[5][5].add_paths(['w'])

# doors
dungeon_map[5][5].spawn_door('s', 'w')
dungeon_map[4][2].spawn_door('e', 'w')
dungeon_map[0][1].spawn_door('n', 'w')
dungeon_map[2][1].spawn_door('w', 'g')
make_doors_2_sided(dungeon_map)

maze_funcs.make_map_image(dungeon_map, player_pos)

# while True:
#     new_dir = input("Direction").strip().lower()
#     tile = dungeon_map[player_pos[0]][player_pos[1]]
#     if new_dir in tile.paths:
#         if new_dir == "n":
#             player_pos[0] += 1
#         elif new_dir == "e":
#             player_pos[1] += 1
#         elif new_dir == "s":
#             player_pos[0] -= 1
#         elif new_dir == "w":
#             player_pos[1] -= 1
#
#         maze_funcs.make_map_image(dungeon_map, player_pos)


