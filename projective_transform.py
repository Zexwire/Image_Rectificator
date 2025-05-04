import numpy as np
import cv2
from classes import Punto
from infinity_line import calculate_infinity_line

def order_points(pts):
    """Ordena 4 puntos en sentido horario (esquina superior-izquierda primero)"""
    pts = np.array(pts, dtype="float32")
    rect = np.zeros((4, 2), dtype="float32")
    
    s = pts.sum(axis=1)
    rect[0] = pts[np.argmin(s)]  # top-left
    rect[2] = pts[np.argmax(s)]  # bottom-right
    
    diff = np.diff(pts, axis=1)
    rect[1] = pts[np.argmin(diff)]  # top-right
    rect[3] = pts[np.argmax(diff)]  # bottom-left
    
    return rect

def calculate_homography_from_infinity(points, infinity_points):
    """
    Calcula la homografía que rectifica la imagen usando los puntos de fuga
    :param points: 4 puntos del cuadrilátero original
    :param infinity_points: 2 puntos que definen la línea del infinito
    :return: matriz de homografía
    """
    if None in infinity_points:
        raise ValueError("No se pudo calcular la línea del infinito (algunas líneas son paralelas)")
    
    # Convertir puntos a numpy array
    src_pts = np.array([p.to_tuple() for p in points], dtype="float32")
    
    # Calcular la línea del infinito (línea de horizonte)
    p_inf = infinity_points[0].to_tuple()
    q_inf = infinity_points[1].to_tuple()
    
    # Calcular la línea del infinito en coordenadas homogéneas
    line_inf = np.cross(
        [p_inf[0], p_inf[1], 1],
        [q_inf[0], q_inf[1], 1]
    )
    
    # Normalizar la línea del infinito
    line_inf = line_inf / line_inf[2]
    
    # Matriz de transformación para rectificar la línea del infinito
    H = np.eye(3)
    H[2] = line_inf
    
    # Aplicar transformación preliminar
    src_homogeneous = np.column_stack((src_pts, np.ones(4)))
    transformed = np.dot(H, src_homogeneous.T).T
    transformed = transformed[:, :2] / transformed[:, 2][:, np.newaxis]
    
    # Ahora calcular homografía para mapear a un cuadrado
    (tl, tr, br, bl) = order_points(transformed)
    
    # Tomar la máxima dimensión para que nada se corte
    width = max(np.linalg.norm(tr - tl), np.linalg.norm(br - bl))
    height = max(np.linalg.norm(tr - br), np.linalg.norm(tl - bl))
    square_size = int(max(width, height))
    
    dst_pts = np.array([
        [0, 0],
        [square_size - 1, 0],
        [square_size - 1, square_size - 1],
        [0, square_size - 1]
    ], dtype="float32")
    
    # Calcular homografía final
    M_affine = cv2.getPerspectiveTransform(transformed.astype(np.float32), dst_pts)
    
    # Combinar ambas transformaciones
    H_final = np.dot(M_affine, H)
    
    return H_final, square_size

def apply_projective_transform(image: np.ndarray, points: list) -> np.ndarray:
    """Transforma un cuadrilátero a un CUADRADO usando perspectiva"""
    try:
        # Calcular puntos de la línea del infinito
        infinity_points = calculate_infinity_line(*points)
        
        # 1. Calcular homografía usando la línea del infinito
        H, square_size = calculate_homography_from_infinity(points, infinity_points)
        
        # 2. Aplicar transformación
        warped = cv2.warpPerspective(
            image,
            H,
            (square_size, square_size),
            flags=cv2.INTER_LINEAR,
            borderMode=cv2.BORDER_CONSTANT,
            borderValue=(255, 255, 255)  # Fondo blanco
        )
        
        return warped
        
    except Exception as e:
        raise RuntimeError(f"Error transformando a cuadrado: {str(e)}")