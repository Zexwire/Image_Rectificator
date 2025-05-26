from classes.points import Point
import numpy as np

# TODO: Check el caso en el que dos de las líneas sean paralelas
def calculate_vanish_points(p1: Point, p2: Point, p3: Point, p4: Point) -> list[Point]:
    """
    Calcula la línea del infinito como la unión de los puntos de fuga de las líneas paralelas
    Devuelve dos puntos que definen la línea del infinito
    """
    # Calcular puntos de infinito como intersecciones de líneas opuestas
    p = intersection([p1, p2], [p3, p4])  # Intersección de lados opuestos 1-2 y 3-4
    q = intersection([p1, p3], [p2, p4])  # Intersección de lados opuestos 1-3 y 2-4

    # Verificar si alguno de los puntos es None (líneas paralelas)
    # En caso de serlo, TODO ver que narices hay que hacer aquí lol
    if p is None or q is None:
        raise ValueError("No se pudo calcular la línea del infinito (algunas líneas son paralelas)")

    return [p, q]


def intersection(r1, r2):
    """
    Calcula la intersección de dos líneas definidas por dos puntos cada una
    """
    x1, y1 = r1[0].x, r1[0].y
    x2, y2 = r1[1].x, r1[1].y
    x3, y3 = r2[0].x, r2[0].y
    x4, y4 = r2[1].x, r2[1].y

    # Line r1 in the form: a1*x + b1*y = c1
    a1 = y2 - y1
    b1 = x1 - x2
    c1 = a1 * x1 + b1 * y1

    # Line r2 in the form: a2*x + b2*y = c2
    a2 = y4 - y3
    b2 = x3 - x4
    c2 = a2 * x3 + b2 * y3

    # Determinant
    det = a1 * b2 - a2 * b1

    if det == 0:
        # Lines are parallel
        return None

    # Cramer's Rule
    x = (c1 * b2 - c2 * b1) / det
    y = (a1 * c2 - a2 * c1) / det

    return Point(x, y, 1)

"""
# TODO: Prueba en proyectiva

    # r1 y r2 son listas de dos puntos cada una, en coordenadas homogéneas
    l1 = np.cross([r1[0].x, r1[0].y], [r1[1].x, r1[1].y])
    l2 = np.cross([r2[0].x, r2[0].y], [r2[1].x, r2[1].y])
    inter = np.cross(l1, l2)
    # Normaliza si el punto no está en el infinito
    if inter[2] != 0:
        inter = inter / inter[2]
    return Point(inter[0],inter[1],inter[2])  # Devuelve [x, y, w]
"""