# Image-Rectification
This is a basic project using Affine and Projective Geometry. It rectifies images containing squares or rectangles.

----------------------
## Tareas:

### Fase 1: Solo cuadrados (5 de mayo)
Herramientas: OpenCV (procesamiento de imágenes) y NumPy (matrices). Tkinter y PySide6 (IU)

- (M - 23/04) Crear una ventana + Crear función que debe recibir como input 4 clicks del usuario en la ventana, y como output las coordenadas relativas de dichos clicks en la ventana. Lo ideal sería que el usuario haga 4 clicks y se active un botón tipo "Aceptar" para que el input se pase a la función.
- (C - 28/04) Función que dadas 4 coordenadas calcule las coordenadas de dos puntos de la recta del infinito
- (C - 28/04) Crear clase coordenada, que tenga como primer punto 0 o 1. 
- (J - 02/05) Función que dada una base y unos puntos transforme los puntos a referencia estándar
- (J - 02/05) Función que halle la referencia proyectiva y calcular la aplicación con la base asociada. Utilizar la función Raw Reduce para triangular. (Ajustar los números entre los puntos que se quieren transformar)
- (M - 05/05) Función que muestre el resultado final con la rectificación de la imagen dados los puntos iniciales y finales. Transformación dadas unas coordenadas iniciales y unas coordenadas finales.
- (05/05 a poder ser) Reunión con Jonatan (consultar si eliminar el fondo de la imagen o no)

### Fase 2: Ampliarlo a folios (razón sqrt(2)) (18 de mayo)
- Paso previo a usar la función cuadrado: hallar las esquinas del cuadrado dentro del rectángulo del folio usando la razón sqrt(2). Con esas nuevas coordenadas, pasárselas a la función cuadrado y el resto es todo igual (creo). --> HACER FUNCIÓN RAZÓN

### Fase 3: Documentación y elementos matemáticos
- Hablar de la preservación de la métrica
- Dar la justificación, con dibujos a ser posible
- Ejemplos de uso

### Fase 4: Mejoras (ideal hacerlo)
- Hacer una buena IU
- Usar IA para detectar las esquinas (algo similar a notebloc scanner, que seleccione las esquinas automáticamente y se puedan editar manualmente en caso de error).
- Mejorar el contraste: Podemos meterle filtros a la imagen resultante (pues tratándose de un folio es sencillo modificando la luz)
- Eliminar el fondo (según lo que opine Jonatan)

### Fase 5: Presentación
- Powerpoint mono que explique un poco por encima que es lo que hemos hecho
- Demo de uso (interesante que se pueda abrir rápido)