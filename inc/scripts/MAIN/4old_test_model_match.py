import numpy as np
import os
from windowcapture import WindowCapture
from preprocess import PreProcessImage
import cv2 as cv
from directkeys import PressKey, ReleaseKey, W, A, S, D
import random

w = [1, 0, 0, 0, 0, 0, 0, 0, 0]
s = [0, 1, 0, 0, 0, 0, 0, 0, 0]
a = [0, 0, 1, 0, 0, 0, 0, 0, 0]
d = [0, 0, 0, 1, 0, 0, 0, 0, 0]
wa = [0, 0, 0, 0, 1, 0, 0, 0, 0]
wd = [0, 0, 0, 0, 0, 1, 0, 0, 0]
sa = [0, 0, 0, 0, 0, 0, 1, 0, 0]
sd = [0, 0, 0, 0, 0, 0, 0, 1, 0]
nk = [0, 0, 0, 0, 0, 0, 0, 0, 1]


def print_key(choice):
    if choice == w:
        print('w')
    elif choice == s:
        print('s')
    elif choice == a:
        print('a')
    elif choice == d:
        print('d')
    elif choice == wa:
        print('wa')
    elif choice == wd:
        print('wd')
    elif choice == sa:
        print('sa')
    elif choice == sd:
        print('sd')
    elif choice == nk:
        print('nk')


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

    if random.randrange(0, 3) == 1:
        PressKey(W)
    else:
        ReleaseKey(W)
    ReleaseKey(A)
    ReleaseKey(S)
    ReleaseKey(D)


fileName = "marv1_clean"
starting_value = 1

wincap = WindowCapture('LDPlayer')
preprocess = PreProcessImage()

training_data = []

# while file exists, keep loading and appending to list
while True:
    file_name = './data/' + fileName + '/' + \
        fileName + '-{}.npy'.format(starting_value)

    if os.path.isfile(file_name):
        training_data_tmp = np.load(file_name, allow_pickle=True)
        print('training_data_tmp: ', len(training_data_tmp))
        # add training_data_tmp to training_data
        for data in training_data_tmp:
            training_data.append(data)
        print('training_data: ', len(training_data))
        starting_value += 1
    else:
        break




while True:

    screen = wincap.get_screenshot()
    minimap1 = preprocess.crop(screen, 740, 40, 173, 110)
    minimap = preprocess.to_grayscale(minimap1)

    max_match_value = 0
    index_position = 0
    best_index = 0
    best_choice = nk

    # search the match between training_data and minimap
    for data in training_data:
        img = data[0]
        choice = data[1]
        index = index_position

        result = cv.matchTemplate(img, minimap, cv.TM_CCOEFF_NORMED)
        min_val, max_val, min_loc, max_loc = cv.minMaxLoc(result)
        top_left = max_loc
        # save index, max_val and choice in tmp_max_val_data
        # tmp_max_val_data.append([index, max_val, choice])
        if max_val > max_match_value:
            max_match_value = max_val
            best_choice = choice
            best_index = index

        index_position += 1

    # found all equal choices in training_data
    # tmp_equal_choices = []
    # for tmp_data in tmp_max_val_data:
    #     if tmp_data[2] == best_choice:
    #         print('tmp_data: [', tmp_data[0], ', ',
    #               tmp_data[1], ', ', tmp_data[2], ']')
    #         tmp_equal_choices.append(tmp_data)

    # # delete
    # for tmp_data in tmp_equal_choices:
        # if tmp_data[1] == max_match_value:
            

    print('best_index: ', best_index)
    print('training_data: ', len(training_data))
    # print(len(tmp_equal_choices))

    print_key(best_choice)
    if best_choice == w:
        straight()
    elif best_choice == s:
        reverse()
    elif best_choice == a:
        left()
    elif best_choice == d:
        right()
    elif best_choice == wa:
        forward_left()
    elif best_choice == wd:
        forward_right()
    elif best_choice == sa:
        reverse_left()
    elif best_choice == sd:
        reverse_right()
    elif best_choice == nk:
        no_keys()

    if cv.waitKey(1) & 0xFF == ord('q'):
        cv.destroyAllWindows()
        break

    starting_value += 1
