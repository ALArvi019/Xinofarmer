import pyautogui
from win32gui import FindWindow, GetWindowRect
import time
import cv2 as cv
from windowcapture import WindowCapture


class CheckColors():

    def __init__(self, src_window):
        self.src_window = src_window
        self.wincap = WindowCapture(src_window)

    def check_if_position_contains_color(self, x, y, color, debug=False, tolerance=3):
        window_pos = self.locate_window()
        # get the color of the pixel inside screenshot image
        pixel_color = pyautogui.pixel(window_pos[0] + x, window_pos[1] + y)
        if debug:
            print("----------------------------------------")
            print("Fullx: " + str(window_pos[0] + x) +
                  " Fully: " + str(window_pos[1] + y))
            print("RGB color: " + str(color))
            print("Pixel color: " + str(pixel_color))
            print("----------------------------------------")
        for i in range(tolerance+1):
            pixel_toleranceplus = (
                pixel_color[0]+i, pixel_color[1]+i, pixel_color[2]+i)
            pixel_toleranceminus = (
                pixel_color[0]-i, pixel_color[1]-i, pixel_color[2]-i)
            if debug:
                print("Pixel RGB color: " + str(color))
                print("Pixel color plus:   " + str(pixel_toleranceplus))
                print("Pixel color minus: " + str(pixel_toleranceminus))
            if str(pixel_toleranceplus) == str(color):
                return True
            if str(pixel_toleranceminus) == str(color):
                return True
        return False

    def locate_window(self):
        window_handle = FindWindow(None, self.src_window)
        window_pos = GetWindowRect(window_handle)
        # print(self.src_window + ' position: ' + str(window_pos))
        return window_pos
    
    def get_skills_coords(self):
        return {
                'skill1': {
                    'x': 728,
                    'y': 474,
                    'x2': 760,
                    'y2': 508
                },
                'skill2': {
                    'x': 726,
                    'y': 399,
                    'x2': 757,
                    'y2': 431
                },
                'skill3': {
                    'x': 783,
                    'y': 341,
                    'x2': 815,
                    'y2': 375
                },
                'skill4': {
                    'x': 861,
                    'y': 339,
                    'x2': 893,
                    'y2': 371
                },
            }

    def define_mean_of_skills(self):
        try:
            screenshot = self.wincap.get_screenshot()
            gray = cv.cvtColor(screenshot, cv.COLOR_BGR2GRAY)
            skills_position = self.get_skills_coords()

            result = {}
            for skill in skills_position:
                skillcrop = gray[skills_position[skill]['y']:skills_position[skill]['y2'], skills_position[skill]['x']:skills_position[skill]['x2']]
                ret, skill_thresh = cv.threshold(skillcrop, 30, 255, cv.THRESH_BINARY)
                skill_mean = cv.mean(cv.bitwise_not(skill_thresh))[0]
                result[skill] = int(skill_mean)
            return result

        except Exception as e:
            print('Warn getting screenshot define_mean_of_skills')
            print(e)
            time.sleep(0.5)
            self.define_mean_of_skills()

        
