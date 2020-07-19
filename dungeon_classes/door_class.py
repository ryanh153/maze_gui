# small/normal, large, and trap
doorTypes = ["w", "g", "t"]


class Door:

    def __init__(self, direction, doorType):
        if doorType in doorTypes:
            self.direction = direction
            self.type = doorType
        else:
            raise ValueError("Trying to spawn invalid door. direction: %s, type: %s" % (direction, doorType))
