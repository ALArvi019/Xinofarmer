
import threading
import cv2 as cv
import time
from preprocess import PreProcessImage
from findImage import RunFindImage
import numpy as np
from getkeys import key_check
import base64
import gc

class CheckMessages(threading.Thread):
    def __init__(self, threads, src_window, telegramConfig, username, send_text_to_bot, from_python, img_path, Moveplayer, language):
        threading.Thread.__init__(self)
        self.captureWorker = threads.get_thread('CaptureWorker')
        self.preprocess = PreProcessImage()
        self.stopped = False
        self.is_running = True
        self.paused = False
        self.telegramConfig = telegramConfig
        self.username = username
        self.socketIO = threads.get_thread('CustomSocketIO')
        self.send_text_to_bot = send_text_to_bot
        self.from_python = from_python
        self.img_path = img_path
        self.src_window = src_window
        self.moveplayer = Moveplayer
        self.threads = threads
        self.language = language
        self.memory_clean = False

    def pause(self):
        self.paused = True

    def resume(self):
        self.paused = False

    def stop(self):
        self.stopped = True

    def run(self):
        # 135 108 144 upper 197 128 242
        lower_PURPLE_1 = 135  
        lower_PURPLE_2 = 108
        lower_PURPLE_3 = 144
        upper_PURPLE_1 = 197
        upper_PURPLE_2 = 128
        upper_PURPLE_3 = 242

        last_image = None
        while self.stopped is False:
            if self.paused is True:
                if self.memory_clean is True:
                    gc.collect()
                    self.memory_clean = False
                time.sleep(1)
                continue
            # Capture screenshot
            try:
                self.memory_clean = True
                send_to_socketio = False
                if self.captureWorker.screenshot is None:
                    time.sleep(1)
                    continue
                screenshot1 = self.captureWorker.screenshot
                screenshot = self.preprocess.crop(screenshot1, 327, 536, 300, 15)
                # LOAD image.png
                # screenshot = cv.imread('image.png')

                # SAVE IMAGE  AS IMAGE.PNG
                # cv.imwrite('image.png', screenshot)
                hsv = cv.cvtColor(screenshot, cv.COLOR_BGR2HSV)
                lower_PURPLE = np.array([lower_PURPLE_1, lower_PURPLE_2, lower_PURPLE_3])
                upper_PURPLE = np.array([upper_PURPLE_1, upper_PURPLE_2, upper_PURPLE_3])

                mask_PURPLE = cv.inRange(hsv, lower_PURPLE, upper_PURPLE)

                # detected_output = cv.bitwise_and(screenshot, screenshot, mask =  mask_PURPLE)

                # get the purple pixels number
                purple_pixels = np.count_nonzero(mask_PURPLE)
                if purple_pixels > 80:
                    # print('purple detected ' + str(time.time()) + ' -- ' + str(purple_pixels))
                    if last_image is None:
                        last_image = purple_pixels
                        send_to_socketio = True
                    else:
                        if abs(purple_pixels - last_image) > 50:
                            last_image = np.count_nonzero(mask_PURPLE)
                            send_to_socketio = True

                    # print('send_to_socketio', send_to_socketio)
                    # print('self.telegramConfig', self.telegramConfig)
                    # print('self.socketIO.checkIfConnected()', self.socketIO.checkIfConnected())
                    
                    if send_to_socketio and self.telegramConfig and self.socketIO.checkIfConnected():
                        # send to telegram
                        self.send_text_to_bot.send('send to telegram ' + str(time.time()) + ' -- ' + str(purple_pixels), self.from_python)
                        # cv.imshow('TELEGRAM', screenshot)
                        # cv.imshow('screenshot', screenshot)
                        # cv.imshow('detected_output', detected_output)
                        # cv.waitKey(1)
                        send_to_socketio = False

                        self.send_text_to_bot.send('send to telegram screenshot', self.from_python)

                        _, compressed_image = cv.imencode('.jpg', screenshot1)
                        base64_image = base64.b64encode(compressed_image).decode('utf-8')

                        self.socketIO.send('send_telegram_message', {'image': base64_image, 'username': self.username})
                        
                        # for i in list(range(10))[::-1]:
                        #     print(i+1)
                        #     time.sleep(1)
                else:
                    response = RunFindImage(
                            self.src_window, self.img_path + '\\game_items', 'new_message_chat_' + self.language, screenshot1)
                    if response['new_message_chat_' + self.language] != 'notfound':
                        self.threads.pause_all_threads(['CheckMessages', 'CaptureWorker'])
                        # wait until all threads are paused
                        while self.threads.check_if_all_threads_paused(['CheckMessages', 'CaptureWorker']) is False:
                            self.send_text_to_bot.send('waiting for checking message', self.from_python, 'blue')
                            self.threads.pause_all_threads(['CheckMessages', 'CaptureWorker'])
                            time.sleep(1)
                        self.moveplayer.processing_movement_output('NK')
                        PositionOFBS_x = int(response['new_message_chat_' + self.language].split('|')[0]) + 50
                        PositionOFBS_y = response['new_message_chat_' + self.language].split('|')[1]
                        self.moveplayer.clickOnCoords(
                            (int(PositionOFBS_x), int(PositionOFBS_y)))
                        self.moveplayer.processing_movement_output('NK')
                        time.sleep(3)
                        self.moveplayer.processing_movement_output('NK')
                        exitToChat = False
                        count = 0
                        while exitToChat is False and count < 5:
                            self.moveplayer.processing_movement_output('NK')
                            response = RunFindImage(
                                self.src_window, self.img_path + '\\game_items', 'close', self.captureWorker.screenshot)
                            if response['close'] != 'notfound':
                                PositionOFBS_x = int(response['close'].split('|')[0])
                                PositionOFBS_y = response['close'].split('|')[1]
                                self.moveplayer.clickOnCoords(
                                    (int(PositionOFBS_x), int(PositionOFBS_y)))
                                exitToChat = True
                            else:
                                response = RunFindImage(
                                    self.src_window, self.img_path + '\\game_items', 'news', self.captureWorker.screenshot)
                                if response['news'] != 'notfound':
                                    self.moveplayer.pressKey('esc')
                                    exitToChat = True
                            count += 1
                            time.sleep(1)
                        last_image = None
                        self.threads.resume_all_threads()

                # cv.imshow('screenshot1', screenshot1)
                # cv.imshow('TELEGRAM', screenshot)
                # cv.waitKey(1)
                

                if 1 == 2:
                    keys = key_check()
                    if 'A' in keys:
                        lower_PURPLE_1 += 1
                        print('lower', lower_PURPLE_1, lower_PURPLE_2, lower_PURPLE_3, 'upper', upper_PURPLE_1, upper_PURPLE_2, upper_PURPLE_3)
                    elif 'Z' in keys:
                        lower_PURPLE_1 -= 1
                        print('lower', lower_PURPLE_1, lower_PURPLE_2, lower_PURPLE_3, 'upper', upper_PURPLE_1, upper_PURPLE_2, upper_PURPLE_3)
                    elif 'S' in keys:
                        lower_PURPLE_2 += 1
                        print('lower', lower_PURPLE_1, lower_PURPLE_2, lower_PURPLE_3, 'upper', upper_PURPLE_1, upper_PURPLE_2, upper_PURPLE_3)
                    elif 'X' in keys:
                        lower_PURPLE_2 -= 1
                        print('lower', lower_PURPLE_1, lower_PURPLE_2, lower_PURPLE_3, 'upper', upper_PURPLE_1, upper_PURPLE_2, upper_PURPLE_3)
                    elif 'D' in keys:
                        lower_PURPLE_3 += 1
                        print('lower', lower_PURPLE_1, lower_PURPLE_2, lower_PURPLE_3, 'upper', upper_PURPLE_1, upper_PURPLE_2, upper_PURPLE_3)
                    elif 'C' in keys:
                        lower_PURPLE_3 -= 1
                        print('lower', lower_PURPLE_1, lower_PURPLE_2, lower_PURPLE_3, 'upper', upper_PURPLE_1, upper_PURPLE_2, upper_PURPLE_3)
                    elif 'F' in keys:
                        upper_PURPLE_1 += 1
                        print('lower', lower_PURPLE_1, lower_PURPLE_2, lower_PURPLE_3, 'upper', upper_PURPLE_1, upper_PURPLE_2, upper_PURPLE_3)
                    elif 'V' in keys:
                        upper_PURPLE_1 -= 1
                        print('lower', lower_PURPLE_1, lower_PURPLE_2, lower_PURPLE_3, 'upper', upper_PURPLE_1, upper_PURPLE_2, upper_PURPLE_3)
                    elif 'G' in keys:
                        upper_PURPLE_2 += 1
                        print('lower', lower_PURPLE_1, lower_PURPLE_2, lower_PURPLE_3, 'upper', upper_PURPLE_1, upper_PURPLE_2, upper_PURPLE_3)
                    elif 'B' in keys:
                        upper_PURPLE_2 -= 1
                        print('lower', lower_PURPLE_1, lower_PURPLE_2, lower_PURPLE_3, 'upper', upper_PURPLE_1, upper_PURPLE_2, upper_PURPLE_3)
                    elif 'H' in keys:
                        upper_PURPLE_3 += 1
                        print('lower', lower_PURPLE_1, lower_PURPLE_2, lower_PURPLE_3, 'upper', upper_PURPLE_1, upper_PURPLE_2, upper_PURPLE_3)
                    elif 'N' in keys:
                        upper_PURPLE_3 -= 1
                        print('lower', lower_PURPLE_1, lower_PURPLE_2, lower_PURPLE_3, 'upper', upper_PURPLE_1, upper_PURPLE_2, upper_PURPLE_3)

            except Exception as e:
                print(e)
                continue
            time.sleep(1)