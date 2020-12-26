class Coordinate:
    def __init__(self, x, y):
        """
        constructor for the coordinate class
        :param x: the x-coordinate
        :param y: the y-coordinate
        """
        self.x = x
        self.y = y

    def calculate_manhatten_distance(self, destination) -> float:
        return abs(self.x - destination.x) + abs(self.y - destination.y)

    def __repr__(self) -> str:
        return f'({self.x}, {self.y})'


