import math

class Point:
    def __init__(self, x, y, w):
        self.point = (x, y, w)
        self.x = x
        self.y = y

class Coordinates:
    def __init__(self, max_points=4):
        self.max_points = max_points
        self.points = []

    def set_points(self, points):
        self.clear()
        self.points = points
        self.order_points()

    def add_point(self, x, y, w):
        if len(self.points) < self.max_points:
            self.points.append(Point(x, y, w))
            self.order_points()
            return True
        return False

    def remove_point_near(self, x, y, threshold=20):
        """Elimina un punto cercano a las coordenadas dadas"""
        for i, p in enumerate(self.points):
            distance = math.sqrt((p.x - x) ** 2 + (p.y - y) ** 2)
            if distance < threshold:
                self.points.pop(i)
                return True
        return False

    def order_points(self):
        # 1 ----- 2
        # |       |
        # |       |
        # 3 ----- 4
        cx = sum(p.x for p in self.points) / len(self.points)
        cy = sum(p.y for p in self.points) / len(self.points)

        self.points = sorted(self.points, key=lambda p: (
            -1 if p.y <= cy else 1,  # Primero separar arriba/abajo
            -p.x if p.x <= cx else p.x  # Luego izquierda/derecha
        ))

    def clear(self):
        self.points = []

    def is_complete(self):
        return len(self.points) == self.max_points

    def get_points(self):
        return self.points.copy()