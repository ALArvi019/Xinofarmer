import cv2 as cv
from windowcapture import WindowCapture
from preprocess import PreProcessImage

# Inicialización de las clases necesarias
wincap = WindowCapture('LDPlayer')
preprocess = PreProcessImage()

# Carga de las imágenes de referencia
mapa_completo = cv.imread('./namari.png')
# Obtenemos las dimensiones de la imagen original
height, width = mapa_completo.shape[:2]
# # Definimos el tamaño del marco negro
border_size = 60
# # Creamos una imagen de tamaño mayor que la original con bordes negros
new_height = height + border_size * 2
new_width = width + border_size * 2
mapa_completo = cv.copyMakeBorder(mapa_completo, border_size, border_size, border_size, border_size, cv.BORDER_CONSTANT, None, value=[0, 0, 0])

gray_mapa_completo = cv.cvtColor(mapa_completo, cv.COLOR_BGR2GRAY)

# Binarizar la imagen usando un umbral de 255
_, binary_image = cv.threshold(gray_mapa_completo, 254, 255, cv.THRESH_BINARY)

# Invertir los colores de la imagen binaria
inverted_image = cv.bitwise_not(binary_image)

# Crear una máscara con los píxeles negros
mask = cv.cvtColor(inverted_image, cv.COLOR_GRAY2BGR)

# Reemplazar los píxeles blancos con negros en la imagen original
mapa_completo = cv.bitwise_and(mapa_completo, mask)

gray_mapa_completo = cv.cvtColor(mapa_completo, cv.COLOR_BGR2GRAY)


while True:

    # Capturamos una imagen del minimapa actual y obtenemos sus descriptores
    screenshot = wincap.get_screenshot()
    minimapa_actual = preprocess.crop(screenshot, 740, 40, 173, 83)
    gray_minimapa_actual = cv.cvtColor(minimapa_actual, cv.COLOR_BGR2GRAY)

    # Buscamos la plantilla en el mapa completo
    result = cv.matchTemplate(gray_mapa_completo, gray_minimapa_actual, cv.TM_CCOEFF_NORMED)

    # Obtenemos la posición de la coincidencia máxima
    min_val, max_val, min_loc, max_loc = cv.minMaxLoc(result)
    top_left = max_loc

    # Mostramos la posición en el mapa completo
    tmp_mapa_completo = mapa_completo.copy()
    # print(max_val)
    if max_val > 0.2:
        # Definimos las dimensiones de la imagen del minimapa actual
        h, w = minimapa_actual.shape[:2]

        # Definimos la posición de la imagen del minimapa actual encima de tmp_mapa_completo
        bottom_right = (top_left[0] + w, top_left[1] + h)

        # Añadimos la imagen del minimapa actual encima de tmp_mapa_completo
        cv.addWeighted(minimapa_actual, 0.5, tmp_mapa_completo[top_left[1]:bottom_right[1], top_left[0]:bottom_right[0]], 0.5, 0, tmp_mapa_completo[top_left[1]:bottom_right[1], top_left[0]:bottom_right[0]])

        # Mostramos el mapa completo
        cv.imshow('Mapa completo', tmp_mapa_completo)

    if cv.waitKey(1) == ord('q'):
        cv.destroyAllWindows()
        break
