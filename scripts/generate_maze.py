from random import shuffle, randrange, seed
import numpy as np
from PIL import Image
import os

from dungeon_classes.tile_class import Tile

WHITE = (255, 255, 255)
BROWN = (153, 102, 51)
GREEN = (0, 204, 0)


def make_maze(numRows, numCols, randSeed=None):
    seed(randSeed)
    vis = [[0] * numCols for _ in range(numRows)]
    dMap = [[Tile("") for _ in range(numCols)] for _ in range(numRows)]
    ver = [["|  "] * numCols + ['|'] for _ in range(numRows)] + [[]]
    hor = [["+--"] * numCols + ['+'] for _ in range(numRows + 1)]

    def drawMap():
        s = ""
        for (a, b) in zip(ver[::-1], hor[::-1]):  # vertical flip b/c my map convention is (0,0) is bottom left
            s += ''.join(a + ['\n'] + b + ['\n'])
        return s

    def walk(row, col):
        s = drawMap()

        vis[row][col] = 1

        d = [(row - 1, col), (row, col + 1), (row + 1, col), (row, col - 1)]
        shuffle(d)
        for (nextRow, nextCol) in d:
            if nextRow < 0 or nextCol < 0 or nextRow >= numRows or nextCol >= numCols or vis[nextRow][nextCol]: continue
            if nextCol == col:
                hor[max(row, nextRow)][col] = "+  "
                removeWall(row, nextRow, col, nextCol, dMap)
            if nextRow == row:
                ver[row][max(col, nextCol)] = "   "
                removeWall(row, nextRow, col, nextCol, dMap)
            walk(nextRow, nextCol)

    walk(randrange(numRows), randrange(numCols))
    s = drawMap()
    return s, dMap


def removeWall(row, nextRow, col, nextCol, dMap):
    dirs = ['n', 'e', 's', 'w']
    oppDirs = ['s', 'w', 'n', 'e']

    if nextRow > row:
        dirIndx = 0
    elif nextRow < row:
        dirIndx = 2
    elif nextCol > col:
        dirIndx = 1
    elif nextCol < col:
        dirIndx = 3
    else:
        raise ValueError("In map generator. Didn't move?")

    dMap[row][col].addPath(dirs[dirIndx])
    dMap[nextRow][nextCol].addPath(oppDirs[dirIndx])


def make_map_image(dungeon_map, player_pos, tile_size=50):
    maze_dim = len(dungeon_map)
    im_size = maze_dim * tile_size
    im_array = np.zeros([im_size, im_size, 3], dtype=np.uint8)

    draw_player(im_array, player_pos, maze_dim, tile_size)

    for r, row in enumerate(reversed(dungeon_map)):
        for c, tile in enumerate(row):
            top_corner = (tile_size * r, tile_size * c)
            draw_tile(im_array, tile, tile_size, top_corner)
    im = Image.fromarray(im_array)
    print(os.getcwd())
    im.save('static/img/curr_level.png')


def draw_player(im_array, pos, maze_dim, tile_size):
    row, col = maze_dim - (pos[0] + 1), pos[1]
    top_corner = (tile_size * row, tile_size * col)
    padding = 15
    im_array[top_corner[0] + padding:top_corner[0] + tile_size - padding,
    top_corner[1] + padding:top_corner[1] + tile_size - padding, :] = GREEN


def draw_tile(im_array, tile, tile_size, top_corner):
    directions = ['n', 'e', 's', 'w']
    for direction in directions:
        if direction not in tile.paths:
            draw_tile_side(im_array, direction, top_corner, tile_size, WHITE)

    for door in tile.doors:
        draw_tile_side(im_array, door.direction, top_corner, tile_size, BROWN)


def draw_tile_side(im_array, direction, top_corner, tile_size, color=WHITE):
    if direction == 'w':
        im_array[top_corner[0]:top_corner[0] + tile_size, top_corner[1], :] = color
    if direction == 'e':
        im_array[top_corner[0]:top_corner[0] + tile_size, top_corner[1] + tile_size - 1, :] = color
    if direction == 'n':
        im_array[top_corner[0], top_corner[1]:top_corner[1] + tile_size, :] = color
    if direction == 's':
        im_array[top_corner[0] + tile_size - 1, top_corner[1]:top_corner[1] + tile_size, :] = color


if __name__ == '__main__':
    maze_dim = 5
    s, d_map = make_maze(maze_dim, maze_dim, 10044)
    im_size = 300
    tile_size = int(im_size / maze_dim)
    im_array = np.zeros([im_size, im_size, 3], dtype=np.uint8)

    for r, row in enumerate(reversed(d_map)):
        for c, tile in enumerate(row):
            top_corner = (tile_size * r, tile_size * c)
            draw_tile(im_array, tile, top_corner)
    im = Image.fromarray(im_array)
    im.save('../static/img/curr_level.png')
    print(s)
