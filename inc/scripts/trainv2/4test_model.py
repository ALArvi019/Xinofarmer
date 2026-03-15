import numpy as np
from windowcapture import WindowCapture
from preprocess import PreProcessImage
import cv2 as cv
import time
from directkeys import PressKey, ReleaseKey, W, A, S, D
from models import otherception3 as googlenet
from getkeys import key_check
from collections import deque, Counter
import random
from statistics import mode, mean
import numpy as np
from motion import motion_detection
import matplotlib.pyplot as plt
from pathlib import Path

GAME_WIDTH = 1920
GAME_HEIGHT = 1080

how_far_remove = 800
rs = (20, 15)
log_len = 25

motion_req = 800
motion_log = deque(maxlen=log_len)
canny_low_threshold = 0
canny_high_threshold = 30
canny_kernel_dimension = 3

hough_thtreshold = 57
hough_minLineLength = 70
hough_maxLineGap = 20

player_x = 520
player_y = 340
player_size = 25

WIDTH = 173
HEIGHT = 110
LR = 1e-3
EPOCHS = 30
MODEL_N = 'otherception3v3'
FILE_NAME = "zavainGPU"

MODEL_NAME = FILE_NAME + \
    '-{}-{}-{}-epochs.model'.format(LR, MODEL_N, EPOCHS)

data_dir = Path('./data') / FILE_NAME
model_dir = Path('./models')
model_file = model_dir / MODEL_NAME

choices = deque([], maxlen=5)
hl_hist = 250
choice_hist = deque([], maxlen=hl_hist)

w = [1, 0, 0, 0, 0, 0, 0, 0, 0]
s = [0, 1, 0, 0, 0, 0, 0, 0, 0]
a = [0, 0, 1, 0, 0, 0, 0, 0, 0]
d = [0, 0, 0, 1, 0, 0, 0, 0, 0]
wa = [0, 0, 0, 0, 1, 0, 0, 0, 0]
wd = [0, 0, 0, 0, 0, 1, 0, 0, 0]
sa = [0, 0, 0, 0, 0, 0, 1, 0, 0]
sd = [0, 0, 0, 0, 0, 0, 0, 1, 0]
nk = [0, 0, 0, 0, 0, 0, 0, 0, 1]

t_time = 0.25


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

    if random.randrange(0, 3) == 1:
        PressKey(W)
    else:
        ReleaseKey(W)
    ReleaseKey(A)
    ReleaseKey(S)
    ReleaseKey(D)


model = googlenet(WIDTH, HEIGHT, 3, LR, output=9)
model.load(model_file)

print('We have loaded a previous model!!!!')


