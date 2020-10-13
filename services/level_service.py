from collections import namedtuple
from pathlib import Path

import numpy as np
from PIL import Image

WHITE = (255, 255, 255)
BROWN = (153, 102, 51)
GREEN = (0, 204, 0)
BLACK = (0, 0, 0)
GREY = (220, 220, 220)
GOLD = (255, 215, 0)

OPPOSITE_DIRECTIONS = {"n": "s", "e": "w", "s": "n", "w": "e"}

Icon = namedtuple('Image', ['image', 'height', 'width', 'padding'])
PLAYER_IMAGE = np.array(Image.open('static/img/player_image.png'))[:, :, 0:3]
PLAYER_ICON = Icon(PLAYER_IMAGE, np.shape(PLAYER_IMAGE)[0], np.shape(PLAYER_IMAGE)[1], 1)

SILVER_KEY_IMAGE = np.array(Image.open('static/img/silver_key.png'))[:, :, 0:3]
SILVER_KEY_ICON = Icon(SILVER_KEY_IMAGE, np.shape(SILVER_KEY_IMAGE)[0], np.shape(SILVER_KEY_IMAGE)[1], 1)

GOLD_KEY_IMAGE = np.array(Image.open('static/img/gold_key.png'))[:, :, 0:3]
GOLD_KEY_ICON = Icon(GOLD_KEY_IMAGE, np.shape(GOLD_KEY_IMAGE)[0], np.shape(GOLD_KEY_IMAGE)[1], 1)

REWARD_TILE_IMAGE = np.array(Image.open('static/img/reward_tile.png'))[:, :, 0:3]
REWARD_TILE_ICON = Icon(REWARD_TILE_IMAGE, np.shape(REWARD_TILE_IMAGE)[0], np.shape(REWARD_TILE_IMAGE)[1], 2)


# Functions for generating an image from a map
def make_black_map(dungeon_map, im_path, tile_size):
    width, height = len(dungeon_map[0]) * tile_size, len(dungeon_map) * tile_size
    im_array = np.zeros([height, width, 3], dtype=np.uint8)
    im = Image.fromarray(im_array)
    im.save(im_path)


def draw_current_tile(dungeon_map, player, im_path, tile_size):
    im_array = np.array(Image.open(im_path))
    maze_dim = len(dungeon_map)

    top_left = (tile_size * (maze_dim - player.pos[0] - 1), tile_size * player.pos[1])
    tile = dungeon_map[player.pos[0]][player.pos[1]]
    draw_tile(im_array, tile, tile_size, top_left)

    draw_player(im_array, player.pos, maze_dim, tile_size)
    if tile.has_key:
        draw_silver_key(im_array, player.pos, maze_dim, tile_size)
    if tile.has_creature:
        if tile.creature.reward == 'small':
            draw_silver_key(im_array, player.pos, maze_dim, tile_size)
        elif tile.creature.reward == 'large':
            draw_gold_key(im_array, player.pos, maze_dim, tile_size)
        elif len(tile.creature.reward) == 1 and isinstance(tile.creature.reward, str):
            draw_reward_tile(im_array, player.pos, maze_dim, tile_size)
        else:
            raise ValueError("Drawing tile with puzzle but no reward")

    im = Image.fromarray(im_array)
    im.save(im_path)


def make_full_map(dungeon_map, player_pos, im_path, tile_size):
    maze_dim = len(dungeon_map)
    im_size = maze_dim * tile_size
    im_array = np.zeros([im_size, im_size, 3], dtype=np.uint8)

    draw_player(im_array, player_pos, maze_dim, tile_size)

    for r, row in enumerate(reversed(dungeon_map)):
        for c, tile in enumerate(row):
            top_left = (tile_size * r, tile_size * c)
            draw_tile(im_array, tile, tile_size, top_left)
    save_image(im_array, im_path)


def save_image(im_array, im_path):
    im = Image.fromarray(im_array)
    im.save(im_path)


def get_top_left(maze_dim, tile_size, pos):
    row, col = maze_dim - (pos[0] + 1), pos[1]
    return tile_size * row, tile_size * col


def draw_player(im_array, pos, maze_dim, tile_size):
    top_left = get_top_left(maze_dim, tile_size, pos)
    im_array[top_left[0] + tile_size - PLAYER_ICON.height - PLAYER_ICON.padding:
             top_left[0] + tile_size - PLAYER_ICON.padding,
             top_left[1] + PLAYER_ICON.padding:
             top_left[1] + PLAYER_ICON.padding + PLAYER_ICON.width,
             :] = PLAYER_ICON.image


