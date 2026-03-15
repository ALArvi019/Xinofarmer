import numpy as np
import cv2 as cv
import pyautogui
import time
from findImage import RunFindImage

def RunFishV2(captureworker, images_path, fish_type, src_window):

    # Pon la primera letra en mayúscula
    fish_type = fish_type[0].upper() + fish_type[1:]

    if fish_type == 'Legendary' or fish_type == 'Epic':
        fish_type = 'Gold'

    LeftColumnTemplate = cv.imread(str(images_path + '/LeftColumn' + fish_type + '.png'))
    RightColumnTemplate = cv.imread(str(images_path + '/RightColumn' + fish_type + '.png'))
    MiddleArrowTemplate = cv.imread(str(images_path + '/Arrow' + fish_type + '.png'))

    
    left_middle_offset = 20
    if fish_type == 'White':
        middle_precision = 0.90
        left_precision = 0.89
        right_precision = 0.66
        fixed_distance_between_left_right = 114  # Distancia entre LeftColumn y RightColumn
        middle_offset = int(fixed_distance_between_left_right / 2)
    elif fish_type == 'Blue':
        middle_precision = 0.90
        left_precision = 0.89
        right_precision = 0.70
        fixed_distance_between_left_right = 99  # Distancia entre LeftColumn y RightColumn
        middle_offset = int(fixed_distance_between_left_right / 2)
    elif fish_type == 'Gold':
        middle_precision = 0.8
        left_precision = 0.81
        right_precision = 0.79
        fixed_distance_between_left_right = 82  # Distancia entre LeftColumn y RightColumn
        fixed_distance_between_left_right = 67  # Distancia entre LeftColumn y RightColumn
        fixed_distance_between_left_right = 55  # Distancia entre LeftColumn y RightColumn
        middle_offset = int(fixed_distance_between_left_right / 2)

    while True:
        screenshot = captureworker.screenshot
        screenshot = screenshot[85:125, 275:687]
        # save secrrenshot
        # cv.imwrite('screenshot.png', screenshot)

        LeftRes = cv.matchTemplate(
            screenshot, LeftColumnTemplate, cv.TM_CCOEFF_NORMED)
        _, max_val_left, _, max_loc_left = cv.minMaxLoc(LeftRes)

        RightRes = cv.matchTemplate(
            screenshot, RightColumnTemplate, cv.TM_CCOEFF_NORMED)
        _, max_val_right, _, max_loc_right = cv.minMaxLoc(RightRes)

        MiddleRes = cv.matchTemplate(
            screenshot, MiddleArrowTemplate, cv.TM_CCOEFF_NORMED)
        _, max_val_middle, _, max_loc_middle = cv.minMaxLoc(MiddleRes)

        # # Dibuja los rectángulos en la captura de pantalla
        # screenshot2 = screenshot.copy()
        # cv.rectangle(screenshot2, max_loc_left, (max_loc_left[0] + LeftColumnTemplate.shape[1], max_loc_left[1] + LeftColumnTemplate.shape[0]), (0, 0, 255), 2)
        # cv.rectangle(screenshot2, max_loc_right, (max_loc_right[0] + RightColumnTemplate.shape[1], max_loc_right[1] + RightColumnTemplate.shape[0]), (0, 0, 255), 2)
        # cv.rectangle(screenshot2, max_loc_middle, (max_loc_middle[0] + MiddleArrowTemplate.shape[1], max_loc_middle[1] + MiddleArrowTemplate.shape[0]), (0, 255, 255), 2)

        # print distance betweeen left and right
        distance_left_right = max_loc_right[0] - (max_loc_left[0] + LeftColumnTemplate.shape[1])
        # print('distance_left_right->', distance_left_right, ' max_val_middle->', max_val_middle, ' max_val_left->', max_val_left, ' max_val_right->', max_val_right)

        # calcular si la distancia actual está entre un rango de +-5 de la distancia fija entre left y right
        if abs(distance_left_right - fixed_distance_between_left_right) <= 5:
            # si la distancia está en el rango, entonces se puede pescar
            right_column_position = max_loc_left[0] + LeftColumnTemplate.shape[1] + fixed_distance_between_left_right
            left_column_position = max_loc_left[0]
        else:
            # obtener la columna con mayor coincidencia
            if max_val_left > max_val_right:
                # calcular la posición de la columna derecha
                right_column_position = max_loc_left[0] + LeftColumnTemplate.shape[1] + fixed_distance_between_left_right
                left_column_position = max_loc_left[0]
            else:            
                # calcular la posición de la columna izquierda
                right_column_position = max_loc_right[0] + RightColumnTemplate.shape[1]
                left_column_position = max_loc_right[0] - fixed_distance_between_left_right

        # calcular la posición de la flecha
        middle_arrow_position = max_loc_middle[0]

        # calcular la distancia entre la flecha y la columna derecha
        distance_to_right = right_column_position - middle_arrow_position
        # calcular la distancia entre la flecha y la columna izquierda
        distance_to_left = middle_arrow_position - left_column_position

        # screenshot2 = screenshot.copy()
        # # dibujar un rectángulo en la columna derecha
        # cv.rectangle(screenshot2, (right_column_position, 0), (right_column_position + 1, screenshot.shape[0]), (0, 0, 255), 2)
        # # dibujar un rectángulo en la columna izquierda
        # cv.rectangle(screenshot2, (left_column_position, 0), (left_column_position + 1, screenshot.shape[0]), (0, 0, 255), 2)
        # # dibujar un rectángulo en la flecha
        # cv.rectangle(screenshot2, (middle_arrow_position, 0), (middle_arrow_position + 1, screenshot.shape[0]), (0, 255, 255), 2)

        press_key = False
        press_key_fast = False

        # si la distancia a la derecha es mayor a la distancia a la izquierda
        if distance_to_right > middle_offset:
            press_key = True
        # si la distancia a la izquierda es menor o igual a la distancia a la izquierda
        if distance_to_left <= left_middle_offset:
            press_key = True

        if press_key and distance_to_left < 0 and distance_to_right > 0:
            # print in red color
            # print('\033[91m' + 'DANGER ZONE PRESS KEY FAST' + '\033[0m')
            press_key_fast = True
        

        # cv.imshow('fishV2', screenshot2)
        # cv.waitKey(1)

        findImage = RunFindImage(src_window, images_path, 'fishIcon', captureworker.screenshot, 0.8, False, False)
        findImage2 = RunFindImage(src_window, images_path, 'exit_fishing', captureworker.screenshot, 0.8, False, False)
        if findImage['fishIcon'] != 'notfound':
            return "found"
        if findImage2['exit_fishing'] == 'notfound':
            return "found"
        findImage = RunFindImage(src_window, images_path, 'fishBeacon', captureworker.screenshot, 0.8, False, False)
        if findImage['fishBeacon'] != 'notfound':
            return "failed"
        if press_key:
            pyautogui.press('l')
            if press_key_fast == False:
                pyautogui.press('l')
                pyautogui.press('l')
                pyautogui.press('l')
            
















