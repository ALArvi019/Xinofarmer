
from findObjectInMinimap import findSpecificItemOnMinimap
# lower: (79, 0, 55) upper: (127, 58, 159)
lower_1 = 50
lower_2 = 50
lower_3 = 56
upper_1 = 52
upper_2 = 52
upper_3 = 58
from preprocess import PreProcessImage
from captureWorker import CaptureWorker
from getkeys import key_check
import numpy as np
import cv2 as cv
import time

preprocess = PreProcessImage()


captureWorker = CaptureWorker('LDPlayer', 'path\\to\\immortal_xinofarmer\\inc\\img')
captureWorker.start()

# wait 5 seconds to start
for i in list(range(5))[::-1]:
    print(i+1)
    time.sleep(1)

while True:

    
        screenshot = captureWorker.screenshot
        # save image to file
        cv.imwrite('screenshot.png', screenshot)
        # read file from disk
        # screenshot =  cv.imread('screenshot.png')

        # movement, distance = findSpecificItemOnMinimap(
        #                     screenshot, "dungeon_chest", 1, True, [lower_1, lower_2, lower_3], [upper_1, upper_2, upper_3])
        
        # print("movement: " + str(movement) + " distance: " + str(distance))

        # screenshot = preprocess.crop(screenshot, 740, 40, 173, 110)
        # screenshot_hsv = cv.cvtColor(screenshot, cv.COLOR_BGR2HSV)
        # lower = np.array([lower_1, lower_2, lower_3])
        # upper = np.array([upper_1, upper_2, upper_3])

        # mask = cv.inRange(screenshot_hsv, lower, upper)

        # # # count = cv.countNonZero(mask)
        # detected_output = cv.bitwise_and(
        #     screenshot, screenshot, mask=mask)
        
        # # get position of mask in image
        # y, x = np.nonzero(mask)
        # # get center of mask
        # if len(x) != 0 and len(y) != 0:
        #     center_of_image = (int(np.mean(x)), int(np.mean(y)))

        # cv.circle(detected_output, center_of_image, 4, (255, 255, 0), -1)

        keys = key_check()
        if 1 == 2:
            if 'A' in keys:
                lower_1 = lower_1 + 1
                print("lower: (" + str(lower_1) + ", " + str(lower_2) + ", " + str(lower_3) + ") upper: (" + str(upper_1) + ", " + str(upper_2) + ", " + str(upper_3) + ")")
            if 'S' in keys:
                lower_2 = lower_2 + 1
                print("lower: (" + str(lower_1) + ", " + str(lower_2) + ", " + str(lower_3) + ") upper: (" + str(upper_1) + ", " + str(upper_2) + ", " + str(upper_3) + ")")
            if 'D' in keys:
                lower_3 = lower_3 + 1
                print("lower: (" + str(lower_1) + ", " + str(lower_2) + ", " + str(lower_3) + ") upper: (" + str(upper_1) + ", " + str(upper_2) + ", " + str(upper_3) + ")")
            if 'F' in keys:
                upper_1 = upper_1 + 1
                print("lower: (" + str(lower_1) + ", " + str(lower_2) + ", " + str(lower_3) + ") upper: (" + str(upper_1) + ", " + str(upper_2) + ", " + str(upper_3) + ")")
            if 'G' in keys:
                upper_2 = upper_2 + 1
                print("lower: (" + str(lower_1) + ", " + str(lower_2) + ", " + str(lower_3) + ") upper: (" + str(upper_1) + ", " + str(upper_2) + ", " + str(upper_3) + ")")
            if 'H' in keys:
                upper_3 = upper_3 + 1
                print("lower: (" + str(lower_1) + ", " + str(lower_2) + ", " + str(lower_3) + ") upper: (" + str(upper_1) + ", " + str(upper_2) + ", " + str(upper_3) + ")")
            if 'Z' in keys:
                lower_1 = lower_1 - 1
                print("lower: (" + str(lower_1) + ", " + str(lower_2) + ", " + str(lower_3) + ") upper: (" + str(upper_1) + ", " + str(upper_2) + ", " + str(upper_3) + ")")
            if 'X' in keys:
                lower_2 = lower_2 - 1
                print("lower: (" + str(lower_1) + ", " + str(lower_2) + ", " + str(lower_3) + ") upper: (" + str(upper_1) + ", " + str(upper_2) + ", " + str(upper_3) + ")")
            if 'C' in keys:
                lower_3 = lower_3 - 1
                print("lower: (" + str(lower_1) + ", " + str(lower_2) + ", " + str(lower_3) + ") upper: (" + str(upper_1) + ", " + str(upper_2) + ", " + str(upper_3) + ")")
            if 'V' in keys:
                upper_1 = upper_1 - 1
                print("lower: (" + str(lower_1) + ", " + str(lower_2) + ", " + str(lower_3) + ") upper: (" + str(upper_1) + ", " + str(upper_2) + ", " + str(upper_3) + ")")
            if 'B' in keys:
                upper_2 = upper_2 - 1
                print("lower: (" + str(lower_1) + ", " + str(lower_2) + ", " + str(lower_3) + ") upper: (" + str(upper_1) + ", " + str(upper_2) + ", " + str(upper_3) + ")")
            if 'N' in keys:
                upper_3 = upper_3 - 1
                print("lower: (" + str(lower_1) + ", " + str(lower_2) + ", " + str(lower_3) + ") upper: (" + str(upper_1) + ", " + str(upper_2) + ", " + str(upper_3) + ")")
        #     if 'Q' in keys:
        #         threshold_line = threshold_line + 1
        #         print("threshold_line: " + str(threshold_line) + " minLineLength: " + str(minLineLength) + " maxLineGap: " + str(maxLineGap))
        #     if 'W' in keys:
        #         minLineLength = minLineLength + 1
        #         print("threshold_line: " + str(threshold_line) + " minLineLength: " + str(minLineLength) + " maxLineGap: " + str(maxLineGap))
        #     if 'E' in keys:
        #         maxLineGap = maxLineGap + 1
        #         print("threshold_line: " + str(threshold_line) + " minLineLength: " + str(minLineLength) + " maxLineGap: " + str(maxLineGap))
        #     if 'R' in keys:
        #         threshold_line = threshold_line - 1
        #         print("threshold_line: " + str(threshold_line) + " minLineLength: " + str(minLineLength) + " maxLineGap: " + str(maxLineGap))
        #     if 'T' in keys:
        #         minLineLength = minLineLength - 1
        #         print("threshold_line: " + str(threshold_line) + " minLineLength: " + str(minLineLength) + " maxLineGap: " + str(maxLineGap))
        #     if 'Y' in keys:
        #         maxLineGap = maxLineGap - 1
        #         print("threshold_line: " + str(threshold_line) + " minLineLength: " + str(minLineLength) + " maxLineGap: " + str(maxLineGap))



        # cv.imshow('detected_output', detected_output)
        # cv.waitKey(1)
        time.sleep(1)