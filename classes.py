import math

class Punto:
    def __init__(self, x, y):
        self.x = x
        self.y = y
    def to_tuple(self):
        return (self.x, self.y)

class PuntoProyectivo:
    def __init__(self, inf, x, y):
        self.inf = inf #0/1 que define si está o no en la recta del infinito
        self.x = x
        self.y = y

    @classmethod
    def proyectar(cls, inf, punto):
        return cls(inf, punto.x, punto.y)

class Coordenadas:
    def __init__(self, max_points=4):
        self.max_points = max_points
        self.points = []

    def add_point(self, x, y):
        if len(self.points) < self.max_points:
            self.points.append(Punto(x, y))
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
        if len(self.points) != 4:
            return

        cx = sum(p.x for p in self.points) / 4
        cy = sum(p.y for p in self.points) / 4

        def angle_from_center(p):
            return math.atan2(p.y - cy, p.x - cx)

        # Ordenar en sentido horario desde el ángulo más negativo
        self.points.sort(key=angle_from_center)

    def clear(self):
        self.points = []

    def is_complete(self):
        return len(self.points) == self.max_points

    def get_points(self):
        return self.points.copy()