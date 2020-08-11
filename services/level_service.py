from collections import namedtuple

import numpy as np
from PIL import Image

WHITE = (255, 255, 255)
BROWN = (153, 102, 51)
GREEN = (0, 204, 0)
BLACK = (0, 0, 0)

OPPOSITE_DIRECTIONS = {"n": "s", "e": "w", "s": "n", "w": "e"}

Icon = namedtuple('Image', ['image', 'height', 'width', 'padding'])
PLAYER_IMAGE = np.array(Image.open('static/img/test_char.jpg'))
PLAYER_ICON = Icon(PLAYER_IMAGE, np.shape(PLAYER_IMAGE)[0], np.shape(PLAYER_IMAGE)[1], 2)

KEY_IMAGE = np.array(Image.open('static/img/key.png'))[:, :, 0:3]
KEY_ICON = Icon(KEY_IMAGE, np.shape(KEY_IMAGE)[0], np.shape(KEY_IMAGE)[1], 2)


# Functions for generating an image from a map
def make_black_map(dungeon_map, player_pos, im_path, tile_size=50):
    im_size = len(dungeon_map) * tile_size
    im_array = np.zeros([im_size, im_size, 3], dtype=np.uint8)

    im = Image.fromarray(im_array)
    im.save(im_path)


def draw_current_tile(dungeon_map, player_pos, im_path, tile_size):
    im_array = np.array(Image.open(im_path))
    maze_dim = len(dungeon_map)

    top_left = (tile_size * (maze_dim - player_pos[0] - 1), tile_size * player_pos[1])
    tile = dungeon_map[player_pos[0]][player_pos[1]]
    draw_tile(im_array, tile, tile_size, top_left)

    draw_player(im_array, player_pos, maze_dim, tile_size)
    if tile.has_key or tile.has_creature:
        draw_key_icon(im_array, player_pos, maze_dim, tile_size)

    im = Image.fromarray(im_array)
    im.save(im_path)


def make_full_map(dungeon_map, player_pos, im_path, tile_size=50):
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


def draw_key_icon(im_array, pos, maze_dim, tile_size):
    top_left = get_top_left(maze_dim, tile_size, pos)
    im_array[top_left[0] + KEY_ICON.padding:
             top_left[0] + KEY_ICON.padding + KEY_ICON.height,
             top_left[1] + tile_size - KEY_ICON.width - KEY_ICON.padding:
             top_left[1] + tile_size - KEY_ICON.padding,
             :] = KEY_ICON.image


def erase_key_icon(im_path, pos, maze_dim, tile_size):
    im_array = np.array(Image.open(im_path))
    top_left = get_top_left(maze_dim, tile_size, pos)
    im_array[top_left[0] + KEY_ICON.padding:
             top_left[0] + KEY_ICON.padding + KEY_ICON.height,
             top_left[1] + tile_size - KEY_ICON.width - KEY_ICON.padding:
             top_left[1] + tile_size - KEY_ICON.padding,
             :] = BLACK

    save_image(im_array, im_path)


def draw_tile(im_array, tile, tile_size, top_left):
    directions = ['n', 'e', 's', 'w']
    for direction in directions:
        if direction in tile.paths:
            draw_tile_side_short(im_array, direction, top_left, tile_size, WHITE)
        else:
            draw_tile_side(im_array, direction, top_left, tile_size, WHITE)

    for door in tile.doors:
        draw_tile_side(im_array, door.direction, top_left, tile_size, BROWN)


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
        im_array[top_left[0] + 1:top_left[0] + tile_size - 1:2, top_left[1], :] = color
    if direction == 'e':
        im_array[top_left[0] + 1:top_left[0] + tile_size - 1, top_left[1] + tile_size - 1, :] = BLACK
        im_array[top_left[0] + 1:top_left[0] + tile_size - 1:2, top_left[1] + tile_size - 1, :] = color
    if direction == 'n':
        im_array[top_left[0], top_left[1] + 1:top_left[1] + tile_size - 1, :] = BLACK
        im_array[top_left[0], top_left[1] + 1:top_left[1] + tile_size - 1:2, :] = color
    if direction == 's':
        im_array[top_left[0] + tile_size - 1, top_left[1] + 1:top_left[1] + tile_size - 1, :] = BLACK
        im_array[top_left[0] + tile_size - 1, top_left[1] + 1:top_left[1] + tile_size - 1:2, :] = color


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
