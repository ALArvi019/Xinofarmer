from windowcapture import WindowCapture
from preprocess import PreProcessImage
import cv2 as cv
from getkeys import key_check
import sys
import numpy as np
import time
import pathlib as pl
import pyautogui

wincap = WindowCapture('LDPlayer')
preprocess = PreProcessImage()

cannyminThreshold = 38
cannyMaxThreshold = 21

hough_thtreshold = 0
hough_minLineLength = 0
hough_maxLineGap = 0

while True:

    screen = wincap.get_screenshot()
    minimap1 = preprocess.crop(screen, 740, 40, 173, 110)
    minimap2 = minimap1
    gris = preprocess.to_grayscale(minimap1)
    suave = cv.GaussianBlur(gris, (5, 5), 0)
    bordes = cv.Canny(suave, cannyminThreshold, cannyMaxThreshold)

    binario = cv.threshold(bordes, 0, 255, cv.THRESH_BINARY_INV)[1]

    contornos, _ = cv.findContours(binario, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)

    for contorno in contornos:
        area = cv.contourArea(contorno)
        if area > 100:
            cv.drawContours(minimap2, [contorno], 0, (0, 255, 0), 2)


    # Transformada de Hough probabilística para detectar trazos
    # lineas = preprocess.get_lines(
    #     bordes, hough_thtreshold, hough_minLineLength, hough_maxLineGap)

    # # Dibujar las líneas en la imagen
    # if lineas is not None:
    #     for linea in lineas:
    #         x1, y1, x2, y2 = linea[0]
    #         cv.line(minimap1, (x1, y1), (x2, y2), (0, 255, 0), 2)

    # preprocess.image_show('minimap', minimap1)

    # # Filtrar las líneas que representan paredes
    # paredes = []
    # for i in range(len(lineas)):
    #     for j in range(i+1, len(lineas)):
    #         # Calcular la distancia y el ángulo entre los trazos
    #         dx = lineas[i][0][0] - lineas[j][0][0]
    #         dy = lineas[i][0][1] - lineas[j][0][1]
    #         dist = np.sqrt(dx*dx + dy*dy)
    #         angulo = np.arctan2(dy, dx) * 180 / np.pi
            
    #         # Descartar trazos que no sean paralelos o que estén demasiado separados
    #         if abs(angulo) < 10 or abs(angulo-180) < 10:
    #             if dist < 20:
    #                 # Agregar los trazos a la lista de paredes
    #                 paredes.append((lineas[i][0], lineas[j][0]))

    # # Dibujar las paredes en la imagen original
    # for linea1, linea2 in paredes:
    #     cv.line(minimap2, (linea1[0], linea1[1]), (linea2[0], linea2[1]), (0, 0, 255), 2)

    
    preprocess.image_show('minimap1', minimap1)
    preprocess.image_show('bordes', bordes)
    preprocess.image_show('binario', binario)
    preprocess.image_show('contornos', minimap2)


    if cv.waitKey(1) == ord('q'):
        cv.destroyAllWindows()
        break

    # keys = key_check()
    # if 'A' in keys:
    #     hough_thtreshold += 1
    #     print('hough_thtreshold: ', hough_thtreshold)
    #     print('hough_minLineLength: ', hough_minLineLength)
    #     print('hough_maxLineGap: ', hough_maxLineGap)
    # if 'Z' in keys:
    #     hough_thtreshold -= 1
    #     print('hough_thtreshold: ', hough_thtreshold)
    #     print('hough_minLineLength: ', hough_minLineLength)
    #     print('hough_maxLineGap: ', hough_maxLineGap)
    # if 'S' in keys:
    #     hough_minLineLength += 1
    #     print('hough_thtreshold: ', hough_thtreshold)
    #     print('hough_minLineLength: ', hough_minLineLength)
    #     print('hough_maxLineGap: ', hough_maxLineGap)
    # if 'X' in keys:
    #     hough_minLineLength -= 1
    #     print('hough_thtreshold: ', hough_thtreshold)
    #     print('hough_minLineLength: ', hough_minLineLength)
    #     print('hough_maxLineGap: ', hough_maxLineGap)
    # if 'D' in keys:
    #     hough_maxLineGap += 1
    #     print('hough_thtreshold: ', hough_thtreshold)
    #     print('hough_minLineLength: ', hough_minLineLength)
    #     print('hough_maxLineGap: ', hough_maxLineGap)
    # if 'C' in keys:
    #     hough_maxLineGap -= 1
    #     print('hough_thtreshold: ', hough_thtreshold)
    #     print('hough_minLineLength: ', hough_minLineLength)
    #     print('hough_maxLineGap: ', hough_maxLineGap)
