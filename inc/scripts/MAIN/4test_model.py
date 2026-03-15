from time import time
from time import sleep
import time
import numpy as np
import os
from pathlib import Path
import tensorflow as tf
from directkeys import PressKey, ReleaseKey, W, A, S, D
from windowcapture import WindowCapture
from preprocess import PreProcessImage
from getkeys import key_check
import cv2 as cv
from tensorflow import keras
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split

nameFile = 'marv1'
FILE_NAME = nameFile + "_clean"
EPOCHS = 30
MODEL_N = 'modelv1'
MODEL_NAME = 'marv1_clean-modelv1-1000-epochs.h5__model-774-0.9449'

w = [1, 0, 0, 0, 0, 0, 0, 0, 0]
s = [0, 1, 0, 0, 0, 0, 0, 0, 0]
a = [0, 0, 1, 0, 0, 0, 0, 0, 0]
d = [0, 0, 0, 1, 0, 0, 0, 0, 0]
wa = [0, 0, 0, 0, 1, 0, 0, 0, 0]
wd = [0, 0, 0, 0, 0, 1, 0, 0, 0]
sa = [0, 0, 0, 0, 0, 0, 1, 0, 0]
sd = [0, 0, 0, 0, 0, 0, 0, 1, 0]
nk = [0, 0, 0, 0, 0, 0, 0, 0, 1]

class_names = ['↑', '↓', '←', '→', '↖', '↗', '↙', '↘', 'NK']

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

def straight():
    PressKey(W)
    ReleaseKey(A)
    ReleaseKey(D)
    ReleaseKey(S)


def left():
    ReleaseKey(W)
    PressKey(A)
    ReleaseKey(S)
    ReleaseKey(D)
    # ReleaseKey(S)


def right():
    ReleaseKey(W)
    PressKey(D)
    ReleaseKey(A)
    ReleaseKey(S)


def reverse():
    PressKey(S)
    ReleaseKey(A)
    ReleaseKey(W)
    ReleaseKey(D)


def forward_left():
    PressKey(W)
    PressKey(A)
    ReleaseKey(D)
    ReleaseKey(S)


def forward_right():
    PressKey(W)
    PressKey(D)
    ReleaseKey(A)
    ReleaseKey(S)


def reverse_left():
    PressKey(S)
    PressKey(A)
    ReleaseKey(W)
    ReleaseKey(D)


def reverse_right():
    PressKey(S)
    PressKey(D)
    ReleaseKey(W)
    ReleaseKey(A)


def no_keys():
    ReleaseKey(W)
    ReleaseKey(A)
    ReleaseKey(S)
    ReleaseKey(D)


def main():
    # check if model exists
    if os.path.isfile("./models/{}".format(MODEL_NAME)):
        print('Model exists, loading previous model {}'.format(MODEL_NAME))
        model = keras.models.load_model("./models/{}".format(MODEL_NAME))
        print('Model loaded!')
    for i in list(range(4))[::-1]:
        print(i+1)
        time.sleep(1)

    paused = False
    wincap = WindowCapture('LDPlayer')
    preprocess = PreProcessImage()

    while (True):
        if paused:
            ReleaseKey(W)
            ReleaseKey(A)
            ReleaseKey(S)
            ReleaseKey(D)
            sleep(1)
            continue
        screen = wincap.get_screenshot()
        minimap1 = preprocess.crop(screen, 740, 40, 173, 110)
        minimap = preprocess.to_grayscale(minimap1)
        # RESIZE___________________________________________
        minimap = cv.resize(minimap, (173, 110), interpolation=cv.INTER_AREA)
        minimap = np.expand_dims(minimap, axis=2)
        # RESIZE___________________________________________
        minimap_correction = minimap.copy()
        minimap_copy = minimap.copy()
        preprocess.image_show('window', minimap, True,
                              minimap.shape[1], minimap.shape[0])
        preprocess.image_show('window1', minimap_copy, True,
                                minimap_copy.shape[1], minimap_copy.shape[0])

        prediction = model.predict(minimap.reshape(1, 173, 110, 1), verbose=0)
        max_value_index = np.argmax(prediction)
        print("dirección: ", class_names[max_value_index])

        if class_names[max_value_index] == '↑':
            straight()
        elif class_names[max_value_index] == '↓':
            reverse()
        elif class_names[max_value_index] == '←':
            left()
        elif class_names[max_value_index] == '→':
            right()
        elif class_names[max_value_index] == '↖':
            forward_left()
        elif class_names[max_value_index] == '↗':
            forward_right()
        elif class_names[max_value_index] == '↙':
            reverse_left()
        elif class_names[max_value_index] == '↘':
            reverse_right()
        elif class_names[max_value_index] == 'NK':
            no_keys()

        if not paused:
            keys = key_check()
        if 'V' in keys:
            paused = True
            starting_value = 1
            while True:
                file_name = './data/' + nameFile + '/' + \
                    nameFile + '-{}.npy'.format(starting_value)

                if os.path.isfile('./data/' + nameFile + '/' + nameFile + '-{}.npy'.format(starting_value)):
                    print('File exists, moving along', starting_value)
                    starting_value += 1
                else:
                    print('File does not exist, starting fresh!', starting_value)
                    break
            
            # ask in the console the correct direction
            pressKey = input('Press the correct direction: ↑: W\n↓: S\n←: A\n→: D\n↖: WA\n↗: WD\n↙: SA\n↘: SD\nNOKEY: NK\n')
            
            if len(pressKey) == 1:
                if pressKey == 'W':
                    pressKey = w
                elif pressKey == 'S':
                    pressKey = s
                elif pressKey == 'A':
                    pressKey = a
                elif pressKey == 'D':
                    pressKey = d
            elif len(pressKey) == 2:
                if pressKey == 'WA':
                    pressKey = wa
                elif pressKey == 'WD':
                    pressKey = wd
                elif pressKey == 'SA':
                    pressKey = sa
                elif pressKey == 'SD':
                    pressKey = sd

            training_data = []
            training_data.append([minimap_correction, pressKey])
            training_data = np.array(training_data, dtype=object)
            np.save(file_name, training_data)

            print('SAVED correct direction: ', pressKey)

            for i in list(range(4))[::-1]:
                print(i+1)
                time.sleep(1)
            paused = False


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


main()
