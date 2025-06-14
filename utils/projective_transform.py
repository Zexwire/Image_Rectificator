from PySide6.QtGui import (QImage, QPixmap)
from numpy import (array, zeros, uint8, frombuffer)
from numpy.linalg import (inv, solve)

from classes.points import (Coordinates)
from utils.infinity_line import calculate_vanish_points


def calculate_homography(sqr_points: Coordinates, output_sqr, aspect_ratio: float):
    """
    Calcula la homografía que rectifica la imagen usando los puntos de fuga
    :param sqr_points: 4 puntos del cuadrilátero original, de la forma [x : y : 1]
    :param aspect_ratio:
    :param output_sqr:
    :return: matriz de homografía
    """
    print(output_sqr)
    print("sqr_points given:")

    # Hallar los puntos de fuga
    vanishing_points = calculate_vanish_points(*sqr_points.get_points())

    print(vanishing_points[0].point)
    print(vanishing_points[1].point)
    print(sqr_points.points[0].point)
    print(sqr_points.points[3].point)
    # Buscamos una homografía tal que:
    # [v1] -> [1 : 0 : 0]
    # [v2] -> [0 : 1 : 0]
    # [sqr_points[0]] -> [1 : 1 : 1]
    # [sqr_points[3]] -> [output_sqr - 1 : output_sqr - 1 : 1]
    src_lin = array([
        array(vanishing_points[0].point),
        array(vanishing_points[1].point),
        array(sqr_points.points[0].point)
    ]).T
    src_final = array(sqr_points.points[3].point).reshape(3, 1)

    target_lin = array([
        [1, 0, 0],
        [0, 1, 0],
        [1, 1, 1]
    ]).T
    target_final = array([output_sqr - 1, output_sqr - 1, 1]).reshape(3, 1)

    modifiers_src = solve(src_lin, src_final)
    modifiers_target = solve(target_lin, target_final)

    print("Modifiers_src:")
    print(modifiers_src[0])
    print(modifiers_src[1])
    print(modifiers_src[2])
    print("Check if they get the final point:")
    print(modifiers_src[0] * array(vanishing_points[0].point) + modifiers_src[1] * array(vanishing_points[1].point) + modifiers_src[2] * array(sqr_points.points[0].point))
    print("Modifiers_target:")
    print(modifiers_target[0])
    print(modifiers_target[1])
    print(modifiers_target[2])
    print("Check if they get the final point:")
    print(modifiers_target[0] * [1, 0, 0] + modifiers_target[1] * [0, 1, 0] + modifiers_target[2] * [1, 1, 1])

    canonical_change = array([
        modifiers_src[0] * array(vanishing_points[0].point),
        modifiers_src[1] * array(vanishing_points[1].point),
        modifiers_src[2] * array(sqr_points.points[0].point)
    ]).T
    print("Canonical change:")
    print(canonical_change)

    lineal_application_matrix = array([
        modifiers_target[0] * [1, 0, 0],
        modifiers_target[1] * [0, 1, 0],
        modifiers_target[2] * [1, 1, 1]
    ]).T
    print("lineal application matrix:")
    print(lineal_application_matrix)

    print("inverse of canonical change:")
    print(inv(canonical_change))

    H = lineal_application_matrix @ inv(canonical_change)

    print("Homography matrix pre normalize: ")
    print(H)

    if H[2, 2] != 0:
        H /= H[2, 2]

    print("Homography matrix post normalize: ")
    print(H)

    b = 1 / aspect_ratio
    c = max(1, b)

    H = array([ [b, 0, 0],
                [0, c, 0],
                [0, 0, 1]]) @ H
    
    point_images0 = H @ array(sqr_points.points[0].point)
    point_images1 = H @ array(sqr_points.points[1].point)
    point_images2 = H @ array(sqr_points.points[2].point)
    point_images3 = H @ array(sqr_points.points[3].point)

    inf_image0 = H @ array(vanishing_points[0].point)
    inf_image1 = H @ array(vanishing_points[1].point)

    print("Images of the square: ")
    print(point_images0)
    print(point_images1)
    print(point_images2)
    print(point_images3)
    print("Images of infinite: ")
    print(inf_image0)
    print(inf_image1)

    return H

def numpy_to_qpixmap(arr):
    """Convertir de NumPy array (RGB) a QPixmap."""
    height, width, channels = arr.shape
    bytes_per_line = channels * width
    q_image = QImage(arr.data, width, height, bytes_per_line, QImage.Format_RGB888)
    return QPixmap.fromImage(q_image)

def warp_perspective_qpixmap(src_pixmap: QPixmap, H: array, output_size: tuple) -> QPixmap:
    """
    Warps a QPixmap using a homography matrix with the nearest neighbor interpolation.

    Parámetros:
        src_pixmap (QPixmap): Imagen original
        H (ndarray): Matriz de homografía
        output_size (tuple): (width, height) de la imagen deseada

    Retorna:
        QPixmap: Imagen distorsionada por la homografía en formato QPixmap
    """
    q_image = src_pixmap.toImage().convertToFormat(QImage.Format_RGB888)
    src_stride = q_image.bytesPerLine()
    src_width = q_image.width()
    src_height = q_image.height()
    src_ptr = q_image.bits()
    src_buffer = frombuffer(src_ptr, dtype=uint8).reshape(src_height, src_stride)[:, :src_width * 3]
    src_img = src_buffer.reshape((src_height, src_width, 3))
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