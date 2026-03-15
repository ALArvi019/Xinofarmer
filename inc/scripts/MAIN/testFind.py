from windowcapture import WindowCapture
from preprocess import PreProcessImage
import cv2 as cv
# import sys

def RunFindImage(src_window, images_path, image_name):

    wincap = WindowCapture(src_window)
    preprocess = PreProcessImage()

    image_template = cv.imread(str(images_path + '/' + image_name + '.png'), 0)

    # get the shape of the template
    template_height, template_width = image_template.shape[:2]

    screenshot1 = wincap.get_screenshot()
    screenshot1 = preprocess.crop(screenshot1, 0, 0, 1002, 575)

    screenshot = preprocess.to_grayscale(screenshot1)

    Res = cv.matchTemplate(
            screenshot, image_template, cv.TM_CCOEFF_NORMED)
    _, max_val_left, _, max_loc_left = cv.minMaxLoc(Res)

    # show the max_val_left in image
    cv.putText(screenshot1, str(max_val_left), (0, 50), cv.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
    cv.rectangle(screenshot1, max_loc_left, (max_loc_left[0] + template_width, max_loc_left[1] + template_height),
                  (0, 255, 255), 2)
    preprocess.image_show('image', screenshot1)
    if cv.waitKey() == ord('q'):
        cv.destroyAllWindows()

    if max_val_left >= 0.8:

        


        # get the center of the match
        match_x_left = max_loc_left[0] + int(template_width / 2)
        match_y_left = max_loc_left[1] + int(template_height / 2)
        
        return str(match_x_left) + '|' + str(match_y_left)
    else:
        # print('notfound')
        return 'notfound'
    

    



# get arguments from command line
# src_window = sys.argv[1]
# images_path = sys.argv[2]
# image_name = sys.argv[3]

RunFindImage('LDPlayer', 'path\\to\\immortal_xinofarmer\\inc\\img','fisherman' )
# RunFindImage('XAXA', 'C:\\Users\\patri\\Desktop\\farrrm\\inc\\img','fisherman' )