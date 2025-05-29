import math

class Point:
    def __init__(self, x, y, w):
        self.point = (x, y, w)
        self.x = x
        self.y = y
        self.w = w

class Coordinates:
    def __init__(self, max_points=4):
        self.max_points = max_points
        self.points = {}  # Key=position 1-max_points, Value=Point

    def __iter__(self):
        # Return iterator over points in order of position
        return iter([self.points[i] for i in sorted(self.points.keys())])

    def set_points(self, points):
        self.clear()
        for i, point in enumerate(points):
            self.points[i] = point

    def add_point(self, x, y, w):
        pos = self.get_next_position()
        if pos is not None:
            self.points[pos] = Point(x, y, w)
            return True
        return False

    def get_next_position(self):
        for i in range(0, self.max_points):
            if i not in self.points:
                return i
        return None

    def remove_point_near(self, x, y, threshold=20):
        """Removes a point near the given coordinates"""
        for i, p in self.points.items():
            distance = math.sqrt((p.x - x) ** 2 + (p.y - y) ** 2)
            if distance < threshold:
                del self.points[i]
                return True
        return False

    def get_points(self):
        # Return points in order by position
        return [self.points[i] for i in sorted(self.points.keys())]

    def clear(self):
        self.points = {}  # Changed from [] to {} to match the dictionary structure

    def is_complete(self):
        return len(self.points) == self.max_points and all(i in self.points for i in range(0, self.max_points))