from windowcapture import WindowCapture
from preprocess import PreProcessImage
import cv2 as cv
import numpy as np
from getkeys import key_check

wincap = WindowCapture('LDPlayer')
preprocess = PreProcessImage()

resize_multiplier = 6

img_name = 0

while True:
    screenshot = wincap.get_screenshot()
    screenshot1 = preprocess.crop(screenshot, 660, 40, 250, 151)

    # screenshot1 = cv.resize(screenshot1, (0, 0),
    #                         fx=resize_multiplier, fy=resize_multiplier)

    preprocess.image_show('screenshot1', screenshot1, True)
    canny_image = preprocess.to_canny(screenshot1, 50, 150, 3)
    
    preprocess.image_show('canny_image', canny_image, True)

    if cv.waitKey(1) == ord('q'):
        cv.destroyAllWindows()
        break
    
    keys = key_check()
    if 'J' in keys:
        # capture only 1 image

        img_name += 1
        # save image in ./data/img_name.jpg
        cv.imwrite(f'./data/{img_name}.jpg', canny_image)
        print(f'Image {img_name} saved')