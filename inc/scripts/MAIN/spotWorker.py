import threading
import time
import cv2 as cv
from preprocess import PreProcessImage
from tensorflow import keras
import keras.backend as K
import os
import numpy as np
from collections import deque
import gc
from readINI import ReadINIFile

class SpotWorker(threading.Thread):
    def __init__(self, threads, src_window, img_path, fileName, inc_path, send_text_to_bot, from_python, rectangle, moveplayer, stuck_average, modelname):
        threading.Thread.__init__(self)
        self.img_path = img_path
        self.src_window = src_window
        self.moveplayer = moveplayer
        self.is_running = False
        self.stopped = False
        self.paused = False
        self.captureWorker = threads.get_thread('CaptureWorker')
        self.checkisdead = threads.get_thread('CheckIsDead')
        self.fight = threads.get_thread('Fight')
        self.threads = threads
        self.preprocess = PreProcessImage()
        self.fileName = fileName
        self.class_names = ['↑', '↓', '←', '→', '↖', '↗', '↙', '↘', 'NK']
        self.model = None
        self.screens = deque(maxlen=2)
        self.movements = deque(maxlen=10)
        self.move_average_count = 0
        self.inc_path = inc_path
        self.send_text_to_bot = send_text_to_bot
        self.from_python = from_python
        self.player_stuck_count = 0
        self.player_stuck_count_time = None
        self.rectangle = rectangle
        self.memory_clean = False
        self.stuck_average = stuck_average
        self.action_after_detect_monster = ReadINIFile(inc_path + '\\..\\setup.ini', 'SpotFarm', 'StopIfDetectMonster', 'Yes')
        if modelname != 'default':
            self.fileName = modelname

        # check if model exists
        # nameFile = 'marv1'
        # FILE_NAME = nameFile + "_clean"
        # EPOCHS = 30
        # MODEL_N = 'modelv1'
        # MODEL_NAME = FILE_NAME + '-{}-{}-epochs.h5'.format(MODEL_N, EPOCHS)
        # model_files = glob.glob("./models/*__model-*")
        # if len(model_files) > 0:
        #     MODEL_NAME = max(model_files, key=os.path.getctime)
        #     print ("Model name: " + MODEL_NAME)
        # else:
        #     MODEL_NAME = './models/marv1_clean-modelv1-1000-epochs.h5__model-2577-0.9516'


    def pause(self):
        self.paused = True

    def resume(self):
        self.paused = False

    def run(self):
        # print in purple
        print('\033[95m' + self.fileName + ' started' + '\033[0m')
        if self.fileName == 'kikuras' or self.fileName == 'ancients' or self.fileName == 'storm':
            self.fileName = 'common_model1'
        MODEL_NAME = self.inc_path + '\\data\\models\\' + self.fileName + '.dat'
        # MODEL_NAME = './models/modelv61__model-modelv61-100-epochs_storm_3.h5'
        if os.path.isfile(MODEL_NAME):
            print('Model exists, loading previous model {}'.format(MODEL_NAME))
            model = keras.models.load_model(MODEL_NAME, compile=False)
            model.compile(optimizer='adam',
                          loss='categorical_crossentropy', metrics=['accuracy'])
            print('Model loaded!')
            self.model = model
        # check if model is loaded
        if self.model is None:
            print("Model is not loaded !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
            self.send_text_to_bot.send('Model is not loaded !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!', self.from_python, 'red')
            return

        while not self.stopped:
            # continue
            if self.paused:
                if self.memory_clean is True:
                    gc.collect()
                    self.memory_clean = False
                time.sleep(0.5)
                continue

            try:
                self.memory_clean = True
                if self.checkisdead.player_is_dead:
                    continue

                screen = self.captureWorker.screenshot
                minimap1 = self.preprocess.crop(screen, 740, 40, 173, 110)
                cv.circle(minimap1, (86, 56), 14, (0, 0, 0), -1)
                cv.rectangle(minimap1, self.rectangle, (minimap1.shape[1], minimap1.shape[0]), (0, 0, 0), -1)
                minimap = self.preprocess.to_grayscale(minimap1)
                # RESIZE___________________________________________
                minimap = cv.resize(minimap, (minimap.shape[1], minimap.shape[0]), interpolation=cv.INTER_AREA)
                minimap = np.expand_dims(minimap, axis=2)
                # cv.imshow("minimap", minimap)
                # cv.waitKey(10)
                # RESIZE___________________________________________
                training_data = []
                training_data.append([minimap, [0, 0, 0, 0, 0, 0, 0, 0, 0]])
                training_data = np.array(training_data, dtype=object)
                x = training_data[:, 0]
                x = np.array([i for i in x]).reshape(-1, 110, 173, 1)
                x = x / 255.0

                # shit before prediction----------------------
                prediction = self.model.predict(x[0].reshape(-1, 110, 173, 1), verbose=0)
                max_value_index = np.argmax(prediction)

                # add screen if the division of the actual seconds by 5 is 0
                if time.localtime().tm_sec % 5 == 0:
                    self.screens.append(minimap1)

                if len(self.screens) == 2:
                    diff = cv.absdiff(self.screens[1], self.screens[0])
                    gray = cv.cvtColor(diff, cv.COLOR_BGR2GRAY)
                    blurred = cv.GaussianBlur(gray, (5, 5), 0)
                    _, thresh = cv.threshold(blurred, 50, 255, cv.THRESH_BINARY)
                    movement_count = len(np.argwhere(thresh == 255))
                    self.movements.append(movement_count)

                    movement_avg = np.mean(self.movements)

                    if float(movement_avg) < 0.1:
                        self.move_average_count += 1
                        # if self.move_average_count > 40:
                        if self.move_average_count > self.stuck_average:
                            self.move_average_count = 0
                            self.moveplayer.processing_movement_output('NK')
                            self.moveplayer.MoveRandomly(1, 1)
                            self.player_stuck_count += 1
                            
                            self.send_text_to_bot.send('PLAYER STUCK (' + str(self.player_stuck_count) + '/200)', self.from_python, 'orange')
                            
                            if self.player_stuck_count >= 200:
                                self.send_text_to_bot.send('PLAYER STUCK FOR 200 TIMES. restart', self.from_python, 'red')
                                self.player_stuck_count = 0
                                self.paused = True
                                self.threads.runAgain()
                                continue

                    else:
                        self.move_average_count = 0

                if self.paused:
                    continue

                if self.action_after_detect_monster == 'Yes' and self.fight.is_running is True:
                    self.moveplayer.processing_movement_output('NK')
                    continue
                
                self.moveplayer.processing_movement_output(self.class_names[max_value_index])
                
                if self.paused:
                    self.moveplayer.processing_movement_output('NK')
                # time.sleep(0.2)
                del minimap1
                del minimap
                del training_data
                del x
                gc.collect()

            except Exception as e:
                print('Error processing SpotWorker:', e)
                time.sleep(0.5)
                continue

    def stop(self):
        self.moveplayer.processing_movement_output('NK')
        self.stopped = True
        self.stop_threads()
        K.clear_session()

    def stop_threads(self):
        cv.destroyAllWindows()
        keras.backend.clear_session()
        self.screens.clear()
        self.movements.clear()
