import cv2 as cv
from windowcapture import WindowCapture
from preprocess import PreProcessImage
from getkeys import key_check
import numpy as np

# Inicialización de las clases necesarias
wincap = WindowCapture('LDPlayer')
preprocess = PreProcessImage()



# Carga de las imágenes de referencia
mapa_completo = cv.imread('./namari.png')
mapa_completo_gray = cv.cvtColor(mapa_completo, cv.COLOR_BGR2GRAY)

orb = cv.ORB_create(nfeatures=200)

BF = cv.BFMatcher(cv.NORM_HAMMING, crossCheck=True)

distance = 50.0





while True:

    # Capturamos una imagen del minimapa actual y obtenemos sus descriptores
    screenshot = wincap.get_screenshot()
    minimapa_actual = preprocess.crop(screenshot, 740, 40, 173, 83)
    gray_minimapa_actual = cv.cvtColor(minimapa_actual, cv.COLOR_BGR2GRAY)

    # Find the key points and descriptors with SIFT
    keypoints1, descriptors1 = orb.detectAndCompute(mapa_completo_gray, None)
    keypoints2, descriptors2 = orb.detectAndCompute(gray_minimapa_actual, None)

    matches = BF.match(descriptors1, descriptors2)
    matches = sorted(matches, key=lambda x: x.distance)

    # get only the good matches, with distance < 50

    good = []
    for m in matches:
        print(f'{int(m.distance)} < {int(distance)}')
        if int(m.distance) < int(distance):
            good.append(m)


    draw_params = dict(matchColor=(0, 255, 0),
                       singlePointColor=(255, 0, 0),
                          flags=0)

    img3 = cv.drawMatches(mapa_completo, keypoints1, minimapa_actual, keypoints2, matches[:5], None, **draw_params)



    cv.rectangle(img3, (45, 343), (93, 374), (0, 0, 255), 2)
    cv.imshow('Matches', img3)
    cv.imshow('mapa_completo', mapa_completo)



    # Mostramos la imagen del minimapa actual
    # cv.imshow('Minimapa', gray_minimapa_ssssssssssssssssssssssssactual)


    if cv.waitKey(1) == ord('q'):
        cv.destroyAllWindows()
        break

    keys = key_check()
    if 1 == 1:
        if 'A' in keys:
            distance += 0.5
            print(distance)
        if 'S' in keys:
            distance -= 0.5
            print(distance)

