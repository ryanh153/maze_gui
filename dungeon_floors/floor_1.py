from pathlib import Path

import services.level_service as maze_funcs
from dungeon_classes.tile_class import Tile
from dungeon_classes.dungeonClass import Dungeon
from dungeon_classes.playerClass import Player


# These functions are called externally so we make this floor's properties global
# so they can be called without knowledge of which floor they're being called on
def move(direction):
    global dungeon_map, player_pos, im_path
    maze_funcs.move_player(dungeon_map, player_pos, direction)
    maze_funcs.make_map_image(dungeon_map, player_pos, im_path)


def interact():
    global player
    return dungeon.interact(player)


# Make the map for floor 1
player_pos = [5, 0]
goalPosArr = [[2, 0]]
startPosArr = [player_pos]
passphrases = [None]

dungeon_map = [[Tile() for _ in range(6)] for _ in range(6)]
mapArr = [dungeon_map]

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
maze_funcs.make_doors_2_sided(dungeon_map)

# make the map image and designate it as the current level image
im_path = Path('static/img/curr_level.png').absolute()
maze_funcs.make_map_image(dungeon_map, player_pos, im_path)

# Create the player
player = Player(player_pos)

# Create the dungeon
dungeon = Dungeon(player, goalPosArr, startPosArr, passphrases, mapArr)
