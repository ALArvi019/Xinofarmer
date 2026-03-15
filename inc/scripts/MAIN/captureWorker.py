import threading
import time
from windowcapture import WindowCapture
import cv2 as cv
import numpy as np
import gc


class CaptureWorker(threading.Thread):
    def __init__(self, src_window, img_path):
        threading.Thread.__init__(self)
        self.wincap = WindowCapture(src_window)
        self.stopped = False
        self.screenshot = None
        self.paused = False
        self.img_path = img_path
        self.memory_clean = False

    def pause(self):
        self.paused = True

    def resume(self):
        self.paused = False

    def stop(self):
        self.stopped = True

    def run(self):
        while self.stopped is False:
            if self.paused is True:
                if self.memory_clean is True:
                    gc.collect()
                    self.memory_clean = False
                time.sleep(0.5)
                continue
            # Capture screenshot
            try:
                self.memory_clean = True
                self.screenshot = self.wincap.get_screenshot()
            except Exception as e:
                # print('Warn getting screenshot CaptureWorker')
                continue
            # time.sleep(0.2)

    def apply_mask(self, screenshot):
        mask = cv.imread(
            self.img_path + '\game_items\game_mask.png', cv.IMREAD_UNCHANGED)

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
        