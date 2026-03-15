from windowcapture import WindowCapture
from preprocess import PreProcessImage
from findImage import RunFindImage
import cv2 as cv
import pyautogui
import time

def RunFish(src_window, images_path, fish_type):
    # print('RunFish')
    wincap = WindowCapture(src_window)
    preprocess = PreProcessImage()

    if fish_type == 'Legendary' or fish_type == 'Epic':
        fish_type = 'Gold'

    LeftColumnTemplate = cv.imread(str(images_path + '/LeftColumn' + fish_type + '.png'), 0)
    RightColumnTemplate = cv.imread(str(images_path + '/RightColumn' + fish_type + '.png'), 0)
    MiddleArrowTemplate = cv.imread(str(images_path + '/Arrow' + fish_type + '.png'), 0)

    precision = 0.8

    while True:
        screenshot0 = wincap.get_screenshot()
        screenshot1 = preprocess.crop(screenshot0, 275, 85, 412, 40)

        screenshot = preprocess.to_grayscale(screenshot1)

        LeftRes = cv.matchTemplate(
            screenshot, LeftColumnTemplate, cv.TM_CCOEFF_NORMED)
        _, max_val_left, _, max_loc_left = cv.minMaxLoc(LeftRes)

        RightRes = cv.matchTemplate(
            screenshot, RightColumnTemplate, cv.TM_CCOEFF_NORMED)
        _, max_val_right, _, max_loc_right = cv.minMaxLoc(RightRes)

        MiddleRes = cv.matchTemplate(
            screenshot, MiddleArrowTemplate, cv.TM_CCOEFF_NORMED)
        _, max_val_middle, _, max_loc_middle = cv.minMaxLoc(MiddleRes)

        # draw in the screenshot the rectangles
        # screenshot2 = screenshot1
        # cv.rectangle(screenshot2, max_loc_left,
        #             (max_loc_left[0] + 50, max_loc_left[1] + 40), (0, 0, 255), 2)
        # cv.rectangle(screenshot2, max_loc_right,
        #             (max_loc_right[0] + 50, max_loc_right[1] + 40), (0, 0, 255), 2)
        # cv.rectangle(screenshot2, max_loc_middle,
        #             (max_loc_middle[0] + 50, max_loc_middle[1] + 40), (0, 255, 255), 2)
        
        # # draw max_val_middle and max_val_middle >= precision in screenshot2
        # cv.putText(screenshot2, str(max_val_middle), (max_loc_middle[0], max_loc_middle[1] - 10), cv.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 255), 1, cv.LINE_AA)

        if max_val_middle and max_val_middle >= precision:
            # print(str(max_val_left) + '-' + str(max_val_middle) + '-' + str(max_val_right))
            precision_left = False
            precision_right = False
            if max_val_left >= precision and max_val_right >= precision:
                precision_left = True
                precision_right = True
            elif max_val_left >= precision and max_val_right < precision:
                precision_left = True
                precision_right = False
            elif max_val_left < precision and max_val_right >= precision:
                precision_left = False
                precision_right = True

            wLeft, hLeft = LeftColumnTemplate.shape[::-1]
            wRight, hRight = RightColumnTemplate.shape[::-1]
            wMiddle, hMiddle = MiddleArrowTemplate.shape[::-1]


            # cv.rectangle(screenshot1, max_loc_left,
            #             (max_loc_left[0] + wLeft, max_loc_left[1] + hLeft), (0, 0, 255), 2)
            # cv.rectangle(screenshot1, max_loc_right,
            #             (max_loc_right[0] + wRight, max_loc_right[1] + hRight), (0, 0, 255), 2)
            # cv.rectangle(screenshot1, max_loc_middle,
            #             (max_loc_middle[0] + wMiddle, max_loc_middle[1] + hMiddle), (0, 255, 255), 2)
            
            if precision_left == True and precision_right == True:
                if max_loc_middle[0] <= max_loc_left[0] + wLeft:
                    # print ('left1')
                    pyautogui.press('l')
                    pyautogui.press('l')
                elif max_loc_middle[0] <= max_loc_right[0] - 95:
                    # print ('right1')
                    pyautogui.press('l')
                    pyautogui.press('l')
            if precision_left == True and precision_right == False:
                if max_loc_middle[0] <= max_loc_left[0] + wLeft:
                    # print ('left')
                    pyautogui.press('l')
                    pyautogui.press('l')
            elif precision_left == False and precision_right == True:
                if max_loc_middle[0] <= max_loc_right[0] - 95:
                    # print ('right')
                    pyautogui.press('l')
                    pyautogui.press('l')

            # check if max_loc_middle is more than 95 pixels away from max_loc_right
            # elif max_loc_middle[0] >= max_loc_right[0] - 95:
            #     pyautogui.press('r')
            #     pyautogui.press('r')

        findImage = RunFindImage(src_window, images_path, 'fishIcon', screenshot0, 0.8, False, False)
        if findImage['fishIcon'] != 'notfound':
            return "found"
        
        findImage = RunFindImage(src_window, images_path, 'fishBeacon', screenshot0, 0.8, False, False)
        if findImage['fishBeacon'] != 'notfound':
            return "failed"


        # preprocess.image_show('fishImage', screenshot1)
        # # preprocess.image_show('fishImage2', screenshot2)
        # if cv.waitKey(1) == ord('q'):
        #    cv.destroyAllWindows()
        #    break
        # time.sleep(0.5)


