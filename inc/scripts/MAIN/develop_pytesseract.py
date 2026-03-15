import cv2 as cv
import numpy as np
import pytesseract


# path\to\immortal_xinofarmer\inc\tesseract\tesseract.exe
pytesseract.pytesseract.tesseract_cmd = r'path\to\immortal_xinofarmer\inc\tesseract\tesseract.exe'

# load image yellow_dust.png
# image = cv.imread('scrap.png')
image = cv.imread('scrapt.png')

resized = cv.resize(image, (0,0), fx=2, fy=2)

hsv_image = cv.cvtColor(resized, cv.COLOR_BGR2HSV)

# Define los valores mínimos y máximos de color en formato HSV
# yellow OK
# lower_color = np.array([25, 189, 82], dtype=np.uint8)
# upper_color = np.array([27, 205, 139], dtype=np.uint8)

# (hMin = 15 , sMin = 151, vMin = 78), (hMax = 27 , sMax = 207, vMax = 165)
# scrapt OK
lower_color = np.array([15, 151, 78], dtype=np.uint8)
upper_color = np.array([27, 207, 165], dtype=np.uint8)

# Filtra los píxeles en el rango de colores
mask = cv.inRange(hsv_image, lower_color, upper_color)

# Aplica la máscara a la imagen original
filtered_image = cv.bitwise_and(resized, resized, mask=mask)

 # Convierte la imagen filtrada a escala de grises
gray_image = cv.cvtColor(filtered_image, cv.COLOR_BGR2GRAY)

# Mejora el contraste y aplica umbralización
_, thresholded_image = cv.threshold(gray_image, 0, 255, cv.THRESH_BINARY + cv.THRESH_OTSU)

inverted_image = cv.bitwise_not(thresholded_image)

# Redimensiona la imagen nuevamente si es necesario
scaled_image = cv.resize(inverted_image, (0, 0), fx=2, fy=2)

custom_config = r'--oem 3 --psm 6 outputbase digits'
text = pytesseract.image_to_string(scaled_image, config=custom_config)



# Imprime el texto en negro

print("\033[30m" + "------------> " + text + "\033[0m")

cv.imshow('crop', image)
cv.imshow('scaled_image', scaled_image)
cv.waitKey(0)