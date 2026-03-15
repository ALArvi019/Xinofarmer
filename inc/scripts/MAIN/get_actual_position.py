
import cv2 as cv
from windowcapture import WindowCapture
from preprocess import PreProcessImage
from astar import MyAstar

images_path = r'path\to\immortal_xinofarmer\inc\img'
image_name = 'sea'
src_window = "LDPlayer"


wincap = WindowCapture(src_window)
preprocess = PreProcessImage()
astar = MyAstar()

tmp_actual_coords = (0, 0)

while True:
    mapa_completo = cv.imread(str(images_path + '/' + image_name + '.png'))
    mapa_completo = preprocess.pp_image(mapa_completo)
    gray_mapa_completo = cv.cvtColor(mapa_completo, cv.COLOR_BGR2GRAY)

    debug_actual_coords = astar.calculateActualCoords(
        gray_mapa_completo, wincap, preprocess)
    
    if debug_actual_coords != tmp_actual_coords:
        tmp_actual_coords = debug_actual_coords
        print("actual_coords: " + str(debug_actual_coords))

    tmp_mapa_completo = mapa_completo.copy()
    # print current position
    cv.circle(tmp_mapa_completo, debug_actual_coords, 5, (0, 0, 255), -1)
    cv.imshow('Mapa completo', tmp_mapa_completo)
    cv.waitKey(1)