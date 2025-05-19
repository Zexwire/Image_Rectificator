from numpy import (array, zeros, uint8)
from numpy.linalg import (lstsq, inv)

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
    # [v1] -> [0 : 1 : 0]
    # [v2] -> [1 : 0 : 0]
    # [sqr_points[0]] -> [-1 : 1 : 1]
    # [sqr_points[1]] -> [1 : 1 : 1]
    # [sqr_points[2]] -> [-1 : -1 : 1]
    # [sqr_points[3]] -> [1 : -1 : 1]
    target_vanishing = [array([0, 1, 0]), array([1, 0, 0])]
    target_sqr = [
        array([1, 1, 1]),
        array([output_sqr - 1, 1, 1]),
        array([1, output_sqr - 1, 1]),
        array([output_sqr - 1, output_sqr - 1, 1])
    ]

    A = []
    b = []

    # Añadimos las restricciones de los puntos del infinito
    for vp_src, vp_dst in zip(vanishing_points, target_vanishing):
        x, y, z = vp_src.point
        X, Y, Z = vp_dst

        # Para [1,0,0]: h11*x + h12*y + z*h13 = lambda, h21*x + h22*y + z*h23 = 0
        if X == 1 and Y == 0:
            # componente X = lambda, componente Y = 0
            A.append([x, y , z, 0, 0, 0, 0, 0, 0])
            b.append(1)
            A.append([0, 0, 0, x, y , z, 0, 0, 0])
            b.append(0)
        # Para [0,1,0]: h11*x + h12*y + z*h13 = 0, h21*x + h22*y + z*h23 = lambda
        elif X == 0 and Y == 1:
            # componente X = 0, componente Y = lambda
            A.append([x, y , z, 0, 0, 0, 0, 0, 0])
            b.append(0)
            A.append([0, 0, 0, x, y , z, 0, 0, 0])
            b.append(1)
        else:
            raise ValueError("Vanishing point must be at infinity with either x or y component 1.")

        # Al ser de la recta del infinito la última componente es cero para ambas
        # h31*x + h32*y + z*h33 = 0
        A.append([0, 0, 0, 0, 0, 0, x, y, z])
        b.append(0)

    for sqrp_src, sqrp_dst in zip(sqr_points, target_sqr):
        x, y, z = sqrp_src.point
        X, Y, Z = sqrp_dst

        # Dos ecuaciones por punto del cuadrado
        # h11*x + h12*y + h13 - X*(h31*x + h32*y + h33) = 0
        A.append([x, y, 1, 0, 0, 0, -X * x, -X * y, -X * z])
        b.append(0)
        # h21*x + h22*y + h23 - Y*(h31*x + h32*y + h33) = 0
        A.append([0, 0, 0, x, y, 1, -Y * x, -Y * y, -Y * z])
        b.append(0)

    A = array(A)
    b = array(b)

    # Resolvemos el sistema de ecuaciones con el método de mínimos cuadrados
    H_flat, residuals, rank, s = lstsq(A, b, rcond=None)

    H = H_flat.reshape(3, 3)

    # Normalizar como hace OpenCV en última componente a 1(no estoy seguro de esto)
    if H[2, 2] != 0:
        H /= H[2, 2]

    return H

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