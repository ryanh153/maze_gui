# small/normal, large, and trap
doorTypes = ["w", "g", "t"]


class Door:

    def __init__(self, direction, door_type):
        if door_type in doorTypes:
            self.direction = direction
            self.type = door_type
        else:
            raise ValueError("Trying to spawn invalid door. direction: %s, type: %s" % (direction, door_type))
