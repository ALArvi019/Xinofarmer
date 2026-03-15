import cv2
import numpy as np

# Función para resaltar las partes no semitransparentes de una imagen
def highlight_opaque(img):
    # Convertir la imagen a escala de grises
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    
    # Binarizar la imagen
    _, thresh = cv2.threshold(gray, 50, 255, cv2.THRESH_BINARY)
    
    cv2.imshow('thresh', thresh)

    # Encontrar los contornos de las regiones blancas en la imagen binarizada
    contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    
    # Dibujar un contorno verde alrededor de las partes no semitransparentes de la imagen
    img_highlight = img.copy()
    for contour in contours:
        cv2.drawContours(img_highlight, [contour], 0, (0, 255, 0), 2)
    
    return img_highlight

img1 = cv2.imread('./data/0.png')
img2 = cv2.imread('./data/400.png')

# Resaltar las partes no semitransparentes de las imágenes
img1_highlight = highlight_opaque(img1)
img2_highlight = highlight_opaque(img2)

# Mostrar las imágenes resaltadas
cv2.imshow('Image 1', img1_highlight)
cv2.imshow('Image 2', img2_highlight)
cv2.waitKey(0)
cv2.destroyAllWindows()

# obtener los descriptores de características y los puntos clave
sift = cv2.SIFT_create()
kp1, des1 = sift.detectAndCompute(img1_highlight, None)
kp2, des2 = sift.detectAndCompute(img2_highlight, None)

# Hacer la coincidencia de características usando BFMatcher
bf = cv2.BFMatcher()
matches = bf.knnMatch(des1, des2, k=2)

# Calcular la media de las distancias entre coincidencias
distances = []
for m,n in matches:
    distances.append(m.distance)
mean_distance = np.mean(distances)

# Aplicar el filtro de distancia para seleccionar las mejores coincidencias
good_matches = []
for m,n in matches:
    if m.distance > 0.10*mean_distance and m.distance < 0.55*mean_distance:
        good_matches.append(m)

# Filtrar más las coincidencias
MIN_MATCH_COUNT = 1
if len(good_matches) > MIN_MATCH_COUNT:
    # extraer los puntos correspondientes en las dos imágenes
    src_pts = np.float32([kp1[m.queryIdx].pt for m in good_matches]).reshape(-1,1,2)
    dst_pts = np.float32([kp2[m.trainIdx].pt for m in good_matches]).reshape(-1,1,2)

    # calcular la distancia entre las dos imágenes usando los puntos correspondientes
    distances = []
    for i in range(len(good_matches)):
        x1, y1 = src_pts[i][0]
        x2, y2 = dst_pts[i][0]
        dist = np.sqrt((x2-x1)**2 + (y2-y1)**2)
        distances.append(dist)
    dist = np.mean(distances)

    # superponer las imágenes usando la distancia calculada
    offset_x = int(dist)
    offset_y = int(dist)
    result_dimensions = (img1.shape[1] + img2.shape[1] + offset_x, img1.shape[0] + img2.shape[0] + offset_y)
    result_image = np.zeros(result_dimensions, dtype=np.uint8)
    result_image[offset_y:img1.shape[0]+offset_y, offset_x:img1.shape[1]+offset_x] = img1
    result_image[:img2.shape[0], :img2.shape[1]] = img2

    # dibujar las coincidencias
    result_image = cv2.drawMatches(img1, kp1, img2, kp2, good_matches, result_image, flags=2)

    # mostrar la imagen resultante
    cv2.imshow('Result', result_image)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

else:
    print("No se encontraron suficientes coincidencias - %d/%d" % (len(good_matches), MIN_MATCH_COUNT))

    