import math

class Punto:
    def __init__(self, x, y):
        self.x = x
        self.y = y

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

    # Ordena los puntos en sentido horario comenzando por la esquina top izquierda
    def order_points(self):
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
