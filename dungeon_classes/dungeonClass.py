import numpy as np

from dungeon_classes.door_class import Door

import dungeon_floors.floor_1 as floor_1

DIRECTIONS = ["n", "e", "s", "w"]
OPPOSITE_DIRECTIONS = {"n": "s", "e": "w", "s": "n", "w": "e"}


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

        if currTile.specialText == None:
            text.append("You enter a dimly lit room.")
        else:
            text.append(currTile.specialText)
            currTile.specialText = None

        # if currTile.hasCreature:
        #     self.creatureInteract(currTile, player)
        #
        # if currTile.hasKey:
        #     self.keyInteract(currTile, player)

        if len(currTile.doors) > 0:
            text.append(self.doorInteract(currTile, player))

        # if currTile.stairs is not None:
        #     if self.acknowledgeStairs:
        #         usedStairs = self.stairInteract(currTile, player)
        #     else:
        #         self.acknowledgeStairs = True

        if not usedStairs:
            text.append(self.choosePath(currTile, player))

        return '\n'.join(text)

    def creatureInteract(self, currTile, player):
        currTile.creature.interact(player)
        if currTile.creature.game.won:
            currTile.despawnCreature()

    def keyInteract(self, currTile, player):
        decided = False

        while not decided:
            takeKey = input(
                "A key lies in the center of the room. Would you like to pick it up (y/n)? ").strip().lower()

            if takeKey == "y":
                currTile.hasKey = False
                player.smallKeys += 1
                decided = True
                print("You pick up the key. It is shiny")

            elif takeKey == "n":
                decided = True
                print("You leave the key on the floor, wary of its alluring shimmer")

            else:
                print("please answer yes or no (y/n).")

    def doorInteract(self, currTile, player):
        text = []
        doorDIRECTIONS = [door.direction for door in currTile.doors if door.type != "t"]
        realDoor = False

        for door in currTile.doors:
            if door.type == "w":
                text.append(f"There is a wooden door to the {door.direction}.")
                realDoor = True
            elif door.type == "g":
                text.append(f"There is a large, golden door to the{door.direction}")
                text.append("It glows almost hungrily, casting more light than you would think possible.")
                realDoor = True

        return "\n".join(text)

        # if realDoor:
        #     if player.smallKeys + player.largeKeys > 0:
        #         decidedToStop = False
        #         while not decidedToStop and len(currTile.doors) > 0:
        #             if player.smallKeys + player.largeKeys < 1:
        #                 print(
        #                     "Doors remain, but you are out of keys. Maybe in the future you can vanquish all of them, but not today.")
        #                 decidedToStop = True
        #                 continue
        #
        #             decision = input("Would you like to attempt to unlock a door (y/n)? ").strip().lower()
        #
        #             if decision == "y":
        #                 decidedWhere = False
        #
        #                 while not decidedWhere:
        #                     if len(doorDIRECTIONS) > 1:
        #                         where = input("Which one (%s)? " % (','.join(doorDIRECTIONS))).strip().lower()
        #                     else:
        #                         where = doorDIRECTIONS[0]
        #
        #                     if where in doorDIRECTIONS:
        #                         numDoors = len(currTile.doors)
        #                         index = doorDIRECTIONS.index(where)
        #                         self.openDoor(currTile, currTile.doors[index], player)
        #                         if len(currTile.doors) < numDoors:  # success!
        #                             doorDIRECTIONS.pop(index)
        #                             print("The door slides open on rusty hinges.")
        #                             print("Your eyes close instinctively at as the grating sound hits your ears.")
        #                             print(
        #                                 "The sound stops and upon opening your eyes again you see it has disappeared.")
        #                         decidedWhere = True
        #                     else:
        #                         print("There is no door in that direction.")
        #
        #             elif decision == "n":
        #                 print("You leave the door where it is. Wary of its very presence.")
        #                 decidedToStop = True
        #
        #             else:
        #                 print("Please answer yes or no (y/n).")
        #     else:
        #         print("Unfortunately you have no keys. You stand there, your keyless impotence filling the room.")

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
        decided = False

        if len(currTile.paths) == 1:
            return f"There is a path to the {currTile.paths[0]}"
        else:
            return f"There are paths to the {', '.join(map(str, currTile.paths))}"

        # while not decided:
        #
        #     nextDir = input(
        #         "Would you like to move forward (%s)? " % ', '.join(map(str, currTile.paths))).strip().lower()
        #
        #     if nextDir in currTile.paths:
        #
        #         for door in currTile.doors:
        #             if door.direction == nextDir and door.type == "t":
        #                 print()
        #                 print("As you move through the pathways you hear a low rumbling.")
        #                 print("Turning around you see a door slide from the sealing, closing the path behind you.")
        #                 print(
        #                     "You knock on the door and upon determining that it is in fact solid you decide there is nothing to do but soldier on")
        #                 input("Press Enter to conitinue.").strip().lower()
        #                 newDoor = Door(nextDir, "w")
        #                 self.openDoor(currTile, door, player)
        #                 self.spawnDoor(currTile, newDoor, player.pos)
        #
        #         player.move(nextDir)
        #         decided = True
        #
        #     else:
        #         print("There is not a path in that direction.")
        #         print()


    # this opens the given door and it's companion (door in adjacent tile on the same wall)
    # necesary b/c doors come in pairs to make them 2 sided and tiles are independant.
    def openDoor(self, tile, door, player):
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
            tile.despawnDoor(door.direction)
            adjacentTile = self.getAdjacentTile(player.pos, door.direction)
            adjacentTile.despawnDoor(OPPOSITE_DIRECTIONS[door.direction])

        else:
            print(
                "Your are unable to open the door. It stands there, mocking you. You swear you will return one day to vanquish it.")
            print()

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
