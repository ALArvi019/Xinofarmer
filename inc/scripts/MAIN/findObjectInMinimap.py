import cv2 as cv
import time
import math
import numpy as np
from captureWorker import CaptureWorker
from preprocess import PreProcessImage
from movePlayer import moveplayer
from sendTextToBot import SendTextToBot
from GeomUtil import GeomUtil


def FindObjectInMinimap(captureworker, fight, moveplayer, path, filename, move_to_object, retries=8, wait_fight=True, screenshot_arg=None):
    preprocess = PreProcessImage()
    send_text_to_bot = SendTextToBot()

    movements = ['→', '↘', '↓', '↙', '←', '↖', '↑', '↗']

    found_once = False

    while True:
        if screenshot_arg is None:
            screenshot = captureworker.screenshot
            minimap1 = preprocess.crop(screenshot, 740, 40, 173, 110)
        else:
            minimap1 = screenshot

        object_position = moveplayer.founfIconInScreen(
            path, filename, 1, False, minimap1, False, False, 0.75)

        for i in range(retries):
            if object_position != (0, 0):
                found_once = True
                break
            else:
                if wait_fight is True:
                    if fight.checkFightIsRunning() is True:
                        print('DEBUG: execute_action Waiting to fight')
                        time.sleep(1)
                        while fight.checkFightIsRunning() is True:
                            print('DEBUG: execute_action Waiting to fight')
                            time.sleep(1)
                        if found_once is True:
                            return (1, 1)
                        return (0, 0)
                if move_to_object is True:
                    pass
                    # print('DEBUG: Not found image ' + filename + ' in minimap, retry ' +
                    #       str(i+1) + ' of ' + str(retries) + ' and move to object')
                    # moveplayer.processing_movement_output(movements[i])
                    # time.sleep(0.7)
                    # moveplayer.processing_movement_output('NK')
                screenshot = captureworker.screenshot
                minimap1 = preprocess.crop(screenshot, 740, 40, 173, 110)
                object_position = moveplayer.founfIconInScreen(
                    path, filename, 1, False, minimap1, False, False, 0.75)
                # print("not found image " + filename +
                #       " in minimap, retry " + str(i+1) + " of " + str(retries))
                if wait_fight is True:
                    if fight.checkFightIsRunning() is True:
                        print('DEBUG: execute_action Waiting to fight')
                        time.sleep(1)
                        while fight.checkFightIsRunning() is True:
                            print('DEBUG: execute_action Waiting to fight')
                            time.sleep(1)
                        if found_once is True:
                            return (1, 1)
                        return (0, 0)
                time.sleep(1)

        if object_position == (0, 0):
            # print("not found image " + filename + " in minimap FALSE!!!")
            if found_once is True:
                return (1, 1)
            return (0, 0)

        if move_to_object is False:
            return object_position

        player_position = (87, 57)

        # print('object_position-->',object_position)
        # print('player_position-->',player_position)

        # draw in minimap1 an arrow between player and object
        # cv.arrowedLine(minimap1, player_position,
        #                object_position, (255, 255, 0), 3)

        # get distance between player and object
        distance = moveplayer.get_distance(player_position, object_position)
        # print('distance-->',distance)

        # calculate angle between player and object
        delta_x = object_position[0] - player_position[0]
        delta_y = object_position[1] - player_position[1]
        angleInDegrees = math.atan2(delta_y, delta_x) * GeomUtil.toDEGREES

        # set angle between 0 and 360
        if angleInDegrees < 0:
            angleInDegrees += 360

        # print('angleInDegrees-->',angleInDegrees)

        # divide a 360 circle in 8 parts
        angleInDegrees = int(angleInDegrees)
        angleInDegrees = angleInDegrees + 22
        if angleInDegrees > 360:
            angleInDegrees = angleInDegrees - 360
        angleInDegrees = int(angleInDegrees / 45)
        movement = movements[angleInDegrees]
        # print('movement-->', movement)
        moveplayer.processing_movement_output(movement)
        time.sleep(0.7)
        moveplayer.processing_movement_output('NK')

        send_text_to_bot.send(movement + " to reach the object.")

        # cv.imshow('test', minimap1)
        # if cv.waitKey(1) & 0xFF == ord('q'):
        #      cv.destroyAllWindows()
        #     captureworker.stop()
        #     break
        # captureworker.stop()


