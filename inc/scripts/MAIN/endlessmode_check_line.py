import threading
import time
import numpy as np
import cv2 as cv
from getkeys import key_check


class EndlessModeCheckLine(threading.Thread):
    def __init__(self, threads, src_window, send_text_to_bot, from_python, moveplayer, img_path):
        threading.Thread.__init__(self)
        self.stopped = False
        self.paused = False
        self.src_window = src_window
        self.send_text_to_bot = send_text_to_bot
        self.from_python = from_python
        self.threads = threads
        self.captureWorker = threads.get_thread('CaptureWorker')
        self.playerPositionInScreen = (480, 331)
        self.moveplayer = moveplayer
        self.lower_1 = 6
        self.lower_2 = 152
        self.lower_3 = 236
        self.upper_1 = 8
        self.upper_2 = 178
        self.upper_3 = 248
        self.threshold_line = 20
        self.minLineLength = 0
        self.maxLineGap = 0
        self.near_line = 0
        self.line_not_detected = 0

    def pause(self):
        self.paused = True

    def stop(self):
        self.stopped = True

    def resume(self):
        self.paused = False

    def run(self):
        print("DEBUG: EndlessModeCheckLine started")
        while self.stopped is False:
            if self.paused is True:
                time.sleep(1)
                continue
            # if 1 == 1:
            try:
                screenshot = self.captureWorker.screenshot
                # save image to file
                # cv.imwrite('screenshot.png', screenshot)
                # read file from disk
                # screenshot =  cv.imread('screenshot.png')
                screenshot_hsv = cv.cvtColor(screenshot, cv.COLOR_BGR2HSV)
                lower = np.array([self.lower_1, self.lower_2, self.lower_3])
                upper = np.array([self.upper_1, self.upper_2, self.upper_3])

                mask = cv.inRange(screenshot_hsv, lower, upper)

                # count = cv.countNonZero(mask)
                detected_output = cv.bitwise_and(
                    screenshot, screenshot, mask=mask)

                detected_output_gray = cv.cvtColor(
                    detected_output, cv.COLOR_BGR2GRAY)

                edges = cv.Canny(detected_output_gray,
                                 threshold1=50, threshold2=150, apertureSize=3)
                lines = cv.HoughLinesP(
                    edges, 1, np.pi / 180, self.threshold_line, self.minLineLength, self.maxLineGap)

                # detected_output2 = detected_output

                if lines is not None:
                    result_x1 = None
                    result_y1 = None
                    result_x2 = None
                    result_y2 = None
                    for line in lines:
                        x1, y1, x2, y2 = line[0]
                        if result_x1 is None or x1 < result_x1:
                            result_x1 = x1
                        if result_y1 is None or y1 < result_y1:
                            result_y1 = y1
                        if result_x2 is None or x2 > result_x2:
                            result_x2 = x2
                        if result_y2 is None or y2 > result_y2:
                            result_y2 = y2
                    cv.line(screenshot, (result_x1, result_y1),
                            (result_x2, result_y2), (0, 255, 0), 2)
                    cv.circle(screenshot, self.playerPositionInScreen,
                              5, (0, 0, 255), -1)

                    # get the distande between player and line
                    distance = abs((result_y2 - result_y1) * self.playerPositionInScreen[0] - (result_x2 - result_x1) * self.playerPositionInScreen[1] +
                                   result_x2 * result_y1 - result_y2 * result_x1) / np.sqrt((result_y2 - result_y1) ** 2 + (result_x2 - result_x1) ** 2)
                    if distance < 150:
                        # print("Player is near to line")
                        self.moveplayer.processing_movement_output('NK')
                        self.moveplayer.processing_movement_output('↗')
                        time.sleep(1)
                        self.moveplayer.processing_movement_output('NK')
                else:
                    if self.line_not_detected > 10:
                        self.line_not_detected = 0
                        # print("No line detected")
                        self.moveplayer.processing_movement_output('↙')
                    self.line_not_detected = self.line_not_detected + 1

                # cv.imshow('detected_output', detected_output)
                # cv.imshow('screenshot', screenshot)
                # cv.imshow('detected_output2', detected_output2)
                # cv.imshow('edges', edges)
                # cv.waitKey(1)

                # keys = key_check()
                # if 1 == 2:
                #     if 'A' in keys:
                #         lower_1 = lower_1 + 1
                #         print("lower: (" + str(lower_1) + ", " + str(lower_2) + ", " + str(lower_3) + ") upper: (" + str(upper_1) + ", " + str(upper_2) + ", " + str(upper_3) + ")")
                #     if 'S' in keys:
                #         lower_2 = lower_2 + 1
                #         print("lower: (" + str(lower_1) + ", " + str(lower_2) + ", " + str(lower_3) + ") upper: (" + str(upper_1) + ", " + str(upper_2) + ", " + str(upper_3) + ")")
                #     if 'D' in keys:
                #         lower_3 = lower_3 + 1
                #         print("lower: (" + str(lower_1) + ", " + str(lower_2) + ", " + str(lower_3) + ") upper: (" + str(upper_1) + ", " + str(upper_2) + ", " + str(upper_3) + ")")
                #     if 'F' in keys:
                #         upper_1 = upper_1 + 1
                #         print("lower: (" + str(lower_1) + ", " + str(lower_2) + ", " + str(lower_3) + ") upper: (" + str(upper_1) + ", " + str(upper_2) + ", " + str(upper_3) + ")")
                #     if 'G' in keys:
                #         upper_2 = upper_2 + 1
                #         print("lower: (" + str(lower_1) + ", " + str(lower_2) + ", " + str(lower_3) + ") upper: (" + str(upper_1) + ", " + str(upper_2) + ", " + str(upper_3) + ")")
                #     if 'H' in keys:
                #         upper_3 = upper_3 + 1
                #         print("lower: (" + str(lower_1) + ", " + str(lower_2) + ", " + str(lower_3) + ") upper: (" + str(upper_1) + ", " + str(upper_2) + ", " + str(upper_3) + ")")
                #     if 'Z' in keys:
                #         lower_1 = lower_1 - 1
                #         print("lower: (" + str(lower_1) + ", " + str(lower_2) + ", " + str(lower_3) + ") upper: (" + str(upper_1) + ", " + str(upper_2) + ", " + str(upper_3) + ")")
                #     if 'X' in keys:
                #         lower_2 = lower_2 - 1
                #         print("lower: (" + str(lower_1) + ", " + str(lower_2) + ", " + str(lower_3) + ") upper: (" + str(upper_1) + ", " + str(upper_2) + ", " + str(upper_3) + ")")
                #     if 'C' in keys:
                #         lower_3 = lower_3 - 1
                #         print("lower: (" + str(lower_1) + ", " + str(lower_2) + ", " + str(lower_3) + ") upper: (" + str(upper_1) + ", " + str(upper_2) + ", " + str(upper_3) + ")")
                #     if 'V' in keys:
                #         upper_1 = upper_1 - 1
                #         print("lower: (" + str(lower_1) + ", " + str(lower_2) + ", " + str(lower_3) + ") upper: (" + str(upper_1) + ", " + str(upper_2) + ", " + str(upper_3) + ")")
                #     if 'B' in keys:
                #         upper_2 = upper_2 - 1
                #         print("lower: (" + str(lower_1) + ", " + str(lower_2) + ", " + str(lower_3) + ") upper: (" + str(upper_1) + ", " + str(upper_2) + ", " + str(upper_3) + ")")
                #     if 'N' in keys:
                #         upper_3 = upper_3 - 1
                #         print("lower: (" + str(lower_1) + ", " + str(lower_2) + ", " + str(lower_3) + ") upper: (" + str(upper_1) + ", " + str(upper_2) + ", " + str(upper_3) + ")")
                #     if 'Q' in keys:
                #         threshold_line = threshold_line + 1
                #         print("threshold_line: " + str(threshold_line) + " minLineLength: " + str(minLineLength) + " maxLineGap: " + str(maxLineGap))
                #     if 'W' in keys:
                #         minLineLength = minLineLength + 1
                #         print("threshold_line: " + str(threshold_line) + " minLineLength: " + str(minLineLength) + " maxLineGap: " + str(maxLineGap))
                #     if 'E' in keys:
                #         maxLineGap = maxLineGap + 1
                #         print("threshold_line: " + str(threshold_line) + " minLineLength: " + str(minLineLength) + " maxLineGap: " + str(maxLineGap))
                #     if 'R' in keys:
                #         threshold_line = threshold_line - 1
                #         print("threshold_line: " + str(threshold_line) + " minLineLength: " + str(minLineLength) + " maxLineGap: " + str(maxLineGap))
                #     if 'T' in keys:
                #         minLineLength = minLineLength - 1
                #         print("threshold_line: " + str(threshold_line) + " minLineLength: " + str(minLineLength) + " maxLineGap: " + str(maxLineGap))
                #     if 'Y' in keys:
                #         maxLineGap = maxLineGap - 1
                #         print("threshold_line: " + str(threshold_line) + " minLineLength: " + str(minLineLength) + " maxLineGap: " + str(maxLineGap))

            except Exception as e:
                print(e)
                print("Error running EndlessModeCheckLine")
            time.sleep(1)