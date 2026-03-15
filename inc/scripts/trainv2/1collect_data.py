import numpy as np
from windowcapture import WindowCapture
from preprocess import PreProcessImage
import cv2 as cv
from getkeys import key_check
import os
from time import time
from time import sleep

os.chdir(os.path.dirname(os.path.abspath(__file__)))

w = [1, 0, 0, 0, 0, 0, 0, 0, 0]
s = [0, 1, 0, 0, 0, 0, 0, 0, 0]
a = [0, 0, 1, 0, 0, 0, 0, 0, 0]
d = [0, 0, 0, 1, 0, 0, 0, 0, 0]
wa = [0, 0, 0, 0, 1, 0, 0, 0, 0]
wd = [0, 0, 0, 0, 0, 1, 0, 0, 0]
sa = [0, 0, 0, 0, 0, 0, 1, 0, 0]
sd = [0, 0, 0, 0, 0, 0, 0, 1, 0]
nk = [0, 0, 0, 0, 0, 0, 0, 0, 1]

starting_value = 1
nameFile = 'rotonda'
samples = 0

# check if data directory exists
if not os.path.exists('./data'):
    os.makedirs('./data')

# check if data directory exists
if not os.path.exists('./data/{}'.format(nameFile)):
    os.makedirs('./data/{}'.format(nameFile))


while True:
    file_name = './data/' + nameFile + '/' + \
        nameFile + '-{}.npy'.format(starting_value)

    if os.path.isfile('./data/' + nameFile + '/' + nameFile + '-{}.npy'.format(starting_value)):
        print('File exists, moving along', starting_value)
        starting_value += 1
    else:
        print('File does not exist, starting fresh!', starting_value)

        break


def keys_to_output(keys):
    '''
    Convert keys to a ...multi-hot... array
     0  1  2  3  4   5   6   7    8
    [W, S, A, D, WA, WD, SA, SD, NOKEY] boolean values.
    '''
    output = [0, 0, 0, 0, 0, 0, 0, 0, 0]

    if 'W' in keys and 'A' in keys:
        output = wa
    elif 'W' in keys and 'D' in keys:
        output = wd
    elif 'S' in keys and 'A' in keys:
        output = sa
    elif 'S' in keys and 'D' in keys:
        output = sd
    elif 'W' in keys:
        output = w
    elif 'S' in keys:
        output = s
    elif 'A' in keys:
        output = a
    elif 'D' in keys:
        output = d
    else:
        output = nk
    return output


def main(file_name, starting_value, samples):
    file_name = file_name
    starting_value = starting_value
    training_data = []
    images_array = []
    for i in list(range(4))[::-1]:
        print(i+1)
        sleep(1)

    wincap = WindowCapture('LDPlayer')
    preprocess = PreProcessImage()

    last_time = time()
    paused = False
    print('STARTING!!!')
    minthhreshold = 69
    maxthhreshold = 473
    while (True):

        if not paused:
            screen = wincap.get_screenshot()
            minimap1 = preprocess.crop(screen, 740, 40, 173, 110)
            # resize to something a bit more acceptable for a CNN
            # minimap = preprocess.resize(
            #      minimap, minimap.shape[1] * 2, minimap.shape[0] * 2)
            # # # # run a color convert:
            minimap = preprocess.to_grayscale(minimap1)
            # # add more contrast to the image
            # minimap = preprocess.increase_contrast(minimap, 3)

            # # increase edge contrast
            # minimap = preprocess.increase_edge_contrast(minimap, 30)

            # # # image shappering
            # minimap = preprocess.image_sharpening(minimap, 3)

            # minimap = preprocess.to_canny(
            #     minimap, minthhreshold, maxthhreshold, 3)

            # _, thresh = cv.threshold(
            #     minimap, minthhreshold, maxthhreshold, cv.THRESH_BINARY)
            # kernel = cv.getStructuringElement(cv.MORPH_ELLIPSE, (5, 5))
            # opening = cv.morphologyEx(thresh, cv.MORPH_OPEN, kernel)
            # masked_img = cv.bitwise_and(minimap1, minimap1, mask=opening)
            # minimap = preprocess.to_canny(minimap, 140, 200, 3)
            preprocess.image_show('window', minimap, True,
                                  minimap.shape[1], minimap.shape[0])
            # preprocess.image_show('window2', thresh, True,
            #                        minimap.shape[1], minimap.shape[0])
            # preprocess.image_show('window3', opening, True,
            #                        minimap.shape[1], minimap.shape[0])

            keys = key_check()
            output = keys_to_output(keys)

            if output != nk:
                training_data.append([minimap, output])

                if len(training_data) % 100 == 0:
                    print(len(training_data))
                    samples += len(training_data)

                    if len(training_data) == 500:
                        print('SAVING sample: ', samples)
                        # transform to numpy array
                        training_data = np.array(training_data, dtype=object)
                        np.save(file_name, training_data)
                        print('SAVED')
                        training_data = []
                        starting_value += 1
                        file_name = './data/' + nameFile + '/' + \
                            nameFile + '-{}.npy'.format(starting_value)

        keys = key_check()
        if 'T' in keys:
            if paused:
                paused = False
                print('unpaused!')
                sleep(1)
            else:
                print('Pausing!')
                # print letter P in color green in the middel of minimap image with opencv
                cv.putText(minimap, 'P', (int(minimap.shape[1]/2), int(
                    minimap.shape[0]/2)), cv.FONT_HERSHEY_SIMPLEX, 2, (255, 255, 255), 3)
                preprocess.image_show('window', minimap, True,
                                      minimap.shape[1], minimap.shape[0])
                paused = True
                sleep(1)
         # if press a key on keyboard, then sum 1 to minthhreshold
        # if 'A' in keys:
        #     minthhreshold += 1
        #     print('minthhreshold: ', minthhreshold)
        #     sleep(0.1)
        #     # if press Z key on keyboard, then sub 1 to MAXTHHRESHOLD
        # if 'Z' in keys:
        #     minthhreshold -= 1
        #     print('minthhreshold: ', minthhreshold)
        #     sleep(0.1)
        #     # if press S key on keyboard, then sum 1 to MAXTHHRESHOLD
        # if 'S' in keys:
        #     maxthhreshold += 1
        #     print('maxthhreshold: ', maxthhreshold)
        #     sleep(0.1)
        #     # if press X key on keyboard, then sub 1 to MAXTHHRESHOLD
        # if 'X' in keys:
        #     maxthhreshold -= 1
        #     print('maxthhreshold: ', maxthhreshold)
        #     sleep(0.1)

        if cv.waitKey(1) == ord('q'):
            cv.destroyAllWindows()
            break


print('Done.')

main(file_name, starting_value, samples)
