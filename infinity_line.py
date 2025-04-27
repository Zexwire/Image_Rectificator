from main import Punto

# TODO: Renombrar este archivo si lo veis necesario (no estaba segura de como llamarlo)
def calculate_infinity_line(p1: Punto, p2: Punto, p3: Punto, p4: Punto):

    p = intersection([p1, p2], [p3, p4])
    q = intersection([p1, p3], [p2, p4])

    return [p, q] # TODO: @Jacob, si necesitas modificar lo que devuelve esta función 0 problema, de momento lo dejo como los 2 puntos de la recta del infinito

def intersection(r1, r2):
    x1, y1 = r1[0]
    x2, y2 = r1[1]
    x3, y3 = r2[0]
    x4, y4 = r2[1]

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

    return Punto(x, y)