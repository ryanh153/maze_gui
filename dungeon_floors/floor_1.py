from pathlib import Path

import services.level_service as maze_funcs
from dungeon_classes.tile_class import Tile
from dungeon_classes.dungeon_class import Dungeon
from dungeon_classes.player_class import Player

from dungeon_classes.thor_class import Thor
from dungeon_classes.word_scramble_class import WordScramble

from dungeon_classes.bull_cow_class import BCGame
from dungeon_classes.audumbla_class import Audumbla

TILE_SIZE = 75
dungeon, player = None, None


# These functions are called externally so we make this floor's properties global
# so they can be called without knowledge of which floor they're being called on
def make_action(command):
    global dungeon, player
    print(f'make action\npos: {player.pos}\ndungeon: {dungeon}')
    text = []
    im_path = get_image_path()
    tile = dungeon.map[player.pos[0]][player.pos[1]]

    # key pickup
    if command == 'pickup key' and tile.has_key:
        player.small_keys += 1
        tile.has_key = False
        maze_funcs.erase_key_icon(get_image_path(), player.pos, len(dungeon.map), TILE_SIZE)
        text.extend(['You pickup the a small, silver key.',
                     'It is heavily tarnished but you are confident it will still function.', '', ''])

    # move or open
    else:
        command = command.split(' ')
        if len(command) != 2:
            text.extend(["Command not understood", '', ''])
            return text

        cmd = command[0].lower()
        direction = command[1].lower()
        if cmd == 'move':
            old_pos = [p for p in player.pos]  # so we don't save a reference to player.pos
            if maze_funcs.move_player(dungeon.map, player.pos, direction):
                maze_funcs.erase_player(im_path, old_pos, len(dungeon.map), TILE_SIZE)
                if dungeon.map[player.pos[0]][player.pos[1]].special_text:
                    text.extend(dungeon.map[player.pos[0]][player.pos[1]].special_text)
                    text.extend(['', ''])
                else:
                    text.extend(["You enter a dimly lit room", '', ''])
            else:
                text.extend(["There is no path in that direction", '', ''])
        elif cmd == 'open':
            text.extend(dungeon.open_door(tile, direction, player))
            text.extend(['', ''])
        else:
            text.extend(["Command not understood", '', ''])
            return text

    maze_funcs.draw_current_tile(dungeon.map, player, im_path, TILE_SIZE)
    return text


def interact():
    global dungeon, player
    return dungeon.interact(player)


def start_mini_game(command):
    tile = get_current_tile()
    if command == 'solve puzzle' and tile.has_creature:
        tile.creature.started_game = True
        return True
    return False


def mini_game_guess(player_guess):
    global dungeon, player
    tile = get_current_tile()
    if tile.has_creature:
        solved, text = tile.creature.interact(player, player_guess)
        if solved:
            tile.despawn_creature()
            maze_funcs.erase_key_icon(get_image_path(), player.pos, len(dungeon.map), TILE_SIZE)
        return solved, text


def mini_game_text():
    global dungeon, player
    tile = dungeon.map[player.pos[0]][player.pos[1]]
    return tile.creature.current_text


def check_win():
    global dungeon, player
    return player.pos == dungeon.goal_pos_arr[0]


def get_current_tile():
    global dungeon, player
    return dungeon.map[player.pos[0]][player.pos[1]]


def make_map():
    # Make the map for floor 1
    player_pos = [5, 0]
    goalPosArr = [[2, 0]]
    startPosArr = [player_pos]
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

    return dungeon_map, player_pos, startPosArr, goalPosArr, passphrases


def get_image_path():
    # make the map image and designate it as the current level image
    return Path('static/img/curr_level.png').absolute()


def initialize():
    global dungeon, player
    dungeon_map, player_pos, start_pos_arr, goal_pos_arr, passphrases = make_map()

    im_path = get_image_path()
    maze_funcs.make_black_map(dungeon_map[0], im_path, TILE_SIZE)

    # Create the player
    player = Player(player_pos)

    # Create the dungeon
    dungeon = Dungeon(player, goal_pos_arr, start_pos_arr, passphrases, dungeon_map)

    # Draw the player's starting room
    maze_funcs.draw_current_tile(dungeon.map, player, im_path, TILE_SIZE)
