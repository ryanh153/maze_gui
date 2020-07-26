from dungeon_classes.door_class import Door

directions = ["n", "e", "s", "w"]
stairDirections = ["u", "d"]


class Tile:

    def __init__(self, paths=[], has_key=False, doors=[], door_types=[], stairs=None):  # empty room

        # Make all the paths
        self.paths = []
        if paths:
            for direction in paths:
                self.add_path(direction)

        # Check for a key
        self.has_key = has_key

        # Make all the doors
        self.doors = []
        if len(doors) != len(door_types):
            raise ValueError("door directions and door types must be the same length when creating a tile.")
        if doors is not []:
            for i, direction in enumerate(doors):
                self.spawn_door(direction, door_types[i])

        # add stairs
        self.stairs = None
        if stairs is not None:
            self.spawnStairs(stairs)

        # creatures are spawned seperately
        self.hasCreature = False
        self.creature = None

        # text added after
        self.special_text = None

    # path functions
    def add_paths(self, directions):
        for direction in directions:
            self.add_path(direction)

            
    def add_path(self, direction):
        if direction not in directions:
            raise ValueError("%s is not a valid direction for a path" % (direction))
        elif direction not in self.paths:
            self.paths.append(direction)

    def remove_path(self, direction):
        if direction not in direction:
            raise ValueError("%s is not a valid direction for a path" % (direction))
        elif direction in self.paths:
            self.paths.remove(direction)

    # door functions
    def spawn_door(self, direction, doorType):
        doorDirections = [door.direction for door in self.doors]
        if direction not in directions:
            raise ValueError("%s is not a valid direction for a door" % (direction))
        elif direction not in doorDirections:
            self.doors.append(Door(direction, doorType))
            if direction in self.paths:
                self.remove_path(direction)

    def despawn_door(self, direction):
        doorDirections = [door.direction for door in self.doors]
        if direction not in doorDirections:
            raise ValueError("There is not a door to the %s, yet you tried to open one..." % (direction))
        index = doorDirections.index(direction)
        self.doors.pop(index)
        self.add_path(direction)

    # stair functions
    def spawnStairs(self, stair):
        if stair not in stairDirections:
            raise ValueError("Stairs must either go up or down")
        self.stairs = stair

    # creature functions
    def spawnCreature(self, creature):
        self.hasCreature = True
        self.creature = creature

    def despawnCreature(self):
        self.hasCreature = False
        self.creature = None

    # unique text functions
    def addSpecialText(self, text):
        self.special_text = text