def erase_player(im_path, pos, maze_dim, tile_size):
    im_array = np.array(Image.open(im_path))
    top_left = get_top_left(maze_dim, tile_size, pos)
    im_array[top_left[0] + tile_size - PLAYER_ICON.height - PLAYER_ICON.padding:
             top_left[0] + tile_size - PLAYER_ICON.padding,
             top_left[1] + PLAYER_ICON.padding:
             top_left[1] + PLAYER_ICON.padding + PLAYER_ICON.width,
             :] = BLACK

    save_image(im_array, im_path)


def draw_silver_key(im_array, pos, maze_dim, tile_size):
    top_left = get_top_left(maze_dim, tile_size, pos)
    im_array[top_left[0] + SILVER_KEY_ICON.padding:
             top_left[0] + SILVER_KEY_ICON.padding + SILVER_KEY_ICON.height,
    top_left[1] + tile_size - SILVER_KEY_ICON.width - SILVER_KEY_ICON.padding:
             top_left[1] + tile_size - SILVER_KEY_ICON.padding,
             :] = SILVER_KEY_ICON.image


def draw_gold_key(im_array, pos, maze_dim, tile_size):
    top_left = get_top_left(maze_dim, tile_size, pos)
    im_array[top_left[0] + GOLD_KEY_ICON.padding:
             top_left[0] + GOLD_KEY_ICON.padding + GOLD_KEY_ICON.height,
             top_left[1] + tile_size - GOLD_KEY_ICON.width - GOLD_KEY_ICON.padding:
             top_left[1] + tile_size - GOLD_KEY_ICON.padding,
             :] = GOLD_KEY_ICON.image


def draw_reward_tile(im_array, pos, maze_dim, tile_size):
    top_left = get_top_left(maze_dim, tile_size, pos)
    im_array[top_left[0] + REWARD_TILE_ICON.padding:
             top_left[0] + REWARD_TILE_ICON.padding + REWARD_TILE_ICON.height,
             top_left[1] + tile_size - REWARD_TILE_ICON.width - REWARD_TILE_ICON.padding:
             top_left[1] + tile_size - REWARD_TILE_ICON.padding,
             :] = REWARD_TILE_ICON.image


def erase_key_icon(im_path, pos, maze_dim, tile_size):
    im_array = np.array(Image.open(im_path))
    top_left = get_top_left(maze_dim, tile_size, pos)
    im_array[top_left[0] + SILVER_KEY_ICON.padding:
             top_left[0] + SILVER_KEY_ICON.padding + SILVER_KEY_ICON.height,
             top_left[1] + tile_size - SILVER_KEY_ICON.width - SILVER_KEY_ICON.padding:
             top_left[1] + tile_size - SILVER_KEY_ICON.padding,
             :] = BLACK

    save_image(im_array, im_path)


def draw_tile(im_array, tile, tile_size, top_left):
    directions = ['n', 'e', 's', 'w']
    for direction in directions:
        if direction in tile.paths:
            draw_tile_side_short(im_array, direction, top_left, tile_size, GREY)
        else:
            draw_tile_side(im_array, direction, top_left, tile_size, WHITE)

    for door in tile.doors:
        color = BROWN if door.type == 'w' else GOLD
        draw_tile_side(im_array, door.direction, top_left, tile_size, color)


def draw_tile_side(im_array, direction, top_left, tile_size, color):
    if direction == 'w':
        im_array[top_left[0]:top_left[0] + tile_size, top_left[1], :] = color
    if direction == 'e':
        im_array[top_left[0]:top_left[0] + tile_size, top_left[1] + tile_size - 1, :] = color
    if direction == 'n':
        im_array[top_left[0], top_left[1]:top_left[1] + tile_size, :] = color
    if direction == 's':
        im_array[top_left[0] + tile_size - 1, top_left[1]:top_left[1] + tile_size, :] = color


def draw_tile_side_short(im_array, direction, top_left, tile_size, color):
    if direction == 'w':
        im_array[top_left[0] + 1:top_left[0] + tile_size - 1, top_left[1], :] = BLACK
        im_array[top_left[0] + 1:top_left[0] + tile_size - 1:3, top_left[1], :] = color
    if direction == 'e':
        im_array[top_left[0] + 1:top_left[0] + tile_size - 1, top_left[1] + tile_size - 1, :] = BLACK
        im_array[top_left[0] + 1:top_left[0] + tile_size - 1:3, top_left[1] + tile_size - 1, :] = color
    if direction == 'n':
        im_array[top_left[0], top_left[1] + 1:top_left[1] + tile_size - 1, :] = BLACK
        im_array[top_left[0], top_left[1] + 1:top_left[1] + tile_size - 1:3, :] = color
    if direction == 's':
        im_array[top_left[0] + tile_size - 1, top_left[1] + 1:top_left[1] + tile_size - 1, :] = BLACK
        im_array[top_left[0] + tile_size - 1, top_left[1] + 1:top_left[1] + tile_size - 1:3, :] = color


