import threading
import time
import numpy as np
import cv2 as cv
import math
from preprocess import PreProcessImage
from findObjectInMinimap import FindObjectInMinimap
from findObjectInMinimap import findSpecificItemOnMinimap
from findImage import RunFindImage
from getkeys import key_check
from GeomUtil import GeomUtil


class EndlessModeChecDoorAttack(threading.Thread):
    def __init__(self, threads, src_window, send_text_to_bot, from_python, moveplayer, img_path):
        threading.Thread.__init__(self)
        self.stopped = False
        self.paused = False
        self.src_window = src_window
        self.send_text_to_bot = send_text_to_bot
        self.from_python = from_python
        self.threads = threads
        self.captureWorker = threads.get_thread('CaptureWorker')
        self.fight = threads.get_thread('Fight')
        self.playerPositionInScreen = (480, 331)
        self.moveplayer = moveplayer
        self.img_path = img_path
        self.lower_1 = 0
        self.lower_2 = 226
        self.lower_3 = 157
        self.upper_1 = 0
        self.upper_2 = 240
        self.upper_3 = 168
        self.threshold_line = 20
        self.minLineLength = 0
        self.maxLineGap = 0
        self.near_line = 0
        self.line_not_detected = 0
        self.preprocess = PreProcessImage()
        self.movements = ['→', '↘', '↓', '↙', '←', '↖', '↑', '↗']

    def pause(self):
        self.paused = True

    def stop(self):
        self.stopped = True

    def resume(self):
        self.paused = False

    def image_triangle(self, image):

        # Crear una máscara del mismo tamaño que la imagen, inicializada en blanco (255, 255, 255)
        mask = np.ones_like(image) * 255

        # Definir las coordenadas de las esquinas
        corner1 = (0, image.shape[0] - 1)  # Esquina inferior izquierda
        corner2 = (0, -25)  # Esquina superior izquierda
        # Esquina inferior derecha
        corner3 = (image.shape[1] - 1 + 30, image.shape[0] - 1)

        # Definir los puntos para el triángulo
        triangle_points = np.array([corner1, corner2, corner3], np.int32)

        # Configurar el triángulo en negro en la máscara
        cv.fillPoly(mask, [triangle_points], (0, 0, 0))

        # Aplicar la máscara a la imagen original
        result = cv.bitwise_and(image, mask)

        return result

    def run(self):
        print("DEBUG: EndlessModeCheckDoor started")
        while self.stopped is False:
            if self.paused is True:
                time.sleep(1)
                continue
            # if 1 == 1:
            try:
                screenshot = self.captureWorker.screenshot
                screenshot = self.preprocess.crop(
                    screenshot, 740, 40, 173, 110)
                # save image to file
                # cv.imwrite('screenshot.png', screenshot)
                # read file from disk
                # screenshot =  cv.imread('screenshot.png')
                screenshot_hsv = cv.cvtColor(screenshot, cv.COLOR_BGR2HSV)
                lower = np.array([self.lower_1, self.lower_2, self.lower_3])
                upper = np.array([self.upper_1, self.upper_2, self.upper_3])

                mask = cv.inRange(screenshot_hsv, lower, upper)

                count = cv.countNonZero(mask)

                if count > 30:
                    self.threads.pause_thread('EndlessModeCheckLine')
                    self.threads.pause_thread('CheckLoot')
                    self.moveplayer.processing_movement_output('NK')
                    self.send_text_to_bot.send(
                        "Hold the door! XD", self.from_python)

                    actualtime = time.time()
                    # execute while lopp max 30 seconds
                    door_big = RunFindImage(self.src_window, self.img_path + '\\game_items',
                                            'minimap_cyrangar_door_big', self.captureWorker.screenshot, 0.8, False, True)
                    while time.time() - actualtime < 10 and door_big['minimap_cyrangar_door_big'] == 'notfound':
                        # print('DEBUG: Try to find door' + str(time.time() - actualtime))
                        screenshot = self.captureWorker.screenshot
                        movement, distance = findSpecificItemOnMinimap(
                            screenshot, "cyrangar_door", 1, True)
                        if movement is not None:
                            self.moveplayer.processing_movement_output(
                                movement)
                            time.sleep(2)
                            self.moveplayer.processing_movement_output('NK')
                            door_big = RunFindImage(self.src_window, self.img_path + '\\game_items',
                                                    'minimap_cyrangar_door_big', self.captureWorker.screenshot, 0.8, False, True)
                        if self.paused:
                            break
                        time.sleep(0.5)
                    if self.paused:
                        break
                    if movement is not None:
                        self.send_text_to_bot.send(
                            'Door found, continue', self.from_python)
                        self.moveplayer.processing_movement_output('NK')
                        self.moveplayer.processing_movement_output(movement)
                        time.sleep(2)
                        self.moveplayer.processing_movement_output('NK')
                        self.threads.resume_thread('EndlessModeCheckLine')
                        self.threads.resume_thread('CheckLoot')

            except Exception as e:
                print(e)
                print("Error running EndlessModeCheckDoor")
            time.sleep(1)