# if max_val_middle and max_val_middle >= precision:
            
#             distance_to_right = max_loc_right[0] - (max_loc_middle[0] + MiddleArrowTemplate.shape[1])
#             distance_to_left = max_loc_middle[0] - (max_loc_left[0] + LeftColumnTemplate.shape[1])

#             if distance_to_right > middle_offset:
#                 pyautogui.press('l')
#                 pyautogui.press('l')
#             if distance_to_left <= left_middle_offset:
#                 pyautogui.press('l')
#                 pyautogui.press('l')
#             precision_left = False
#             precision_right = False
#             if max_val_left >= precision and max_val_right >= precision:
                
#                 precision_left = True
#                 precision_right = True
#             elif max_val_left >= precision and max_val_right < precision:
#                 precision_left = True
#                 precision_right = False
#             elif max_val_left < precision and max_val_right >= precision:
#                 precision_left = False
#                 precision_right = True

#             if precision_left and precision_right:
#                 if max_loc_middle[0] <= max_loc_left[0] + LeftColumnTemplate.shape[1]:
#                     pyautogui.press('l')
#                     pyautogui.press('l')
#                 elif max_loc_middle[0] <= max_loc_right[0] - 95:
#                     pyautogui.press('l')
#                     pyautogui.press('l')
#             elif precision_left:
#                 if max_loc_middle[0] <= max_loc_left[0] + LeftColumnTemplate.shape[1]:
#                     pyautogui.press('l')
#                     pyautogui.press('l')
#             elif precision_right:
#                 if max_loc_middle[0] <= max_loc_right[0] - 95:
#                     pyautogui.press('l')
#                     pyautogui.press('l')
















# # (hMin = 12 , sMin = 47, vMin = 61), (hMax = 34 , sMax = 131, vMax = 154)
# # read image
# image = cv.imread('screenshot.png')

# # convert to hsv
# hsv = cv.cvtColor(image, cv.COLOR_BGR2HSV)

# # define range of blue color in HSV
# lower_blue = np.array([12, 47, 61])
# upper_blue = np.array([34, 131, 154])

# # threshold the hsv image to get only blue colors
# mask = cv.inRange(hsv, lower_blue, upper_blue)

# # Bitwise-AND mask and original image
# res = cv.bitwise_and(image, image, mask=mask)


# # generate lines from mask
# lines = cv.HoughLinesP(mask, 1, np.pi/180, 100, minLineLength=100, maxLineGap=10)

# # draw lines
# for line in lines:
#     x1, y1, x2, y2 = line[0]
#     cv.line(image, (x1, y1), (x2, y2), (0, 255, 0), 2)



# # show image
# cv.imshow('image', image)
# cv.imshow('mask', mask)
# cv.imshow('res', res)
# cv.waitKey(0)