def findSpecificItemOnMinimap(screenshot, itemToFind, to_count, crop, debug_lower=None, debug_upper=None):
    if itemToFind == 'cyrangar_door':
        lower_colors = [5, 168, 185]
        upper_colors = [9, 180, 237]
    elif itemToFind == 'boss':
        # lower: (0, 213, 168) upper: (0, 251, 206)
        lower_colors = [0, 213, 168]
        upper_colors = [0, 251, 206]
    elif itemToFind == 'exit_portal':
        # lower: (91, 135, 147) upper: (95, 144, 189)
        lower_colors = [90, 135, 147]
        upper_colors = [95, 144, 189]
    elif itemToFind == 'blacksmith':
    # lower: (79, 0, 55) upper: (127, 58, 159)
    # (hMin = 100 , sMin = 10, vMin = 87), (hMax = 110 , sMax = 70, vMax = 135)
        lower_colors = [100, 10, 87]
        upper_colors = [110, 70, 135]
        # lower_colors = debug_lower
        # upper_colors = debug_upper
    elif itemToFind == 'dungeon_chest':
        # (hMin = 15 , sMin = 102, vMin = 150), (hMax = 26 , sMax = 136, vMax = 208)
        lower_colors = [15, 102, 150]
        upper_colors = [26, 136, 208]
    else:
        return None, None

    movements = ['→', '↘', '↓', '↙', '←', '↖', '↑', '↗']

    movement = None
    distance = None

    try:

        preprocess = PreProcessImage()
        send_text_to_bot = SendTextToBot()

        if crop is True:
            screenshot = preprocess.crop(screenshot, 740, 40, 173, 110)

        screenshot_hsv = cv.cvtColor(screenshot, cv.COLOR_BGR2HSV)
        lower = np.array(lower_colors)
        upper = np.array(upper_colors)

        mask = cv.inRange(screenshot_hsv, lower, upper)

        count = cv.countNonZero(mask)

        if count > to_count:
            # get position of mask in image
            y, x = np.nonzero(mask)
            # get center of mask
            center_of_image = (int(np.mean(x)), int(np.mean(y)))
            # print('DEBUG: center-->', center)
            player_position = (87, 57)

            distance = moveplayer.get_distance(None, player_position, center_of_image)

            # calculate angle between player and object
            delta_x = center_of_image[0] - player_position[0]
            delta_y = center_of_image[1] - player_position[1]
            angleInDegrees = math.atan2(
                delta_y, delta_x) * GeomUtil.toDEGREES

            # set angle between 0 and 360
            if angleInDegrees < 0:
                angleInDegrees += 360

            angleInDegrees = int(angleInDegrees)
            angleInDegrees = angleInDegrees + 22
            if angleInDegrees > 360:
                angleInDegrees = angleInDegrees - 360
            angleInDegrees = int(angleInDegrees / 45)
            movement = movements[angleInDegrees]
            # print('movement-->', movement)
            # self.send_text_to_bot.send("El jugador debe moverse hacia " + movement + " para alcanzar la puerta", self.from_python)
            send_text_to_bot.send(
                movement + " to reach " + itemToFind, False, "orange")
            


            # DEBUG ↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓
            # DEBUG ---------------------------------------------
            # DEBUG ---------------------------------------------
            # DEBUG ---------------------------------------------
            if 1 == 2:
                movement_debug = {"→": "right", "↘": "down-right", "↓": "down", "↙": "down-left",
                                    "←": "left", "↖": "up-left", "↑": "up", "↗": "up-right"}
                # print arrow betbewn player and object
                cv.arrowedLine(screenshot, player_position,
                                    center_of_image, (255, 255, 0), 3)
                # print movement in image
                cv.putText(screenshot, movement_debug[movement], (10, 20),
                                cv.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1, cv.LINE_AA)
                # print distance in image
                cv.putText(screenshot, str(int(distance)), (10, 40),
                                cv.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1, cv.LINE_AA)
                # print actual seconds
                cv.putText(screenshot, str(int(time.time())), (10, 60),
                                cv.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1, cv.LINE_AA)
                cv.imshow('test', screenshot)
                if cv.waitKey(1) & 0xFF == ord('q'):
                    cv.destroyAllWindows()
            # DEBUG ↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑
            # DEBUG ---------------------------------------------
            # DEBUG ---------------------------------------------
            # DEBUG ---------------------------------------------
            
        # return movement and distance+
        return movement, distance
    except Exception as e:
        print('ERROR: findSpecificItemOnMinimap', e)
        return None, None
        



# capture = CaptureWorker(
#     "LDPlayer", "path\\to\\immortal_xinofarmer\\inc\\img")
# capture.start()
# send_text_to_bot = SendTextToBot()
# Moveplayer = moveplayer(
#     "LDPlayer", None, "path\\to\\immortal_xinofarmer\\inc\\img", "en", send_text_to_bot, True)
# for i in list(range(2))[::-1]:
#     print(i+1)
#     time.sleep(1)