def main():
    last_time = time.time()
    for i in list(range(4))[::-1]:
        print(i+1)
        time.sleep(1)

    paused = False
    mode_choice = 0
    wincap = WindowCapture('LDPlayer')
    preprocess = PreProcessImage()
    last_frames = []
    while (True):

        if not paused:
            screen = wincap.get_screenshot()
            minimap1 = preprocess.crop(screen, 740, 40, 173, 110)

            minimap = preprocess.to_grayscale(minimap1)

            # Preprocess the image
            edges = preprocess.to_canny(
                minimap, canny_low_threshold, canny_high_threshold, canny_kernel_dimension)
            lines = preprocess.get_lines(
                edges, hough_thtreshold, hough_minLineLength, hough_maxLineGap)

            preprocess.draw_lines(minimap1, lines, (0, 255, 0), 2)
            preprocess.print_player_position(
                minimap1, player_x, player_y, player_size, (255, 0, 255), 2)
            preprocess.draw_coliision_between_player_and_lines(
                minimap1, lines, player_x, player_y, player_size, (0, 0, 255), 2)

            preprocess.image_show('screenshot', minimap1)

            if cv.waitKey(1) == ord('q'):
                cv.destroyAllWindows()
                break

            last_frames.append(minimap)

            last_time = time.time()

            # plt show image minimap
            # plt.imshow(minimap)
            # plt.show()

            # plt.imshow(minimap.reshape(WIDTH, HEIGHT, 1))
            # plt.show()

            # plt.imshow(minimap.reshape(HEIGHT, WIDTH, 1))
            # plt.show()

            # plt.imshow(minimap)
            # plt.show()

            # cv2.imshow('window', minimap.reshape(HEIGHT, WIDTH, 1))
            # if cv2.waitKey(25) & 0xFF == ord('q'):
            #     cv2.destroyAllWindows()

            prediction = model.predict([minimap.reshape(HEIGHT, WIDTH, 1)])[0]
            prediction = np.array(
                prediction)
            mode_choice = np.argmax(prediction)
            if mode_choice == 0:
                straight()
                choice_picked = 'straight'

            elif mode_choice == 1:
                reverse()
                choice_picked = 'reverse'

            elif mode_choice == 2:
                left()
                choice_picked = 'left'
            elif mode_choice == 3:
                right()
                choice_picked = 'right'
            elif mode_choice == 4:
                forward_left()
                choice_picked = 'forward+left'
            elif mode_choice == 5:
                forward_right()
                choice_picked = 'forward+right'
            elif mode_choice == 6:
                reverse_left()
                choice_picked = 'reverse+left'
            elif mode_choice == 7:
                reverse_right()
                choice_picked = 'reverse+right'
            elif mode_choice == 8:
                no_keys()
                choice_picked = 'nokeys'

            print('choice: {}'.format(choice_picked))

            if len(last_frames) > 100:
                # remove the first frame from the list
                last_frames.pop(0)

                # calculate the mean squared error between all the frames
                mean_squared_error = np.mean(
                    [np.sum((minimap - frame) ** 2) for frame in last_frames])

                # set a threshold for the mean squared error
                threshold = 10 ** 6

                if mean_squared_error < threshold:
                    # the frames are too similar, do something (e.g. break the loop)
                    print('stuck')
                    last_frames = []
                    no_keys()
                    time.sleep(0.5)
                    # move randomly
                    random_move = random.randrange(0, 4)

                    if random_move == 0:
                        straight()
                        print('move random straight')
                    elif random_move == 1:
                        left()
                        print('move random left')
                    elif random_move == 2:
                        right()
                        print('move random right')
                    elif random_move == 3:
                        reverse()
                        print('move random reverse')

            # if motion_avg < motion_req and len(motion_log) >= log_len:
            #     print('WERE PROBABLY STUCK FFS, initiating some evasive maneuvers.')

            #     # 0 = reverse straight, turn left out
            #     # 1 = reverse straight, turn right out
            #     # 2 = reverse left, turn right out
            #     # 3 = reverse right, turn left out

            #     quick_choice = random.randrange(0, 4)

            #     if quick_choice == 0:
            #         reverse()
            #         time.sleep(random.uniform(1, 2))
            #         forward_left()
            #         time.sleep(random.uniform(1, 2))

            #     elif quick_choice == 1:
            #         reverse()
            #         time.sleep(random.uniform(1, 2))
            #         forward_right()
            #         time.sleep(random.uniform(1, 2))

            #     elif quick_choice == 2:
            #         reverse_left()
            #         time.sleep(random.uniform(1, 2))
            #         forward_right()
            #         time.sleep(random.uniform(1, 2))

            #     elif quick_choice == 3:
            #         reverse_right()
            #         time.sleep(random.uniform(1, 2))
            #         forward_left()
            #         time.sleep(random.uniform(1, 2))

            #     for i in range(log_len-2):
            #         del motion_log[0]

        keys = key_check()

        # p pauses game and can get annoying.
        if 'T' in keys:
            if paused:
                paused = False
                time.sleep(1)
            else:
                paused = True
                ReleaseKey(A)
                ReleaseKey(W)
                ReleaseKey(D)
                time.sleep(1)


main()
