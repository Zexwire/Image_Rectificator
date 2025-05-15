from classes.points import Coordinates, Point
from utils.infinity_line import calculate_vanish_points

def find_sqr_points(corners: Coordinates, aspect_ratio: float) -> Coordinates:
    if aspect_ratio == 1:
        return corners
    # Usando la razón, siendo P = corners[0], Q = corners[1], R = corners[2] y S = corners[3]
    # Podemos hallar R' y S' de la forma:
    # [P, R, R'] = aspect_ratio -> PR = aspect_ratio PR' -> rx-px/a +px= r'x
    # Y análogo para S'
    pts = corners.get_points()
    P = pts[0]
    Q = pts[1]
    R = pts[2]
    S = pts[3]

    # Hallemos Q' y S'
    Rx = P.x + (R.x - P.x) / aspect_ratio
    Ry = P.y + (R.y - P.y) / aspect_ratio
    Sx = Q.x + (S.x - Q.x) / aspect_ratio
    Sy = Q.y + (S.y - Q.y) / aspect_ratio

    # De esta forma:
    # P --- Q
    # |     |
    # R'--- S'
    # |     |
    # R --- S
    coordinates = Coordinates()
    coordinates.set_points([P, Q, Point(Rx, Ry, 1), Point(Sx, Sy, 1)])
    return coordinates


def calculate_homography(sqr_points: Coordinates):
    """
    Calcula la homografía que rectifica la imagen usando los puntos de fuga
    :param sqr_points: 4 puntos del cuadrilátero original, de la forma [x : y : 1]
    :return: matriz de homografía
    """

    # Hallar los puntos de fuga
    v1, v2 = calculate_vanish_points(*sqr_points.get_points())

    # Buscamos una homografía tal que:
    # [v1] -> [1 : 0 : 0]
    # [v2] -> [0 : 1 : 0]
    # [sqr_points[0]] -> [-1 : 1 : 1]
    # [sqr_points[1]] -> [1 : 1 : 1]
    # [sqr_points[2]] -> [-1 : -1 : 1]
    # [sqr_points[3]] -> [1 : -1 : 1]
    # TODO: completar esta funcion