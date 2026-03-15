from preprocess import PreProcessImage
import cv2 as cv
import threading
import time
import numpy as np
import gc
from readINI import ReadINIFile

class CheckLife(threading.Thread):
    def __init__(self, threads, moveplayer, send_text_to_bot, from_python, img_path):
        threading.Thread.__init__(self)
        self.moveplayer = moveplayer
        self.preprocess = PreProcessImage()
        self.stopped = False
        self.is_running = True
        self.paused = False
        self.send_text_to_bot = send_text_to_bot
        self.from_python = from_python
        self.captureWorker = threads.get_thread('CaptureWorker')
        self.memory_clean = False
        self.life_percent = ReadINIFile(img_path + '\\..\\..\\setup.ini', 'Main', 'HealthPlayerAt', '60')

    def pause(self):
        self.paused = True

    def resume(self):
        self.paused = False

    def run(self):
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
                screenshot = self.captureWorker.screenshot
                screenshot = self.preprocess.crop(screenshot, 10, 103, 92, 12)

                # ---------------------------------------
                hsv = cv.cvtColor(screenshot, cv.COLOR_BGR2HSV)

                # Definir el rango de colores rojos que deseas detectar en HSV
                lower_red = np.array([0, 75, 75])
                upper_red = np.array([255, 255, 255])

                # Umbralizar la imagen para obtener solo los píxeles rojos
                mask_red = cv.inRange(hsv, lower_red, upper_red)

                # detected_output = cv.bitwise_and(screenshot, screenshot, mask =  mask_red) 
                # self.preprocess.image_show('detected_output', detected_output, True)

                # Calcular el número de píxeles negros
                num_black_pixels = cv.countNonZero((mask_red == 0).astype(np.uint8) if np.any(mask_red) else mask_red)

                # Calcular el porcentaje de píxeles negros respecto al espacio total
                total_pixels = mask_red.shape[0] * mask_red.shape[1]
                black_ratio = num_black_pixels / total_pixels
                life_percent = 100 - int(black_ratio * 100)

                # print(f"Porcentaje de vida: {life_percent}%")
                # ---------------------------------------


                # self.preprocess.image_show('threshold_red',threshold_red,True)
                # cv.imshow("screenshot", screenshot)
                # cv.imshow("gray", gray)
                # cv.imshow("blur", blur)
                # if cv.waitKey(1) == ord('q'):
                #     cv.destroyAllWindows()
                #     break

                if life_percent <= int(self.life_percent):
                    self.send_text_to_bot.send('Health Player', self.from_python, 'green')
                    self.moveplayer.pressKey('q')
                    # time.sleep(3)
            except  Exception as e:
                # print('Warn getting CheckLife')
                continue
            time.sleep(0.3)

    def stop(self):
        self.stopped = True