def RunFisha(src_window, images_path, fish_type):
    # print('RunFish')
    wincap = WindowCapture(src_window)
    preprocess = PreProcessImage()

    LeftColumnTemplate = cv.imread(str(images_path + '/LeftColumn' + fish_type + '.png'))
    RightColumnTemplate = cv.imread(str(images_path + '/RightColumn' + fish_type + '.png'))
    MiddleArrowTemplate = cv.imread(str(images_path + '/Arrow' + fish_type + '.png'))

    precision = 0.8

    while True:
        screenshot0 = wincap.get_screenshot()
        screenshot1 = preprocess.crop(screenshot0, 275, 85, 412, 40)

        # No need to convert to grayscale because the images are already in color

        LeftRes = cv.matchTemplate(
            screenshot1, LeftColumnTemplate, cv.TM_CCOEFF_NORMED)
        _, max_val_left, _, max_loc_left = cv.minMaxLoc(LeftRes)

        RightRes = cv.matchTemplate(
            screenshot1, RightColumnTemplate, cv.TM_CCOEFF_NORMED)
        _, max_val_right, _, max_loc_right = cv.minMaxLoc(RightRes)

        MiddleRes = cv.matchTemplate(
            screenshot1, MiddleArrowTemplate, cv.TM_CCOEFF_NORMED)
        _, max_val_middle, _, max_loc_middle = cv.minMaxLoc(MiddleRes)

        # draw in the screenshot the rectangles
        # screenshot2 = screenshot1
        # cv.rectangle(screenshot2, max_loc_left,
        #             (max_loc_left[0] + 50, max_loc_left[1] + 40), (0, 0, 255), 2)
        # cv.rectangle(screenshot2, max_loc_right,
        #             (max_loc_right[0] + 50, max_loc_right[1] + 40), (0, 0, 255), 2)
        # cv.rectangle(screenshot2, max_loc_middle,
        #             (max_loc_middle[0] + 50, max_loc_middle[1] + 40), (0, 255, 255), 2)
        
        # # draw max_val_middle and max_val_middle >= precision in screenshot2
        # cv.putText(screenshot2, str(max_val_middle), (max_loc_middle[0], max_loc_middle[1] - 10), cv.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 255), 1, cv.LINE_AA)

        if max_val_middle and max_val_middle >= precision:
            # print(str(max_val_left) + '-' + str(max_val_middle) + '-' + str(max_val_right))
            precision_left = False
            precision_right = False
            if max_val_left >= precision and max_val_right >= precision:
                precision_left = True
                precision_right = True
            elif max_val_left >= precision and max_val_right < precision:
                precision_left = True
                precision_right = False
            elif max_val_left < precision and max_val_right >= precision:
                precision_left = False
                precision_right = True

            wLeft, hLeft = LeftColumnTemplate.shape[::-1]
            wRight, hRight = RightColumnTemplate.shape[::-1]
            wMiddle, hMiddle = MiddleArrowTemplate.shape[::-1]



            # cv.rectangle(screenshot1, max_loc_left,
            #             (max_loc_left[0] + wLeft, max_loc_left[1] + hLeft), (0, 0, 255), 2)
            # cv.rectangle(screenshot1, max_loc_right,
            #             (max_loc_right[0] + wRight, max_loc_right[1] + hRight), (0, 0, 255), 2)
            # cv.rectangle(screenshot1, max_loc_middle,
            #             (max_loc_middle[0] + wMiddle, max_loc_middle[1] + hMiddle), (0, 255, 255), 2)
            
            if precision_left == True and precision_right == True:
                if max_loc_middle[0] <= max_loc_left[0] + wLeft:
                    # print ('left1')
                    pyautogui.press('l')
                    pyautogui.press('l')
                elif max_loc_middle[0] <= max_loc_right[0] - 95:
                    # print ('right1')
                    pyautogui.press('l')
                    pyautogui.press('l')
            if precision_left == True and precision_right == False:
                if max_loc_middle[0] <= max_loc_left[0] + wLeft:
                    # print ('left')
                    pyautogui.press('l')
                    pyautogui.press('l')
            elif precision_left == False and precision_right == True:
                if max_loc_middle[0] <= max_loc_right[0] - 95:
                    # print ('right')
                    pyautogui.press('l')
                    pyautogui.press('l')

            # check if max_loc_middle is more than 95 pixels away from max_loc_right
            # elif max_loc_middle[0] >= max_loc_right[0] - 95:
            #     pyautogui.press('r')
            #     pyautogui.press('r')

        findImage = RunFindImage(src_window, images_path, 'fishIcon', screenshot0, 0.8, False, False)
        if findImage['fishIcon'] != 'notfound':
            return "found"
        findImage = RunFindImage(src_window, images_path, 'fishBeacon', screenshot0, 0.8, False, False)
        if findImage['fishBeacon'] != 'notfound':
            return "failed"


        preprocess.image_show('fishImage', screenshot1)
        # preprocess.image_show('fishImage2', screenshot2)
        if cv.waitKey(1) == ord('q'):
           cv.destroyAllWindows()
           break
        # time.sleep(0.5)
