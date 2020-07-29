from dungeon_classes.door_class import Door

DIRECTIONS = ["n", "e", "s", "w"]
STAIR_DIRECTIONS = ["u", "d"]


class Tile:

    def __init__(self, paths=None, has_key=False, doors=None, door_types=None, stairs=None):  # empty room

        # Make all the paths
        self.paths = []
        if paths:
            for direction in paths:
                self.add_path(direction)

        # Check for a key
        self.has_key = has_key

        # Make all the doors
        self.doors = []
        if doors and door_types and len(doors) != len(door_types):
            raise ValueError("door directions and door types must be the same length when creating a tile.")
        if doors is not None:
            for i, direction in enumerate(doors):
                self.spawn_door(direction, door_types[i])

        # add stairs
        self.stairs = None
        if stairs is not None:
            self.spawn_stairs(stairs)

        # creatures are spawned separately
        self.has_creature = False
        self.creature = None

        # text added after
        self.special_text = None

    # path functions
    def add_paths(self, directions):
        for direction in directions:
            self.add_path(direction)

    def add_path(self, direction):
        if direction not in DIRECTIONS:
            raise ValueError("%s is not a valid direction for a path" % direction)
        elif direction not in self.paths:
            self.paths.append(direction)

    def remove_path(self, direction):
        if direction not in direction:
            raise ValueError("%s is not a valid direction for a path" % direction)
        elif direction in self.paths:
            self.paths.remove(direction)

    # door functions
    def spawn_door(self, direction, door_type):
        doorDirections = [door.direction for door in self.doors]
        if direction not in DIRECTIONS:
            raise ValueError("%s is not a valid direction for a door" % direction)
        elif direction not in doorDirections:
            self.doors.append(Door(direction, door_type))
            if direction in self.paths:
                self.remove_path(direction)

    def despawn_door(self, direction):
        doorDirections = [door.direction for door in self.doors]
        if direction not in doorDirections:
            raise ValueError("There is not a door to the %s, yet you tried to open one..." % direction)
        index = doorDirections.index(direction)
        self.doors.pop(index)
        self.add_path(direction)

    # stair functions
    def spawn_stairs(self, stair):
        if stair not in STAIR_DIRECTIONS:
            raise ValueError("Stairs must either go up or down")
        self.stairs = stair

    # creature functions
    def spawn_creature(self, creature):
        self.has_creature = True
        self.creature = creature

    def despawn_creature(self):
        self.has_creature = False
        self.creature = None

    # unique text functions
    def add_special_text(self, text):
        self.special_text = text
