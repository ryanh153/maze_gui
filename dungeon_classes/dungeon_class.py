import numpy as np

DIRECTIONS = ["n", "e", "s", "w"]
OPPOSITE_DIRECTIONS = {"n": "s", "e": "w", "s": "n", "w": "e"}
PRINT_DIR = {'n': 'north', 'e': 'east', 's': 'south', 'w': 'west'}


def key_interact():
    text = ["A silver keys lies on the ground in front of you.",
            "Enter 'pickup key' to retrieve it",
            ""]
    return text


def choose_path(curr_tile):
    text = []

    if len(curr_tile.paths) == 1:
        text.append(f"There is a path to the {PRINT_DIR[curr_tile.paths[0]]}")
    else:
        text.append(f"There are paths to the {', '.join(map(str, [PRINT_DIR[d] for d in curr_tile.paths]))}.")

    text.append(f"Would you like to move forward ({', '.join(map(str, curr_tile.paths))})?")
    text.append("")

    return text


def creature_interact(curr_tile, player):
    return curr_tile.creature.interact(player)
    # if curr_tile.creature.game.won:
    #     curr_tile.despawn_creature()


class Dungeon:

    def __init__(self, player, goal_pos_arr, start_pos_arr, passphrases, map_arr):
        self.goal_pos_arr = goal_pos_arr
        self.start_pos_arr = start_pos_arr
        self.passphrases = passphrases
        self.map_arr = map_arr
        self.level = 0
        self.map = self.map_arr[self.level]
        player.pos = self.start_pos_arr[self.level]
        if self.goal_pos_arr[self.level] is None:
            self.goalPos = None
        else:
            self.goalPos = self.goal_pos_arr[self.level]
        self.acknowledgeStairs = True

    def interact(self, player):

        text = []
        currTile = self.map[player.pos[0]][player.pos[1]]
        usedStairs = False

        if currTile.has_creature:
            text.extend(creature_interact(currTile, player))

        if currTile.has_key:
            text.extend(key_interact())

        if len(currTile.doors) > 0:
            text.extend(self.door_interact(player))

        if currTile.stairs is not None:
            if self.acknowledgeStairs:
                usedStairs = self.stair_interact(currTile, player)
            else:
                self.acknowledgeStairs = True

        if not usedStairs:
            text.extend(choose_path(currTile))

        return text

    def door_interact(self, player):
        text = []
        curr_tile = self.map[player.pos[0]][player.pos[1]]

        for door in curr_tile.doors:
            if door.type == "w":
                text.append(f"There is a wooden door to the {PRINT_DIR[door.direction]}.")
            elif door.type == "g":
                text.append(f"There is a large, golden door to the{PRINT_DIR[door.direction]}")
                text.append("It glows almost hungrily, casting more light than you would think possible.")

        if curr_tile.doors:
            if not (player.small_keys or player.large_keys):
                text.extend(["Unfortunately you have no keys.",
                             "You stand there, your keyless impotence filling the room."])
            else:
                if player.small_keys == 1:
                    text.append(f"You have one small key.")
                else:
                    text.append(f"You have {player.small_keys} small keys.")

                if player.large_keys == 1:
                    text.append("You have one large key.")
                else:
                    text.append(f"You have {player.large_keys} large keys.")

        return text

    def stair_interact(self, curr_tile, player):
        usedStairs = 0
        if curr_tile.stairs == "u":
            self.check_clear()
            print("On the far side of the room is a staircase leading upwards.")
            decided = False
            while not decided:
                goUp = input("Do you dare ascend from the depths of your current state (y/n)? ").strip().lower()
                if goUp == "y":
                    usedStairs = 1
                    print("You climb the stairs, hoping they bring you closer to escape.")
                    self.level = self.level + 1
                    decided = True
                    self.acknowledgeStairs = False
                    self.setup_new_floor(player)
                elif goUp == "n":
                    print("You stay where you are. There is more to explore here first.")
                    decided = True
                else:
                    print("Please answer yes or no (y/n).")

        elif curr_tile.stairs == "d":
            print("On the far side of the room is a staircase leading down.")
            decided = False
            while not decided:
                goDown = input("Do you return to the depths from whence you came (y/n)? ").strip().lower()
                if goDown == "y":
                    usedStairs = 1
                    print("You return to the chambers of your past torment. Hopefully for a good reason...")
                    self.level = self.level - 1
                    decided = True
                    self.setup_new_floor(player)
                elif goDown == "n":
                    print("You stay where you are. Maybe you can still find the way out of here...")
                    decided = True
                else:
                    print("Please answer yes or no (y/n).")

        else:
            raise ValueError("Ryan: stairs must lead up or down (u/d)... currently: %s" % curr_tile.stairs)
        return usedStairs

    def check_clear(self):
        cleared = True
        for rowNum, row in enumerate(self.map):
            for colNum, tile in enumerate(row):
                if tile.has_creature or len(tile.doors) != 0 or tile.has_key:
                    cleared = False
                    break
            if not cleared:
                break

        if cleared:
            print("You have cleared all obstacles on this floor. Congratulations!")
            print(
                f"If you would like to return to this state when starting the game simply enter the following "
                f"passphrase: {self.passphrases[self.level]}")
            print("This will clear all floors up to and including this one, and place you on the floor above.")
            print("Carry on noble adventurer!")
        else:
            print("You have reached the end of a floor, but have not cleared the floor.")
            print("If you do clear the floor (all puzzles completed, doors opened, and keys grabbed)")
            print("you will be rewarded with the ability to warp to the end of this floor when the game is started!")

    # this opens the given door and it's companion (door in adjacent tile on the same wall)
    # necessary b/c doors come in pairs to make them 2 sided and tiles are independent.
    def open_door(self, tile, direction, player):
        text = list()

        for door in tile.doors:
            if direction == door.direction:
                break
        else:
            text.append("There is no door in that direction.")
            return text

        canOpen = False
        if door.type == "w" and player.small_keys > 0:
            canOpen = True
            player.small_keys = player.small_keys - 1
        elif door.type == "g" and player.large_keys > 0:
            canOpen = True
            player.large_keys = player.large_keys - 1
        elif door.type == "t":
            canOpen = True  # traps need to be despawned. Only done by dungeon.

        if canOpen:
            tile.despawn_door(door.direction)
            adjacentTile = self.get_adjacent_tile(player.pos, door.direction)
            adjacentTile.despawn_door(OPPOSITE_DIRECTIONS[door.direction])
            text.append("The door slides open on rusty hinges.")
            text.append("Your eyes close instinctively at as the grating sound hits your ears.")
            text.append("The sound stops and upon opening your eyes again you see it has disappeared.")

        else:
            text.append("Your are unable to open the door. It stands there, mocking you.")
            text.append("You swear you will return one day to vanquish it.")

        return text

    def spawn_door(self, tile, door, curr_pos):
        tile.spawn_door(door.direction, door.type)
        tile.removePath(door.direction)

        adjacentTile = self.get_adjacent_tile(curr_pos, door.direction)
        adjacentTile.spawn_door(OPPOSITE_DIRECTIONS[door.direction], door.type)
        adjacentTile.removePath(OPPOSITE_DIRECTIONS[door.direction])

    def get_adjacent_tile(self, pos, direction):
        if direction == "n" and pos[0] <= np.shape(self.map)[0] - 1:
            tile = self.map[pos[0] + 1][pos[1]]
        elif direction == "e" and pos[1] <= np.shape(self.map)[1] - 1:
            tile = self.map[pos[0]][pos[1] + 1]
        elif direction == "s" and pos[0] > 0:
            tile = self.map[pos[0] - 1][pos[1]]
        elif direction == "w" and pos[1] > 0:
            tile = self.map[pos[0]][pos[1] - 1]
        else:
            raise ValueError("Can't get tile adjacent to %d, %d in map creation." % (pos[0], pos[1]))
        return tile

    # Setting up after a level change
    def setup_new_floor(self, player):

        self.map = self.map_arr[self.level]  # load new map
        self.start_pos_arr[self.level - 1] = player.pos  # if you come back you return to the stairs
        player.pos = self.start_pos_arr[self.level]  # put the player at the start of the new floor

        # if the goal is on this floor, set it.
        if self.goal_pos_arr[self.level] is None:
            self.goalPos = None
        else:
            self.goalPos = self.goal_pos_arr[self.level]

    # Clear floors, allowing you to warp to a level with all puzzles up to that point completed.
    # This clears floor one, placing player on floor two.
    def clear_floors(self, player, starting_floor):
        self.level = 0
        self.map = self.map_arr[self.level]
        while self.level != starting_floor:
            # clear creatures and get keys
            for rowNum, row in enumerate(self.map):
                for colNum, tile in enumerate(row):
                    if tile.has_creature:
                        player.pos = [rowNum, colNum]
                        tile.creature.interact(player, auto_win=True)
                        tile.despawn_creature()

                    if tile.has_key:
                        player.small_keys += 1
                        tile.has_key = False

            # clear doors and use keys. Also save stair position so we can set that
            stair_pos = None
            for rowNum, row in enumerate(self.map):
                for colNum, tile in enumerate(row):
                    for doorIter, door in enumerate(tile.doors):
                        if door.type == 'w' or 't':
                            player.pos = [rowNum, colNum]
                            self.open_door(tile, door, player)
                        elif door.type == 'g':
                            self.open_door(tile, door, player)

                    if tile.stairs is not None:
                        stair_pos = [rowNum, colNum]

            print("You have cleared floor %d" % (self.level + 1))
            print()

            if stair_pos is None:
                raise ValueError("Did not find a staircase on a floor that was trying to be cleared...")
            else:
                player.pos = stair_pos  # put the player on the stairs
                self.level = self.level + 1  # move up
                self.setup_new_floor(player)

        self.acknowledgeStairs = False
        print("Starting on floor %d!" % (self.level + 1))
        print()