# functions to aid in map creation
def make_doors_2_sided(d_map):
    m_rows, m_cols = np.shape(d_map)

    for row in range(m_rows):  # search through tiles
        for col in range(m_cols):
            if d_map[row][col].doors:  # if a tile has doors
                for door in d_map[row][col].doors:  # go through them
                    tile = get_adjacent_tile(row, col, door.direction, d_map)  # get adjacent tile
                    tile.spawn_door(OPPOSITE_DIRECTIONS[door.direction],
                                    door.type)  # make a companion door (so they're 2 sided)


def get_adjacent_tile(row, col, direction, d_map):
    if direction == "n" and row <= np.shape(d_map)[0] - 1:
        tile = d_map[row + 1][col]
    elif direction == "e" and col <= np.shape(d_map)[1] - 1:
        tile = d_map[row][col + 1]
    elif direction == "s" and row > 0:
        tile = d_map[row - 1][col]
    elif direction == "w" and col > 0:
        tile = d_map[row][col - 1]
    else:
        raise ValueError("Can't get tile adjacent to %d, %d in map creation." % (row, col))
    return tile


# functions for interacting with the dungeon
def move_player(dungeon_map, player_pos, direction):
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
        return True
    else:
        return False


# These functions are called externally so we make this floor's properties global
# so they can be called without knowledge of which floor they're being called on
def make_action(command, dungeon, player, tile_size):
    text = []
    im_path = get_image_path()
    tile = dungeon.map[player.pos[0]][player.pos[1]]

    # check for spooktober end
    print(player.letter_tiles)
    print(player.pos)
    print(command)
    print()
    if len(player.letter_tiles) == 5 and player.pos == [1, 7] and command == "quoth":
        player.pos = [1, 8] # TODO: Use goal pos from dungeon?
        return

    # key pickup
    if command == 'pickup key' and tile.has_key:
        player.small_keys += 1
        tile.has_key = False
        erase_key_icon(get_image_path(), player.pos, len(dungeon.map), tile_size)
        text.extend(['You pickup the a small, silver key.',
                     'It is heavily tarnished but you are confident it will still function.', ''])

    # move or open
    else:
        command = command.split(' ')
        if len(command) != 2:
            text.extend(["Command not understood", ''])
            return text

        cmd = command[0].lower()
        direction = command[1].lower()
        if cmd == 'move':
            old_pos = [p for p in player.pos]  # so we don't save a reference to player.pos
            if move_player(dungeon.map, player.pos, direction):
                erase_player(im_path, old_pos, len(dungeon.map), tile_size)
                if dungeon.map[player.pos[0]][player.pos[1]].special_text:
                    text.extend(dungeon.map[player.pos[0]][player.pos[1]].special_text)
                    text.extend([''])
                else:
                    text.extend(["You enter a dimly lit room", ''])
            else:
                text.extend(["There is no path in that direction", ''])
        elif cmd == 'open':
            text.extend(dungeon.open_door(tile, direction, player))
            text.extend([''])
        else:
            text.extend(["Command not understood", ''])
            return text

    draw_current_tile(dungeon.map, player, im_path, tile_size)
    return text


def interact(dungeon, player):
    return dungeon.interact(player)


def start_mini_game(command, dungeon, player):
    tile = get_current_tile(dungeon, player)
    if command == 'solve puzzle' and tile.has_creature:
        tile.creature.started_game = True
        return True
    return False


def mini_game_guess(player_guess, dungeon, player, tile_size):
    tile = get_current_tile(dungeon, player)
    print(f'Do we have a creature?: {tile.has_creature}')
    print(f'player at: {player.pos}')
    print(f'Tile is: {tile}')
    if tile.has_creature:
        solved, text = tile.creature.interact(player, player_guess)
        if solved:
            tile.despawn_creature()
            erase_key_icon(get_image_path(), player.pos, len(dungeon.map), tile_size)
        return solved, text


def mini_game_text(dungeon, player):
    tile = dungeon.map[player.pos[0]][player.pos[1]]
    return tile.creature.main_text


def check_win(dungeon, player):
    return player.pos == dungeon.goal_pos_arr[0]


def get_current_tile(dungeon, player):
    return dungeon.map[player.pos[0]][player.pos[1]]


def get_image_path():
    # make the map image and designate it as the current level image
    return Path('static/img/curr_level.png').absolute()
