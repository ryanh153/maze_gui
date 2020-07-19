import numpy as np

from dungeon_classes.door_class import Door

import dungeon_floors.floor_1 as floor_1

DIRECTIONS = ["n", "e", "s", "w"]
OPPOSITE_DIRECTIONS = {"n": "s", "e": "w", "s": "n", "w": "e"}
PRINT_DIR = {'n': 'north', 'e': 'east', 's': 'south', 'w': 'west'}


class Dungeon:

    def __init__(self, player, goalPosArr, startPosArr, passphrases, mapArr):
        self.goalPosArr = goalPosArr
        self.startPosArr = startPosArr
        self.passphrases = passphrases
        self.mapArr = mapArr
        self.level = 0
        self.map = self.mapArr[self.level]
        player.pos = self.startPosArr[self.level]
        if self.goalPosArr[self.level] is None:
            self.goalPos = None
        else:
            self.goalPos = self.goalPosArr[self.level]
        self.acknowledgeStairs = True

    def interact(self, player):

        text = []
        currTile = self.map[player.pos[0]][player.pos[1]]
        usedStairs = 0

        if currTile.specialText is None:
            text.append("You enter a dimly lit room.")
        else:
            text.append(currTile.specialText)
            currTile.specialText = None

        if currTile.hasCreature:
            self.creatureInteract(currTile, player)

        if currTile.hasKey:
            text.extend(self.keyInteract())

        if len(currTile.doors) > 0:
            text.extend(self.doorInteract(currTile, player))

        if currTile.stairs is not None:
            if self.acknowledgeStairs:
                usedStairs = self.stairInteract(currTile, player)
            else:
                self.acknowledgeStairs = True

        if not usedStairs:
            text.extend(self.choosePath(currTile, player))

        return text

    def creatureInteract(self, currTile, player):
        currTile.creature.interact(player)
        if currTile.creature.game.won:
            currTile.despawnCreature()

    def keyInteract(self):
        text = list()
        text.append("A silver keys lies on the ground in front of you.")
        text.append("Enter 'pickup key' to retrieve it")
        return text

    def doorInteract(self, currTile, player):
        text = []

        for door in currTile.doors:
            if door.type == "w":
                text.append(f"There is a wooden door to the {PRINT_DIR[door.direction]}.")
            elif door.type == "g":
                text.append(f"There is a large, golden door to the{PRINT_DIR[door.direction]}")
                text.append("It glows almost hungrily, casting more light than you would think possible.")

        if currTile.doors:
            if player.smallKeys == 1:
                text.append(f"You have one small key.")
            else:
                text.append(f"You have {player.smallKeys} small keys.")

            if player.largeKeys == 1:
                text.append("You have one large key.")
            else:
                text.append(f"You have {player.largeKeys} large keys.")

        return text


                    #     while not decidedWhere:
                    #         if len(doorDIRECTIONS) > 1:
                    #             where = input("Which one (%s)? " % (','.join(doorDIRECTIONS))).strip().lower()
                    #         else:
                    #             where = doorDIRECTIONS[0]
                    #
                    #         if where in doorDIRECTIONS:
                    #             numDoors = len(currTile.doors)
                    #             index = doorDIRECTIONS.index(where)
                    #             self.openDoor(currTile, currTile.doors[index], player)
                    #             if len(currTile.doors) < numDoors:  # success!
                    #                 doorDIRECTIONS.pop(index)
                    #                 print("The door slides open on rusty hinges.")
                    #                 print("Your eyes close instinctively at as the grating sound hits your ears.")
                    #                 print(
                    #                     "The sound stops and upon opening your eyes again you see it has disappeared.")
                    #             decidedWhere = True
                    #         else:
                    #             print("There is no door in that direction.")
                    #
                    #
                    # print("Unfortunately you have no keys. You stand there, your keyless impotence filling the room.")

    def stairInteract(self, currTile, player):
        usedStairs = 0
        if currTile.stairs == "u":
            self.checkClear()
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
                    self.setupNewFloor(player)
                elif goUp == "n":
                    print("You stay where you are. There is more to explore here first.")
                    decided = True
                else:
                    print("Please answer yes or no (y/n).")

        elif currTile.stairs == "d":
            print("On the far side of the room is a staircase leading down.")
            decided = False
            while not decided:
                goDown = input("Do you return to the depths from whence you came (y/n)? ").strip().lower()
                if goDown == "y":
                    usedStairs = 1
                    print("You return to the chambers of your past torment. Hopefully for a good reason...")
                    self.level = self.level - 1
                    decided = True
                    self.setupNewFloor(player)
                elif goDown == "n":
                    print("You stay where you are. Maybe you can still find the way out of here...")
                    decided = True
                else:
                    print("Please answer yes or no (y/n).")

        else:
            raise ValueError("Ryan: stairs must lead up or down (u/d)... currently: %s" % (currTile.stairs))
        return usedStairs

    def checkClear(self):
        cleared = True
        for rowNum, row in enumerate(self.map):
            for colNum, tile in enumerate(row):
                if tile.hasCreature or len(tile.doors) != 0 or tile.hasKey:
                    cleared = False
                    break
            if cleared == False:
                break

        if cleared:
            print("You have cleared all obstacles on this floor. Congratulations!")
            print(
                f"If you would like to return to this state when starting the game simply enter the following passphrase: {self.passphrases[self.level]}")
            print("This will clear all floors up to and including this one, and place you on the floor above.")
            print("Carry on noble adventurer!")
        else:
            print("You have reached the end of a floor, but have not cleared the floor.")
            print("If you do clear the floor (all puzzles completed, doors opened, and keys grabbed)")
            print("you will be rewarded with the ability to warp to the end of this floor when the game is started!")

    def choosePath(self, currTile, player):
        text = []

        if len(currTile.paths) == 1:
            text.append(f"There is a path to the {PRINT_DIR[currTile.paths[0]]}")
        else:
            text.append(f"There are paths to the {', '.join(map(str, [PRINT_DIR[d] for d in currTile.paths]))}.")

        text.append(f"Would you like to move forward ({', '.join(map(str, currTile.paths))})?")

        return text


    # this opens the given door and it's companion (door in adjacent tile on the same wall)
    # necesary b/c doors come in pairs to make them 2 sided and tiles are independant.
    def openDoor(self, tile, direction, player):
        # find door to open
        for door in tile.doors:
            if direction == door.direction:
                break
        else:
            door = None

        # open door
        if door is not None:
            canOpen = False
            if door.type == "w" and player.smallKeys > 0:
                canOpen = True
                player.smallKeys = player.smallKeys - 1
            elif door.type == "g" and player.largeKeys > 0:
                canOpen = True
                player.largeKeys = player.largeKeys - 1
            elif door.type == "t":
                canOpen = True  # traps need to be despawned. Only done by dungeon.

            if canOpen:
                tile.despawn_door(door.direction)
                adjacentTile = self.getAdjacentTile(player.pos, door.direction)
                adjacentTile.despawn_door(OPPOSITE_DIRECTIONS[door.direction])

            # else:
            #     print(
            #         "Your are unable to open the door. It stands there, mocking you. You swear you will return one day to vanquish it.")
            #     print()

    def spawnDoor(self, tile, door, currPos):
        tile.spawnDoor(door.direction, door.type)
        tile.removePath(door.direction)

        adjacentTile = self.getAdjacentTile(currPos, door.direction)
        adjacentTile.spawnDoor(OPPOSITE_DIRECTIONS[door.direction], door.type)
        adjacentTile.removePath(OPPOSITE_DIRECTIONS[door.direction])

    def getAdjacentTile(self, pos, direction):
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
    def setupNewFloor(self, player):

        self.map = self.mapArr[self.level]  # load new map
        self.startPosArr[self.level - 1] = player.pos  # if you come back you return to the staris
        player.pos = self.startPosArr[self.level]  # put the player at the start of the new floor

        # if the goal is on this floor, set it.
        if self.goalPosArr[self.level] == None:
            self.goalPos = None
        else:
            self.goalPos = self.goalPosArr[self.level]

    # Clear floors, allowing you to warp to a level with all puzzles up to that point completed.
    # This clears floor one, placing player on floor two.
    def clearFloors(self, player, startingFloor):
        self.level = 0
        self.map = self.mapArr[self.level]
        while self.level != startingFloor:
            # clear creatures and get keys
            for rowNum, row in enumerate(self.map):
                for colNum, tile in enumerate(row):
                    if tile.hasCreature:
                        player.pos = [rowNum, colNum]
                        tile.creature.interact(player, autoWin=True)
                        tile.despawnCreature()

                    if tile.hasKey:
                        player.smallKeys += 1
                        tile.hasKey = False

            # clear doors and use keys. Also save stair position so we can set that
            for rowNum, row in enumerate(self.map):
                for colNum, tile in enumerate(row):
                    for doorIter, door in enumerate(tile.doors):
                        if door.type == 'w' or 't':
                            player.pos = [rowNum, colNum]
                            self.openDoor(tile, door, player)
                        # print('small'
                        # print(player.smallKeys
                        # print(player.largeKeys
                        # print(''
                        elif door.type == 'g':
                            player.pos[rowNum, colNum]
                            self.openDoor(tile, door, player)
                        # print('large'
                        # print(player.smallKeys
                        # print(player.largeKeys
                        # print(''

                    if tile.stairs != None:
                        stairPos = [rowNum, colNum]

            print("You have cleared floor %d" % (self.level + 1))
            print()

            player.pos = stairPos  # put the player on the stairs
            self.level = self.level + 1  # move up
            self.setupNewFloor(player)

        self.acknowledgeStairs = False
        print("Starting on floor %d!" % (self.level + 1))
        print()
