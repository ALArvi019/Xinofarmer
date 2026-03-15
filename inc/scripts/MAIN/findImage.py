from windowcapture import WindowCapture
from preprocess import PreProcessImage
import cv2 as cv
# import sys

debug_image = []

def RunFindImage(src_window, images_path, image_name, screenshot=None, threshold=0.8, returnPrecision=False, gray=True):
    try: 
        # convert to float
        threshold = float(threshold)

        wincap = WindowCapture(src_window)
        preprocess = PreProcessImage()

        # check if image_name is a tuple
        if not isinstance(image_name, tuple):
            image_name = (image_name,)

        FoundedImages = {}

        if screenshot is None:
            screenshot = wincap.get_screenshot()
        screenshot1 = screenshot
        screenshot1 = preprocess.crop(screenshot1, 0, 0, 1002, 575)

        if gray:
            screenshot = preprocess.to_grayscale(screenshot1)

        for i in range(len(image_name)):
            if gray:
                image_template = cv.imread(
                    str(images_path + '/' + image_name[i] + '.png'), cv.IMREAD_GRAYSCALE)
            else:
                image_template = cv.imread(
                    str(images_path + '/' + image_name[i] + '.png'))

            # get the shape of the template
            template_height, template_width = image_template.shape[:2]

            Res = cv.matchTemplate(
                screenshot, image_template, cv.TM_CCOEFF_NORMED)
            _, max_val_left, _, max_loc_left = cv.minMaxLoc(Res)

            # avoid memory leak
            del Res

            if image_name[i] in debug_image:
                # print in blue
                # print(image_name[i] + ' ' + str(max_val_left))
                print("\033[1;34;40m [IMAGE_FOUND] \033[0m" + image_name[i] + ' ' + str(max_val_left))

                cv.rectangle(screenshot1, max_loc_left, (max_loc_left[0] + template_width, max_loc_left[1] + template_height),
                            (0, 255, 0), 2)
                cv.putText(screenshot1, image_name[i], (max_loc_left[0] + 10, max_loc_left[1] + 10),
                        cv.FONT_HERSHEY_COMPLEX, 0.5, (0, 255, 0), 1)
                preprocess.image_show('findImage0', screenshot1)

            if max_val_left >= threshold:


                if image_name[i] in debug_image:
                    cv.rectangle(screenshot1, max_loc_left, (max_loc_left[0] + template_width, max_loc_left[1] + template_height),
                            (0, 0, 255), 2)
                    cv.putText(screenshot1, image_name[i], (max_loc_left[0] + 10, max_loc_left[1] + 10),
                                cv.FONT_HERSHEY_COMPLEX, 0.5, (0, 0, 255), 1)
                    
                    preprocess.image_show('findImage1', screenshot1)

                # get the center of the match
                match_x_left = max_loc_left[0] + int(template_width / 2)
                match_y_left = max_loc_left[1] + int(template_height / 2)

                if returnPrecision == False:
                    FoundedImages[image_name[i]] = str(
                        match_x_left) + '|' + str(match_y_left)
                else:
                    FoundedImages[image_name[i]] = str(
                        match_x_left) + '|' + str(match_y_left) + '|' + str(max_val_left)
            else:
                FoundedImages[image_name[i]] = 'notfound'
        # clean all variables for avoid memory leak
        del screenshot
        del screenshot1
        del wincap
        del preprocess
        del image_template
        del template_height
        del template_width
        del max_val_left
        del max_loc_left
        del threshold
        del src_window
        del images_path
        del image_name
        del returnPrecision
    
    except Exception as e:
        print('Error in RunFindImage: ' + str(e))
        for i in range(len(image_name)):
            FoundedImages[image_name[i]] = 'notfound'

    
    # if cv.waitKey(1) == ord('q'):
    #     cv.destroyAllWindows()

    # print(FoundedImages)

    return FoundedImages




# while True:
    # RunFindImage("LDPlayer", "path\\to\\immortal_xinofarmer\\inc\\img",
    #              ('health_globe1', 'health_globe2', 'gold1', 'gold_label', 'close_item',
    #               'monstrous_essence', 'health_globe_label_en'),
    #              None, 0.8, True)
