import numpy as np
from PIL import Image
import os

WHITE = (255, 255, 255)
BROWN = (153, 102, 51)
GREEN = (0, 204, 0)

OPPOSITE_DIRECTIONS = {"n": "s", "e": "w", "s": "n", "w": "e"}


# Functions for generating an image from a map
def make_map_image(dungeon_map, player_pos, im_path, tile_size=50):
    maze_dim = len(dungeon_map)
    im_size = maze_dim * tile_size
    im_array = np.zeros([im_size, im_size, 3], dtype=np.uint8)

    draw_player(im_array, player_pos, maze_dim, tile_size)

    for r, row in enumerate(reversed(dungeon_map)):
        for c, tile in enumerate(row):
            top_left = (tile_size * r, tile_size * c)
            draw_tile(im_array, tile, tile_size, top_left)
    im = Image.fromarray(im_array)
    print(os.getcwd())
    im.save(im_path)


def draw_player(im_array, pos, maze_dim, tile_size):
    row, col = maze_dim - (pos[0] + 1), pos[1]
    top_left = (tile_size * row, tile_size * col)
    pad = 15
    im_array[top_left[0]+pad:top_left[0]+tile_size-pad, top_left[1]+pad:top_left[1]+tile_size-pad, :] = GREEN


def draw_tile(im_array, tile, tile_size, top_left):
    directions = ['n', 'e', 's', 'w']
    for direction in directions:
        if direction not in tile.paths:
            draw_tile_side(im_array, direction, top_left, tile_size, WHITE)

    for door in tile.doors:
        draw_tile_side(im_array, door.direction, top_left, tile_size, BROWN)


def draw_tile_side(im_array, direction, top_left, tile_size, color=WHITE):
    if direction == 'w':
        im_array[top_left[0]:top_left[0] + tile_size, top_left[1], :] = color
    if direction == 'e':
        im_array[top_left[0]:top_left[0] + tile_size, top_left[1] + tile_size - 1, :] = color
    if direction == 'n':
        im_array[top_left[0], top_left[1]:top_left[1] + tile_size, :] = color
    if direction == 's':
        im_array[top_left[0] + tile_size - 1, top_left[1]:top_left[1] + tile_size, :] = color


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
