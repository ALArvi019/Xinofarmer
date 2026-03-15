import pyastar2d
import numpy as np
import cv2 as cv
from preprocess import PreProcessImage
preprocess = PreProcessImage()

class MyAstar:
    def __init__(self):
        pass

    def get_path(self, gray_mapa_completo, path_start, path_end, treshval, treshmaxval):
        ret, thresh = cv.threshold(
            gray_mapa_completo, treshval, treshmaxval, cv.THRESH_BINARY)
        thresh1 = cv.dilate(thresh, np.ones((3,3), np.uint8), iterations=1)
        weights = np.array(thresh1, dtype=np.float32) + 1

        path = pyastar2d.astar_path(weights, path_start[::-1], path_end[::-1], allow_diagonal=True)  # Reverse (i, j) coordinates

        # check is None
        if path is None:
            return None

        # Convert matrix coordinates (i, j) to (x, y) coordinates
        cell_size = 1  # Change this to the size of each cell in pixels
        path = [(int(cell_size * j), int(cell_size * i)) for (i, j) in path]

        # foreach all points in path and move 3px if near a wall
        for i in range(len(path)):
            if thresh1[path[i][1]][path[i][0]] == 0:
                path[i] = (path[i][0] + 3, path[i][1] + 3)

        return path
    
    def calculateActualCoords(self, gray_mapa_completo, wincap, preprocess, relative_coords = None):
        try:
            screenshot = wincap.get_screenshot()
            minimapa_actual = preprocess.crop(screenshot, 740, 40, 173, 83)
            gray_minimapa_actual = cv.cvtColor(minimapa_actual, cv.COLOR_BGR2GRAY)
            result = cv.matchTemplate(gray_mapa_completo, gray_minimapa_actual, cv.TM_CCOEFF_NORMED)
            min_val, max_val, min_loc, max_loc = cv.minMaxLoc(result)
            top_left = max_loc
            if max_val > 0.35:
                if relative_coords is not None:
                    return (top_left[0] + 87 + relative_coords[0], top_left[1] + 57 + relative_coords[1])
                else:
                    return (top_left[0] + 87, top_left[1] + 57)
            else:
                return None
        except:
            return None
    
    def calculateActualCoordsCanny(self, gray_mapa_completo, wincap, preprocess, relative_coords = None):
        try:
            screenshot = wincap.get_screenshot()
            minimapa_actual = preprocess.crop(screenshot, 720, 40, 173, 120)
            gray_minimapa_actual = cv.cvtColor(minimapa_actual, cv.COLOR_BGR2GRAY)
            canny_image = preprocess.to_canny(gray_minimapa_actual, 50, 150, 3)

            cv.imshow('canny_image', canny_image)
            cv.waitKey(1)
            result = cv.matchTemplate(gray_mapa_completo, canny_image, cv.TM_CCOEFF_NORMED)
            min_val, max_val, min_loc, max_loc = cv.minMaxLoc(result)
            top_left = max_loc
            print(max_val)
            if max_val > 0.06:
                if relative_coords is not None:
                    return (top_left[0] + 46 + relative_coords[0], top_left[1] + 79 + relative_coords[1])
                else:
                    return (top_left[0] + 46, top_left[1] + 79)
            else:
                return None
        except Exception as e:
            print(e)
            return None
        
    def isNear(self, path_start, path_end):
        if abs(path_start[0] - path_end[0]) < 20 and abs(path_start[1] - path_end[1]) < 20:
            return True
        else:
            return False
        
    # def checkIfCoordsIsOutsideWalls(self, gray_mapa_completo, path_end):
    #     if gray_mapa_completo[path_end[1]][path_end[0]] == 0:
    #         return True
    #     else:
    #         return False