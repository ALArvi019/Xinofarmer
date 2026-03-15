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
nameFile = 'tundra'

# check if data directory exists
if not os.path.exists('./data'):
    os.makedirs('./data')

# check if data directory exists
if not os.path.exists('./data/{}'.format(nameFile)):
    os.makedirs('./data/{}'.format(nameFile))


while True:
    file_name = './data/' + nameFile + '/' + \
        nameFile + '-{}.npy'.format(starting_value)

    if os.path.isfile('./data/{}'.format(file_name)):
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


def main(file_name, starting_value):
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
    while (True):

        if not paused:
            screen = wincap.get_screenshot()
            minimap = preprocess.crop(screen, 740, 40, 173, 110)
            # resize to something a bit more acceptable for a CNN
            minimap = preprocess.resize(
                minimap, minimap.shape[1] * 2, minimap.shape[0] * 2)
            # # # # run a color convert:
            minimap = preprocess.to_rgb(minimap)
            preprocess.image_show('window', minimap, True,
                                  minimap.shape[1], minimap.shape[0])

            keys = key_check()
            output = keys_to_output(keys)

            if output != nk:
                training_data.append([minimap, output])

                if len(training_data) % 100 == 0:
                    print(len(training_data))

                    if len(training_data) == 1000:
                        print('SAVING')
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
                paused = True
                sleep(1)
        if cv.waitKey(1) == ord('q'):
            cv.destroyAllWindows()
            break


print('Done.')

main(file_name, starting_value)
