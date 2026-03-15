import numpy as np
from windowcapture import WindowCapture
from preprocess import PreProcessImage
import cv2 as cv
from getkeys import key_check
import os
from time import time
from time import sleep

minimap_only = True

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
nameFile = 'ancients'
rectangle_fix = (39, 82)
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

def apply_dungeon_mask(screenshot):
        # mask = cv.imread('..\..\img\game_items\game_mask.png', cv.IMREAD_UNCHANGED)
        mask = cv.imread('.\dungeon_game_mask.png', cv.IMREAD_UNCHANGED)

        if mask.shape[-1] == 4:
            mask = cv.cvtColor(mask, cv.COLOR_BGRA2GRAY)

        # Crear una imagen de fondo negro sólido con el mismo tamaño que la captura de pantalla
        background = np.zeros_like(screenshot)

        # Copiar los canales RGB de la captura de pantalla a la imagen de fondo
        background[:, :, 0] = screenshot[:, :, 0]
        background[:, :, 1] = screenshot[:, :, 1]
        background[:, :, 2] = screenshot[:, :, 2]

        # Aplicar la máscara en la imagen de fondo
        screenshot = cv.bitwise_and(background, background, mask=mask)

        return screenshot


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
            # save image
            cv.imwrite('image.png', screen)
            if minimap_only:
                minimap1 = preprocess.crop(screen, 740, 40, 173, 110)
                # draw black circle in 87, 57
                cv.circle(minimap1, (86, 56), 14, (0, 0, 0), -1)
                # draw black rectangle from 69, 473 to right, down
                cv.rectangle(minimap1, rectangle_fix, (minimap1.shape[1], minimap1.shape[0]), (0, 0, 0), -1)
            else:
                minimap1 = apply_dungeon_mask(screen)
            minimap = preprocess.to_grayscale(minimap1)
            # get the size of the image
            # print('width: ', minimap.shape[1], 'height: ', minimap.shape[0])
            # RESIZE___________________________________________
            minimap = cv.resize(minimap, (minimap.shape[1], minimap.shape[0]), interpolation=cv.INTER_AREA)
            minimap = np.expand_dims(minimap, axis=2)
            # RESIZE___________________________________________
            preprocess.image_show('window', minimap, True,
                                  minimap.shape[1], minimap.shape[0])

            keys = key_check()
            output = keys_to_output(keys)

            if output != nk:
            # if 1 == 1:
                training_data.append([minimap, output])

                if len(training_data) % 100 == 0:
                        print(len(training_data))
                        samples += len(training_data)
                        sleep(1)
                        if len(training_data) == 300:
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
                # cv.putText(minimap, 'P', (int(minimap.shape[1]/2), int(
                #     minimap.shape[0]/2)), cv.FONT_HERSHEY_SIMPLEX, 2, (255, 255, 255), 3)
                # preprocess.image_show('window', minimap, True,
                #                       minimap.shape[1], minimap.shape[0])
                paused = True
                sleep(1)

        if cv.waitKey(1) == ord('q'):
            cv.destroyAllWindows()
            break


print('Done.')

main(file_name, starting_value, samples)
