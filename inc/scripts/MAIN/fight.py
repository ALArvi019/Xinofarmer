from preprocess import PreProcessImage
import cv2 as cv
import threading
import time
import numpy as np
import gc
from readINI import ReadINIFile


class Fight(threading.Thread):
    def __init__(self, threads, skills_means, ranged, moveplayer, send_text_to_bot, from_python, solo_mode, image_path):
        threading.Thread.__init__(self)
        self.captureWorker = threads.get_thread('CaptureWorker')
        self.preprocess = PreProcessImage()
        self.moveplayer = moveplayer
        self.is_running = False
        self.stopped = False
        self.skills_means = skills_means
        self.ranged = ranged
        self.paused = False
        self.send_text_to_bot = send_text_to_bot
        self.from_python = from_python
        self.memory_clean = False
        self.survivor_mode = False
        self.key_press_thread = None
        self.key_press_thread_survivor = None
        self.force_fight = False
        self.solo_mode = solo_mode
        self.image_path = image_path
        self.color_mode = ReadINIFile(image_path + '\\..\\..\\setup.ini', 'Main', 'AttackMethod', 'Precise')


    def pause(self):
        self.paused = True

    def resume(self):
        self.paused = False

    def checkFightIsRunning(self, time_to_wait=5, show_message=True):
        if self.is_running:
            if show_message:
                self.send_text_to_bot.send(
                    'Fight is running, waiting...', self.from_python)
            # Wait for fight to finish
            while self.is_running:
                time.sleep(time_to_wait)
            return True
        else:
            if show_message:
                self.send_text_to_bot.send(
                    'Fight finished, continuing...', self.from_python)
            return False

    def set_survivor_mode(self, survivor_mode):
        self.send_text_to_bot.send(
            'Survivor mode: ' + str(survivor_mode), self.from_python, 'pink')
        self.survivor_mode = survivor_mode

    def press_keys_in_order(self):
        keys_to_press = ['l', 'n', 'k']
        while not self.stop_key_thread:
            for key in keys_to_press:
                self.moveplayer.pressCustomKey(key)
            time.sleep(0.4)

    def press_keys_in_order_survivor(self):
        keys_to_press = ['1', '2', '3', '4']
        while not self.stop_key_thread:
            for key in keys_to_press:
                self.moveplayer.pressCustomKey(key)
            time.sleep(0.4)

    def run(self):
        # (hMin = 0 , sMin = 255, vMin = 178), (hMax = 0 , sMax = 255, vMax = 178)
        if self.color_mode == 'Precise':
            lower_1 = 0
            lower_2 = 255
            lower_3 = 178
            upper_1 = 0
            upper_2 = 255
            upper_3 = 178
        else:
            # 0, 255, 78
            lower_1 = 0
            lower_2 = 255
            lower_3 = 0
            upper_1 = 0
            upper_2 = 255
            upper_3 = 255

        number_of_fights = 0

        while self.stopped is False:
            # Capture screenshot
            if self.paused is True:
                self.pauseSubThreads()
                if self.memory_clean is True:
                    gc.collect()
                    self.memory_clean = False
                time.sleep(1)
                continue
            try:
                self.memory_clean = True
                screenshot = self.captureWorker.screenshot
                screenshot = self.captureWorker.apply_mask(screenshot)

                # Convertir a HSV
                screenshot_hsv = cv.cvtColor(screenshot, cv.COLOR_BGR2HSV)

                # Definir los colores a buscar
                # BGR----------------------
                
                continue_fighting = False

                # Buscar los colores
                lower = np.array(
                    [lower_1, lower_2, lower_3])
                upper = np.array(
                    [upper_1, upper_2, upper_3])

                mask = cv.inRange(screenshot_hsv, lower, upper)
                count = cv.countNonZero(mask)

                if self.paused is True:
                    self.pauseSubThreads()
                    continue

                if count > 100 or self.force_fight:
                    self.resumeSubThreads()

                    # get the position of the monster
                    contours, hierarchy = cv.findContours(
                        mask, cv.RETR_TREE, cv.CHAIN_APPROX_SIMPLE)
                    for cnt in contours:
                        x, y, w, h = cv.boundingRect(cnt)
                        break

                    self.is_running = True
                    if self.survivor_mode:
                        self.moveplayer.fight(
                            self.skills_means, x + int(w/2), y + int(h/2), self.ranged, True, self.solo_mode)
                    else:
                        self.moveplayer.fight(
                            self.skills_means, x + int(w/2), y + int(h/2), self.ranged)
                    number_of_fights = number_of_fights + 1
                    if number_of_fights >= 50:
                        print('Stuck in fight')
                        time.sleep(10)
                        number_of_fights = 0
                        continue_fighting = False
                    else:
                        continue_fighting = True

                if self.paused is True:
                    self.pauseSubThreads()
                    continue

                if continue_fighting:
                    self.is_running = True
                    number_of_fights = 0
                else:
                    # Si no se encuentra el color, esperar 1 segundo y continuar
                    self.pauseSubThreads()
                    time.sleep(0.5)
            except Exception as e:
                print('Fight->' + str(e))
                print('Warn getting screenshot Fight')
                time.sleep(0.5)
                continue

    def pauseSubThreads(self):
        if self.key_press_thread is not None and self.key_press_thread.is_alive():
            self.is_running = False
            self.stop_key_thread = True
            self.key_press_thread.join()
            self.key_press_thread = None
        if self.key_press_thread_survivor is not None and self.key_press_thread_survivor.is_alive():
            self.is_running = False
            self.stop_key_thread = True
            self.key_press_thread_survivor.join()
            self.key_press_thread_survivor = None

    def resumeSubThreads(self):
        # print in red
        if self.key_press_thread is None or not self.key_press_thread.is_alive():
            self.is_running = True
            self.stop_key_thread = False
            self.key_press_thread = threading.Thread(
                target=self.press_keys_in_order)
            self.key_press_thread.start()

        if self.survivor_mode:
            if self.key_press_thread_survivor is None or not self.key_press_thread_survivor.is_alive():
                self.is_running = True
                self.stop_key_thread = False
                self.key_press_thread_survivor = threading.Thread(
                    target=self.press_keys_in_order_survivor)
                self.key_press_thread_survivor.start()

    def stop(self):
        self.stopped = True
