import cv2
from windowcapture import WindowCapture
from preprocess import PreProcessImage
import numpy as np
import os

# Creamos la ventana de captura
wincap = WindowCapture('LDPlayer')
preprocess = PreProcessImage()

# check if directory ./data exists
if not os.path.exists('./data'):
    os.makedirs('./data')

last_image = None
final_image = None

# Capturar la primera imagen del juego
screen = wincap.get_screenshot()

# Recortar la imagen para obtener la sección del mapa que nos interesa
minimap = preprocess.crop(screen, 740, 40, 173, 83)

# Inicializar la imagen base con el primer recorte de la pantalla
base_image = minimap.copy()

final_image = np.zeros((83, 173, 3), dtype=np.uint8)

# Ciclo principal de captura y procesamiento de imagen
while True:
    # Capturamos la imagen del juego
    screen = wincap.get_screenshot()

    # Recortamos la imagen para obtener la sección del mapa que nos interesa
    minimap = preprocess.crop(screen, 740, 40, 173, 83)

    # Capturar la imagen actual del juego
    screen = wincap.get_screenshot()

    # Recortar la imagen para obtener la sección del mapa que nos interesa
    minimap = preprocess.crop(screen, 740, 40, 173, 83)

    # Calcular la similitud entre la imagen actual y la imagen base
    result = cv2.matchTemplate(base_image, minimap, cv2.TM_CCOEFF_NORMED)
    _, similarity, _, location = cv2.minMaxLoc(result)

    threshold = 0.6

    # Si la similitud es mayor al umbral, superponer la imagen actual en la imagen base
    if similarity >= threshold:
        left = location[0]
        top = location[1]
        right = location[0] + minimap.shape[1]
        bottom = location[1] + minimap.shape[0]
        base_image[top:bottom, left:right] = minimap

        # Crea una nueva imagen con las dimensiones adecuadas
        new_image = np.zeros(
            (max(bottom, 83), max(right, 173), 3), dtype=np.uint8)
        new_image.fill(255)

        # Crea una máscara para el área que se superpone con la imagen anterior
        mask1 = np.zeros((83, 173), dtype=np.uint8)
        mask1[0:bottom-top, 0:right-left] = 255

        # Crea una máscara para el área que no se superpone con la imagen anterior
        mask2 = np.zeros_like(mask1)
        mask2[top:bottom, left:right] = 255

        # Pega la imagen base en la posición correcta usando la máscara
        final_image = cv2.bitwise_and(final_image, final_image, mask=mask2)
        final_image[0:bottom-top, 0:right -
                    left] += cv2.bitwise_and(minimap, minimap, mask=mask1)

    # Muestra la imagen resultante
    cv2.imshow('Mapa completo', final_image)

    # Esperamos un segundo antes de la siguiente captura
    if cv2.waitKey(1) == ord('q'):
        break
