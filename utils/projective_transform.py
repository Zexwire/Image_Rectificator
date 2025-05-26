from numpy import (array, zeros, uint8)
from numpy.linalg import (inv, solve)

from PySide6.QtGui import (QImage, QPixmap)

from classes.points import (Coordinates, Point)
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

    # Hallemos R' y S'
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


def calculate_homography(sqr_points: Coordinates, output_sqr):
    """
    Calcula la homografía que rectifica la imagen usando los puntos de fuga
    :param sqr_points: 4 puntos del cuadrilátero original, de la forma [x : y : 1]
    :return: matriz de homografía
    """

    # Hallar los puntos de fuga
    vanishing_points = calculate_vanish_points(*sqr_points.get_points())

    # Buscamos una homografía tal que:
    # [v1] -> [1 : 0 : 0]
    # [v2] -> [0 : 1 : 0]
    # [sqr_points[0]] -> [1 : 1 : 1]
    # [sqr_points[3]] -> [output_sqr - 1 : output_sqr - 1 : 1]
    src_lin = array([
        array(vanishing_points[0].point),
        array(vanishing_points[1].point),
        array(sqr_points.points[0].point)
    ])
    src_final = array(sqr_points.points[3].point).reshape(3, 1)

    target_lin = array([
        [1, 0, 0],
        [0, 1, 0],
        [1, 1, 1]
    ])
    target_final = array([output_sqr - 1, output_sqr - 1, 1]).reshape(3, 1)

    modifiers_src = solve(src_lin, src_final)
    modifiers_target = solve(target_lin, target_final)

    canonical_change = array([
        [modifiers_src[0] * array(vanishing_points[0].point)],
        [modifiers_src[1] * array(vanishing_points[1].point)],
        [modifiers_src[2] * array(sqr_points.points[0].point)]
    ]).T

    lineal_application_matrix = array([
        [modifiers_target[0] * [1, 0, 0]],
        [modifiers_target[1] * [0, 1, 0]],
        [modifiers_target[2] * [1, 1, 1]]
    ]).T

    return lineal_application_matrix @ inv(canonical_change)

def qpixmap_to_numpy(pixmap):
    """Convertir de QPixmap a NumPy array (RGB)."""
    q_image = pixmap.toImage().convertToFormat(QImage.Format_RGB888)
    width = q_image.width()
    height = q_image.height()
    ptr = q_image.bits()
    arr = array(ptr, dtype=uint8).reshape((height, width, 3))
    return arr

def numpy_to_qpixmap(arr):
    """Convertir de NumPy array (RGB) a QPixmap."""
    height, width, channels = arr.shape
    bytes_per_line = channels * width
    q_image = QImage(arr.data, width, height, bytes_per_line, QImage.Format_RGB888)
    return QPixmap.fromImage(q_image)

def warp_perspective_qpixmap(src_pixmap: QPixmap, H: array, output_size: tuple) -> QPixmap:
    """
    Warps a QPixmap using a homography matrix with nearest neighbor interpolation.

    Parámetros:
        src_pixmap (QPixmap): Imagen original
        H (ndarray): Matriz de homografía
        output_size (tuple): (width, height) de la imagen deseada

    Retorna:
        QPixmap: Imagen distorsionada por la homografía en formato QPixmap
    """
    src_img = qpixmap_to_numpy(src_pixmap)
    width, height = output_size
    dst_img = zeros((height, width, src_img.shape[2]), dtype=src_img.dtype)
    H_inv = inv(H)

    for y_dst in range(height):
        for x_dst in range(width):
            dst_pt = array([x_dst, y_dst, 1])
            src_pt = H_inv @ dst_pt
            src_x = float(src_pt[0] / src_pt[2])
            src_y = float(src_pt[1] / src_pt[2])

            src_x_int = int(round(src_x))
            src_y_int = int(round(src_y))
            if (0 <= src_x_int < src_img.shape[1]) and (0 <= src_y_int < src_img.shape[0]):
                dst_img[y_dst, x_dst] = src_img[src_y_int, src_x_int]

    return numpy_to_qpixmap(dst_img)