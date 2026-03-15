import numpy as np
import cv2
import time
import os
import pandas as pd
from tqdm import tqdm
from collections import deque
from models import otherception3 as googlenet
from random import shuffle


WIDTH = 173
HEIGHT = 110
LR = 1e-3
EPOCHS = 30


fileName = "zavainGPU"

MODEL_NAME = fileName + \
    '-{}-{}-{}-epochs.model'.format(LR, 'otherception3', EPOCHS)
PREV_MODEL = fileName + \
    '-{}-{}-{}-epochs.model'.format(LR, 'otherception3', EPOCHS)

wl = 0
sl = 0
al = 0
dl = 0

wal = 0
wdl = 0
sal = 0
sdl = 0
nkl = 0

w = [1, 0, 0, 0, 0, 0, 0, 0, 0]
s = [0, 1, 0, 0, 0, 0, 0, 0, 0]
a = [0, 0, 1, 0, 0, 0, 0, 0, 0]
d = [0, 0, 0, 1, 0, 0, 0, 0, 0]
wa = [0, 0, 0, 0, 1, 0, 0, 0, 0]
wd = [0, 0, 0, 0, 0, 1, 0, 0, 0]
sa = [0, 0, 0, 0, 0, 0, 1, 0, 0]
sd = [0, 0, 0, 0, 0, 0, 0, 1, 0]
nk = [0, 0, 0, 0, 0, 0, 0, 0, 1]

model = googlenet(WIDTH, HEIGHT, 3, LR, output=9, model_name=MODEL_NAME)

# check if model exists
if os.path.isfile('./' + MODEL_NAME + '.meta'):
	print('Model exists, loading previous model {}'.format(MODEL_NAME))
	model.load(MODEL_NAME)
	print('Model loaded!')

# get number of training data files in './data/' + fileName + '/'
FILE_I_END = 0
while True:
    try:
        file_name = './data/' + fileName + '/' + \
            fileName + '-{}.npy'.format(FILE_I_END+1)
        train_data = np.load(file_name, allow_pickle=True)
        FILE_I_END += 1
    except:
        break


# iterates through the training files


for e in range(EPOCHS):
    # data_order = [i for i in range(1,FILE_I_END+1)]
    data_order = [i for i in range(1, FILE_I_END+1)]
    shuffle(data_order)
    for count, i in enumerate(data_order):

        try:
            file_name = './data/' + fileName + '/' + \
                fileName + '-{}.npy'.format(i)

            next_file_name = './data/' + fileName + '/' + \
                fileName + '-{}.npy'.format(i+1)
            # full file info
            train_data = np.load(file_name, allow_pickle=True)
            # check if next_file_name exists
            if os.path.isfile(next_file_name):
                test_data = np.load(next_file_name, allow_pickle=True)
                print('testing_data-{}.npy'.format(i+1), len(test_data))
            else:
                test_data = train_data
            print('training_data-{}.npy'.format(i), len(train_data))
            

# [   [    [FRAMES], CHOICE   ]    ]
# train_data = []
# current_frames = deque(maxlen=HM_FRAMES)
##
# for ds in data:
# screen, choice = ds
# gray_screen = cv2.cvtColor(screen, cv2.COLOR_RGB2GRAY)
##
##
# current_frames.append(gray_screen)
# if len(current_frames) == HM_FRAMES:
# train_data.append([list(current_frames),choice])

            # #
            # always validating unique data:
            shuffle(train_data)
            train = train_data[:-50]
            test = test_data[-50:]

            X = np.array([i[0] for i in train]).reshape(-1, WIDTH, HEIGHT, 1)
            Y = [i[1] for i in train]

            test_x = np.array([i[0]
                              for i in test]).reshape(-1, WIDTH, HEIGHT, 1)
            test_y = [i[1] for i in test]

            model.fit({'input': X}, {'targets': Y}, n_epoch=10, validation_set=({'input': test_x}, {'targets': test_y}),
                      snapshot_step=500, show_metric=True, run_id=MODEL_NAME, batch_size=100)

            if count % 10 == 0:
                print('SAVING MODEL!')
                model.save(MODEL_NAME)

        except Exception as e:
            print(str(e))


#

# C:\Users\Alex\AppData\Local\Packages\PythonSoftwareFoundation.Python.3.10_qbz5n2kfra8p0\LocalCache\local-packages\Python310\Scripts\tensorboard.exe --logdir path\to\immortal_xinofarmer\inc\scripts\trainv2\log
