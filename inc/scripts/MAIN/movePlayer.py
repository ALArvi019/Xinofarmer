import pyautogui
import math
from time import sleep
import random
from checksColors import CheckColors
from preprocess import PreProcessImage
import time
import cv2 as cv
from directkeys import PressKey, ReleaseKey, W, A, S, D
from findImage import RunFindImage
import numpy as np
import pytesseract
import re
from math import cos, sin, atan2, pi

w = [1, 0, 0, 0, 0, 0, 0, 0, 0]
s = [0, 1, 0, 0, 0, 0, 0, 0, 0]
a = [0, 0, 1, 0, 0, 0, 0, 0, 0]
d = [0, 0, 0, 1, 0, 0, 0, 0, 0]
wa = [0, 0, 0, 0, 1, 0, 0, 0, 0]
wd = [0, 0, 0, 0, 0, 1, 0, 0, 0]
sa = [0, 0, 0, 0, 0, 0, 1, 0, 0]
sd = [0, 0, 0, 0, 0, 0, 0, 1, 0]
nk = [0, 0, 0, 0, 0, 0, 0, 0, 1]


class moveplayer:
    def __init__(self, src_window, threads=None, img_path=None, language=None, send_text_to_bot=None, from_python=None):
        self.src_window = src_window
        self.checksColors = CheckColors(src_window)
        if threads is not None:
            self.captureWorker = threads.get_thread('CaptureWorker')
            self.threads = threads
        else:
            self.captureWorker = None
            self.threads = None
        self.preprocess = PreProcessImage()
        self.img_path = img_path
        self.language = language
        self.send_text_to_bot = send_text_to_bot
        self.from_python = from_python
        self.stop_key_thread = False
        pytesseract.pytesseract.tesseract_cmd = self.img_path + '\\..\\tesseract\\tesseract.exe'

    # Función para mover al personaje en una dirección dada
    def move(self, start, end):
        # Mover al personaje a la nueva posición
        directionToMove = ''
        # AW, W, DW
        if end[0] < start[0]:
            # Mover hacia la izquierda
            directionToMove = '←'
            pyautogui.keyDown('a')
            pyautogui.keyUp('d')
            if end[1] < start[1]:
                # Mover hacia arriba
                directionToMove += '↑'
                pyautogui.keyDown('w')
                pyautogui.keyUp('s')
            elif end[1] > start[1]:
                # Mover hacia abajo
                directionToMove += '↓'
                pyautogui.keyDown('s')
                pyautogui.keyUp('w')
            else:
                # No mover verticalmente
                pyautogui.keyUp('w')
                pyautogui.keyUp('s')
        # AS, S, DS
        elif end[0] > start[0]:
            # Mover hacia la derecha
            directionToMove += '→'
            pyautogui.keyDown('d')
            pyautogui.keyUp('a')
            if end[1] < start[1]:
                # Mover hacia arriba
                directionToMove += '↑'
                pyautogui.keyDown('w')
                pyautogui.keyUp('s')
            elif end[1] > start[1]:
                # Mover hacia abajo
                directionToMove += '↓'
                pyautogui.keyDown('s')
                pyautogui.keyUp('w')
            else:
                # No mover verticalmente
                pyautogui.keyUp('w')
                pyautogui.keyUp('s')
        else:
            # No mover horizontalmente
            pyautogui.keyUp('a')
            pyautogui.keyUp('d')
            if end[1] < start[1]:
                # Mover hacia arriba
                directionToMove += '↑'
                pyautogui.keyDown('w')
                pyautogui.keyUp('s')
            elif end[1] > start[1]:
                # Mover hacia abajo
                directionToMove += '↓'
                pyautogui.keyDown('s')
                pyautogui.keyUp('w')
            else:
                # No mover verticalmente
                pyautogui.keyUp('w')
                pyautogui.keyUp('s')
        if 1 == 2:
            if directionToMove == '←':
                print('←')
            elif directionToMove == '→':
                print('→')
            elif directionToMove == '↑':
                print('↑')
            elif directionToMove == '↓':
                print('↓')
            elif directionToMove == '←↑':
                print('↖')
            elif directionToMove == '←↓':
                print('↙')
            elif directionToMove == '→↑':
                print('↗')
            elif directionToMove == '→↓':
                print('↘')

    def releaseAllMovementKeys(self):
        pyautogui.keyUp('a')
        pyautogui.keyUp('w')
        pyautogui.keyUp('s')
        pyautogui.keyUp('d')

    def move_player_to_target(self, target_coords, actual_coords, gray_mapa_completo, wincap, preprocess, astar, checkisdead, accuracy):
        savedDistances = []
        while True:
            if checkisdead.player_is_dead:
                break
            # get current position of the player
            new_coords = astar.calculateActualCoords(
                gray_mapa_completo, wincap, preprocess)
            distance = math.sqrt(
                (new_coords[0] - target_coords[0])**2 + (new_coords[1] - target_coords[1])**2)

            print('distance2Points: ', int(distance))
            counter = 0
            while distance > 50:
                counter += 1
                if counter > 10:
                    return "stuck"
                print('distance is greater than 50: ', distance)
                # self.releaseAllMovementKeys()
                self.MoveRandomly(1, 1)
                new_coords = astar.calculateActualCoords(
                    gray_mapa_completo, wincap, preprocess)
                while new_coords is None:
                    self.MoveRandomly(1, 1)
                    new_coords = astar.calculateActualCoords(
                        gray_mapa_completo, wincap, preprocess)
                distance = math.sqrt(
                    (new_coords[0] - target_coords[0])**2 + (new_coords[1] - target_coords[1])**2)

            if new_coords is None:
                # if current position is not found, wait and try again
                sleep(1)
            elif new_coords == actual_coords:
                # if player has not moved from the previous position, wait and try again
                sleep(0.5)
            else:
                # if current position is found and player has moved, update actual_coords
                actual_coords = new_coords

            # calculate distance between current position and target
            distance = math.sqrt(
                (actual_coords[0] - target_coords[0])**2 + (actual_coords[1] - target_coords[1])**2)
            savedDistances.append(distance)
            # if we haved more than 10 similar distances, we are stuck
            if len(savedDistances) > 5:
                savedDistances.pop(0)
                if all(x == savedDistances[0] for x in savedDistances):
                    self.releaseAllMovementKeys()
                    print('Stuck')
                    # go to last checkpoint
                    return "stuck"

            # if distance > 50:
            #     print('distance is greater than 50: ', distance)
            #     self.releaseAllMovementKeys()
            #     self.MoveRandomly(2, 1)
            #     break

            # check if distance is less than or equal to accuracy
            if distance <= accuracy:
                # print('distance is less than or equal to ' +
                #       str(accuracy)+': ', distance)
                break
            # draw a white line between current position and target
            gray_mapa_completo_tmp = gray_mapa_completo.copy()
            cv.line(gray_mapa_completo_tmp, actual_coords,
                    target_coords, (255, 255, 255), 3)
            self.move(actual_coords, target_coords)
            cv.imshow('gray_mapa_completo', gray_mapa_completo_tmp)
            cv.waitKey(1)

        #     tmp_mapa_completo = mapa_completo.copy()
        #     cv.circle(tmp_mapa_completo, actual_coords, 5, (0, 255, 0), -1)
        #     cv.circle(tmp_mapa_completo, path_end, 5, (0, 0, 255), -1)
        #     cv.circle(tmp_mapa_completo, target_coords, 5, (255, 0, 0), -1)
        #     for j in range(next_path_index, len(path)):
        #         cv.circle(tmp_mapa_completo, path[j], 5, (0, 0, 255), -1)
        #     cv.imshow('mapa_completo', tmp_mapa_completo)
        #     key = cv.waitKey(1)
        #     if key == ord('q'):
        #         cv.destroyAllWindows()
        #         break
        # print("path: ", path)
        # print("next_path_index: ", next_path_index)
        # print("path_end: ", path_end)
        # print("actual_coords: ", actual_coords)
        return actual_coords

    def MoveRandomly(self, steps=1, time=0.5):
        keys = ['w', 'a', 's', 'd']
        for i in range(steps):
            key = random.choice(keys)
            pyautogui.keyDown(key)
            sleep(time)
            pyautogui.keyUp(key)
        sleep(0.1)  # Agregar un pequeño retraso aquí
        self.releaseAllMovementKeys()

    def clickOnCoords(self, coords):
        window_pos = self.checksColors.locate_window()
        pyautogui.click(window_pos[0] + coords[0], window_pos[1] + coords[1])

    def mouseWheel(self, direction, timesToMove, sleepTime=1):
        for i in range(timesToMove):
            pyautogui.scroll(direction)
            time.sleep(sleepTime)

    def mouseMoveTo(self, coords):
        window_pos = self.checksColors.locate_window()
        pyautogui.moveTo(window_pos[0] + coords[0], window_pos[1] + coords[1])

    def mouseDragTo(self, initial_coords, final_coords, button='left'):
        window_pos = self.checksColors.locate_window()
        pyautogui.moveTo(window_pos[0] + initial_coords[0],
                         window_pos[1] + initial_coords[1])
        time.sleep(0.5)
        pyautogui.dragTo(window_pos[0] + final_coords[0],
                         window_pos[1] + final_coords[1],duration=2, button=button)

    def wait_for_loading_screen(self):
        actualtime = time.time()
        timeout = 60

        if self.founfIconInScreen(self.img_path + '\\game_items', 'load_screen', 0, False, self.captureWorker.screenshot, False) != (0, 0):
            loading_image_coords = self.founfIconInScreen(
                self.img_path + '\\game_items', 'load_screen', 0, False, self.captureWorker.screenshot, False)
            self.send_text_to_bot.send(
                "Waiting for loading screen", self.from_python, 'yellow')
            while loading_image_coords == (0, 0) and time.time() - actualtime < timeout:
                loading_image_coords = self.founfIconInScreen(
                    self.img_path + '\\game_items', 'load_screen', 0, False, self.captureWorker.screenshot, False)
                self.send_text_to_bot.send(
                    "Waiting for loading screen (" + str(int(time.time() - actualtime)) + "/" + str(timeout) + ")", self.from_python, 'yellow')
                time.sleep(1)
            if time.time() - actualtime > timeout:
                self.send_text_to_bot.send(
                    "Timeout waiting for loading screen", self.from_python, 'red')
                return False
            self.send_text_to_bot.send(
                "Loading screen found", self.from_python, 'yellow')
            time.sleep(2)
            self.send_text_to_bot.send(
                "Waiting for close loading screen", self.from_python, 'yellow')
            loading_image_coords = self.founfIconInScreen(
                self.img_path + '\\game_items', 'load_screen', 0, False, self.captureWorker.screenshot, False)
            while loading_image_coords != (0, 0) and time.time() - actualtime < timeout:
                loading_image_coords = self.founfIconInScreen(
                    self.img_path + '\\game_items', 'load_screen', 0, False, self.captureWorker.screenshot, False)
                time.sleep(1)
            if time.time() - actualtime > timeout:
                self.send_text_to_bot.send(
                    "Timeout waiting for loading screen", self.from_python, 'red')
                return False
            self.send_text_to_bot.send(
                "Loading screen closed", self.from_python, 'yellow')
            return True

    def waitForTheArrivalToSpot(self):
        actualtime = time.time()
        times_to_check_is_in_spot = 0
        while time.time() - actualtime < 150:  # 3.5 minutos como máximo
            self.send_text_to_bot.send(
                'Waiting to arrive to spot, time left: ' + str(int(150 - (time.time() - actualtime))), self.from_python, 'purple')
            time.sleep(1)
            # Comprobar si se detecta la pantalla de carga
            self.wait_for_loading_screen()

            response = RunFindImage(self.src_window, self.img_path + '\\' + self.language +
                                    '\\farm', 'navto_' + self.language, self.captureWorker.screenshot)
            response2 = RunFindImage(self.src_window, self.img_path + '\\' +
                                     self.language + '\\farm', 'nav_arrow', self.captureWorker.screenshot)
            if response2['nav_arrow'] != 'notfound':
                times_to_check_is_in_spot = 0
                self.clickOnCoords((int(response2['nav_arrow'].split(
                    '|')[0]) - 9, int(response2['nav_arrow'].split('|')[1]) - 5))

            # Salir del bucle si se cumple la condición
            if response['navto_' + self.language] == 'notfound' and response2['nav_arrow'] == 'notfound':
                times_to_check_is_in_spot += 1
                self.send_text_to_bot.send(
                    "Checking if arrived to spot (" + str(times_to_check_is_in_spot) + "/3)", self.from_python, 'purple')

            if times_to_check_is_in_spot > 2:
                break

        self.send_text_to_bot.send(
            "Arrived to POINT", self.from_python, 'green')

    def pressKey(self, key, time=0.5):
        pyautogui.keyDown(key)
        sleep(time)
        pyautogui.keyUp(key)

    def manual_move(self, direction, timesToMove, timeToMove=0.5):
        for i in range(timesToMove):
            if direction == 'North':
                pyautogui.keyDown('w')
            elif direction == 'South':
                pyautogui.keyDown('s')
            elif direction == 'East':
                pyautogui.keyDown('d')
            elif direction == 'West':
                pyautogui.keyDown('a')
            elif direction == 'NorthEast':
                randomnumber = random.randint(1, 2)
                if randomnumber == 1:
                    pyautogui.keyDown('w')
                    pyautogui.keyDown('d')
                else:
                    pyautogui.keyDown('d')
                    pyautogui.keyDown('w')
            elif direction == 'NorthWest':
                randomnumber = random.randint(1, 2)
                if randomnumber == 1:
                    pyautogui.keyDown('w')
                    pyautogui.keyDown('a')
                else:
                    pyautogui.keyDown('a')
                    pyautogui.keyDown('w')
            elif direction == 'SouthEast':
                randomnumber = random.randint(1, 2)
                if randomnumber == 1:
                    pyautogui.keyDown('s')
                    pyautogui.keyDown('d')
                else:
                    pyautogui.keyDown('d')
                    pyautogui.keyDown('s')
            elif direction == 'SouthWest':
                randomnumber = random.randint(1, 2)
                if randomnumber == 1:
                    pyautogui.keyDown('s')
                    pyautogui.keyDown('a')
                else:
                    pyautogui.keyDown('a')
                    pyautogui.keyDown('s')
            sleep(timeToMove)
            self.releaseAllMovementKeys()

    def fast_normal_attack(self, KeyToRelease=False):
        if KeyToRelease:
            pyautogui.keyUp(KeyToRelease)
            return
        randomnumber = random.randint(1, 3)
        if randomnumber == 1:
            pyautogui.keyDown('l')
            return 'l'
        if randomnumber == 2:
            pyautogui.keyDown('n')
            return 'n'
        if randomnumber == 3:
            pyautogui.keyDown('k')
            return 'k'

    def get_distance(self, p1, p2):
        # Calcula la distancia entre dos puntos
        return math.sqrt((p1[0]-p2[0])**2 + (p1[1]-p2[1])**2)

    def get_angle(self, p1, p2):
        # Calcula el ángulo entre dos puntos
        return math.atan2(p2[1]-p1[1], p2[0]-p1[0])

    def move_away_from_monster(self, player_position, monster_position, distance=150):
        # Calcula la distancia actual entre el personaje y el monstruo
        current_distance = self.get_distance(player_position, monster_position)

        # Si la distancia es menor que el límite deseado, mueve al personaje en la dirección opuesta al monstruo
        # print('current_distance: ', int(current_distance) , 'actual_distance: ', distance)
        if int(current_distance) < distance:
            dx = player_position[0] - monster_position[0]
            dy = player_position[1] - monster_position[1]
            length = math.sqrt(dx*dx + dy*dy)
            dx /= length
            dy /= length
            new_x = int(player_position[0] + dx *
                        (distance - current_distance))
            new_y = int(player_position[1] + dy *
                        (distance - current_distance))

            # Mueve al jugador en la dirección opuesta al monstruo
            if dx < 0:
                if dy < 0:
                    pyautogui.keyDown('s')
                    pyautogui.keyDown('a')
                    time.sleep(0.3)
                    pyautogui.keyUp('s')
                    pyautogui.keyUp('a')
                elif dy > 0:
                    pyautogui.keyDown('w')
                    pyautogui.keyDown('a')
                    time.sleep(0.3)
                    pyautogui.keyUp('w')
                    pyautogui.keyUp('a')
                else:
                    pyautogui.keyDown('a')
                    time.sleep(0.3)
                    pyautogui.keyUp('a')
            elif dx > 0:
                if dy < 0:
                    pyautogui.keyDown('s')
                    pyautogui.keyDown('d')
                    time.sleep(0.3)
                    pyautogui.keyUp('s')
                    pyautogui.keyUp('d')
                elif dy > 0:
                    pyautogui.keyDown('w')
                    pyautogui.keyDown('d')
                    time.sleep(0.3)
                    pyautogui.keyUp('w')
                    pyautogui.keyUp('d')
                else:
                    pyautogui.keyDown('d')
                    time.sleep(0.3)
                    pyautogui.keyUp('d')
            else:
                if dy < 0:
                    pyautogui.keyDown('s')
                    time.sleep(0.3)
                    pyautogui.keyUp('s')
                elif dy > 0:
                    pyautogui.keyDown('w')
                    time.sleep(0.3)
                    pyautogui.keyUp('w')

    def pressCustomKey(self, key):
        pyautogui.press(key)

    def fight(self, skills, positionOfMonster_x, positionOfMonster_y, ranged=False, survivor_mode=False, solo_mode=True):
        # Capture screenshot
        try:
            screenshot = self.captureWorker.screenshot
            gray = cv.cvtColor(screenshot, cv.COLOR_BGR2GRAY)
        except:
            print('Warn getting screenshot MovePlayer fight')
            time.sleep(0.5)
            self.fight(skills)

        if survivor_mode is False:
            player_position = (482, 327)

            skills_position = self.checksColors.get_skills_coords()

            for skill in skills_position:
                skillcrop = gray[skills_position[skill]['y']:skills_position[skill]
                                 ['y2'], skills_position[skill]['x']:skills_position[skill]['x2']]
                ret, skill_thresh = cv.threshold(
                    skillcrop, 30, 255, cv.THRESH_BINARY)
                skill_mean = cv.mean(cv.bitwise_not(skill_thresh))[0]
                # compare int(skill_mean) with skills[skill]
                if int(skill_mean) >= skills[skill]:
                    # get the last character of the skill name
                    skill_key = skill[-1]
                    pyautogui.press(skill_key)
                    pyautogui.press(skill_key)
                    pyautogui.press(skill_key)
                if ranged:
                    self.move_away_from_monster(
                        player_position, (positionOfMonster_x, positionOfMonster_y))
                    self.releaseAllMovementKeys()
                    # else: melee. Move little bit to the monster TODO: improve this
                    # if positionOfMonster_x > player_position[0]:
                    #     pyautogui.keyDown('d')
        if solo_mode:
            pyautogui.press('5')

    def straight(self):
        PressKey(W)
        ReleaseKey(A)
        ReleaseKey(D)
        ReleaseKey(S)

    def left(self):
        ReleaseKey(W)
        PressKey(A)
        ReleaseKey(S)
        ReleaseKey(D)

    def right(self):
        ReleaseKey(W)
        PressKey(D)
        ReleaseKey(A)
        ReleaseKey(S)

    def reverse(self):
        PressKey(S)
        ReleaseKey(A)
        ReleaseKey(W)
        ReleaseKey(D)

    def forward_left(self):
        PressKey(W)
        PressKey(A)
        ReleaseKey(D)
        ReleaseKey(S)

    def forward_right(self):
        PressKey(W)
        PressKey(D)
        ReleaseKey(A)
        ReleaseKey(S)

    def reverse_left(self):
        PressKey(S)
        PressKey(A)
        ReleaseKey(W)
        ReleaseKey(D)

    def reverse_right(self):
        PressKey(S)
        PressKey(D)
        ReleaseKey(W)
        ReleaseKey(A)

    def no_keys(self):
        ReleaseKey(W)
        ReleaseKey(A)
        ReleaseKey(S)
        ReleaseKey(D)
        ReleaseKey(W)
        ReleaseKey(A)
        ReleaseKey(S)
        ReleaseKey(D)

    def print_key(self, choice):
        if choice == w:
            print('w')
        elif choice == s:
            print('s')
        elif choice == a:
            print('a')
        elif choice == d:
            print('d')
        elif choice == wa:
            print('wa')
        elif choice == wd:
            print('wd')
        elif choice == sa:
            print('sa')
        elif choice == sd:
            print('sd')
        elif choice == nk:
            print('nk')

    def processing_movement_output(self, best_choice):
        # self.print_key(best_choice)
        if best_choice == '↑':
            self.straight()
        elif best_choice == '↓':
            self.reverse()
        elif best_choice == '←':
            self.left()
        elif best_choice == '→':
            self.right()
        elif best_choice == '↖':
            self.forward_left()
        elif best_choice == '↗':
            self.forward_right()
        elif best_choice == '↙':
            self.reverse_left()
        elif best_choice == '↘':
            self.reverse_right()
        elif best_choice == 'NK':
            self.no_keys()

    def processing_reverse_movement_output(self, best_choice):
        # self.print_key(best_choice)
        if best_choice == '↑':
            self.reverse()
        elif best_choice == '↓':
            self.straight()
        elif best_choice == '←':
            self.right()
        elif best_choice == '→':
            self.left()
        elif best_choice == '↖':
            self.reverse_right()
        elif best_choice == '↗':
            self.reverse_left()
        elif best_choice == '↙':
            self.forward_right()
        elif best_choice == '↘':
            self.forward_left()
        elif best_choice == 'NK':
            self.no_keys()

    def movePlayerToReverseDirection(self, positionOfLoot):
        if positionOfLoot == 'North':
            self.reverse()
            sleep(1)
        elif positionOfLoot == 'South':
            self.straight()
            sleep(1)
        elif positionOfLoot == 'East':
            self.left()
            sleep(1)
        elif positionOfLoot == 'West':
            self.right()
            sleep(1)
        elif positionOfLoot == 'NorthEast':
            self.reverse_left()
            sleep(1)
        elif positionOfLoot == 'NorthWest':
            self.reverse_right()
            sleep(1)
        elif positionOfLoot == 'SouthEast':
            self.forward_left()
            sleep(1)
        elif positionOfLoot == 'SouthWest':
            self.forward_right()
            sleep(1)
        self.no_keys()

    def openMap(self, leftMenu=False):
        # Open the map
        count = 0
        while self.checksColors.check_if_position_contains_color(57, 78, (115, 39, 9)) == False and self.checksColors.check_if_position_contains_color(40, 306, (120, 66, 59)) == False and self.checksColors.check_if_position_contains_color(945, 76, (125, 48, 18)) == False:
            self.send_text_to_bot.send(
                "Try to open map (" + str(count) + "/100)", self.from_python)
            if count == 100:
                print("cannt open map " + str(count))
                sleep(20)
                return False
            count = count + 1
            pyautogui.press('m')
            sleep(0.5)
        if leftMenu:
            sleep(1)
            self.clickOnCoords((36, 305))
        return True

    def openLeftMapMenu(self):
        self.clickOnCoords((36, 305))

    def closeLeftMapMenu(self):
        self.clickOnCoords((303, 311))

    def ctrl_scroll(self, timesToMove):
        pyautogui.keyDown('ctrl')
        pyautogui.scroll(timesToMove)
        pyautogui.keyUp('ctrl')

    def ctrl_scrollv2(self, direction, timesToMove, sleepTime=1):
        pyautogui.keyDown('ctrl')
        self.mouseWheel(direction, timesToMove, sleepTime)
        pyautogui.keyUp('ctrl')
        time.sleep(sleepTime)

    def GoToSafeZone(self, left_menu, spot_safe_zone):
        if spot_safe_zone == (0, 0):
            self.send_text_to_bot.send("Custom model, then the bot can't go to safe zone", self.from_python)
            return True
        self.send_text_to_bot.send("Going to safe zone", self.from_python)
        if self.openMap(False) == False:
            self.send_text_to_bot.send("Error opening map", self.from_python)
            return False
        time.sleep(1)
        self.openLeftMapMenu()
        time.sleep(1)
        self.clickOnCoords(left_menu)
        time.sleep(1)
        # close left menu
        self.closeLeftMapMenu()
        time.sleep(1)
        self.clickOnCoords((509, 142))
        time.sleep(1)
        self.mouseMoveTo((456, 368))
        time.sleep(1)
        self.ctrl_scroll(10000)
        time.sleep(1)
        self.clickOnCoords(spot_safe_zone)
        time.sleep(1)
        self.clickOnCoords(spot_safe_zone)
        time.sleep(1)
        if self.clickOnNavigateOrTeleport((spot_safe_zone)) is False:
            return False
        time.sleep(5)
        self.waitForTheArrivalToSpot()
        return True

    def founfIconInScreen(self, img_path, image_name, fails, insideMap, screenshot=None, showMessage=True, gray=True, threshold=0.8):
        if insideMap:
            time.sleep(2)
            self.mouseMoveTo((144, 278))
            time.sleep(2)
        BSFoundIcon = False
        Fails = 0
        PositionOFBS_x = 0
        PositionOFBS_y = 0
        while BSFoundIcon is False:
            if Fails > fails:
                if showMessage:
                    self.send_text_to_bot.send(
                        "We are stuck trying to find " + image_name, self.from_python)
                return (0, 0)
            response = RunFindImage(
                self.src_window, img_path, image_name, screenshot, threshold, False, gray)
            if response[image_name] == 'notfound':
                if insideMap:
                    self.mouseWheel(-150, 1)
                Fails = Fails + 1
                if Fails > fails:
                    if showMessage:
                        self.send_text_to_bot.send(
                            "We are stuck trying to find " + image_name, self.from_python)
                    return (0, 0)
                time.sleep(1)
            else:
                # print(response)
                PositionOFBS_x = response[image_name].split('|')[0]
                PositionOFBS_y = response[image_name].split('|')[1]
                BSFoundIcon = True

        return (int(PositionOFBS_x), int(PositionOFBS_y))

    def clickOnNavigateOrTeleport(self, coords=None):
        # check images for 10 times
        timestocheck = 0
        while timestocheck < 10:
            for image_type in ['navigate_', 'teleport_']:
                response = RunFindImage(
                    self.src_window, self.img_path + '\game_items', image_type + self.language, self.captureWorker.screenshot)
                if response[image_type + self.language] == 'notfound':
                    timestocheck += 1
                    self.send_text_to_bot.send(
                        f"Error finding {image_type} button, retrying ({timestocheck}/10)", self.from_python)
                    if coords is not None:
                        self.clickOnCoords(coords)
                    time.sleep(1)
                else:
                    self.send_text_to_bot.send(
                        f"{image_type.capitalize()} button found", self.from_python)
                    self.clickOnCoords((int(response[image_type + self.language].split(
                        '|')[0]) - 9, int(response[image_type + self.language].split('|')[1])))
                    return True  # Se encontró alguna de las imágenes, salimos de la función
        self.send_text_to_bot.send(
            "Error finding navigation or teleport button, RESET", self.from_python)
        return False

    def checkIfPlayerIsNearTo(self, object):
        if object == 'fisherman' or object == 'blacksmith':
            objectName = 'talk'
            objectPath = '\\game_items'
        if object == 'bestiary':
            objectName = 'hand_up'
            objectPath = '\\game_items'
        if object == 'loot_hand_down':
            objectName = 'hand_down'
            objectPath = '\\game_items'
        if object == 'fishzone':
            objectName = 'fishicon'
            objectPath = '\\fishing'
        if object == 'exit_fish':
            objectName = 'exit_fishing'
            objectPath = '\\fishing'
        if object == 'portal':
            objectName = 'portal'
            objectPath = '\\game_items'

        response = RunFindImage(
            self.src_window, self.img_path + objectPath, objectName, self.captureWorker.screenshot)
        if response[objectName] == 'notfound':
            return False
        else:
            return True

    def openInventory(self):
        # open inventory B key
        # while inventory_bag_image not found, pres key b and wait 1 second
        count = 0

        while self.founfIconInScreen(self.img_path + '\\game_items', 'inventory_bag', 0, False, self.captureWorker.screenshot, False) == (0, 0):
            self.send_text_to_bot.send(
                "Try to open inventory (" + str(count) + "/10)", self.from_python)
            pyautogui.press('b')
            time.sleep(2)
            if self.founfIconInScreen(self.img_path + '\\game_items', 'inventory_bag', 0, False, self.captureWorker.screenshot, False) != (0, 0):
                return True
            count = count + 1
            if count > 10:
                return False
        time.sleep(1)
        return True
    
    def foundPetIcon(self, action='recycle'):
        count = 0
        pet_icon_coords = self.founfIconInScreen(self.img_path + '\\game_items', 'pet_icon', 0, False, self.captureWorker.screenshot, False)
        while pet_icon_coords == (0, 0):
            self.send_text_to_bot.send(
                "Try to find pet icon (" + str(count) + "/10)", self.from_python)
            if count > 10:
                return False
            count = count + 1
            time.sleep(1)
            pet_icon_coords = self.founfIconInScreen(self.img_path + '\\game_items', 'pet_icon', 0, False, self.captureWorker.screenshot, False)
            
        if action == 'recycle':
            self.clickOnCoords(pet_icon_coords)
            time.sleep(1)
            pet_recycle_coords = self.founfIconInScreen(self.img_path + '\\game_items', 'pet_recycle', 0, False, self.captureWorker.screenshot, False)
            while pet_recycle_coords == (0, 0):
                self.send_text_to_bot.send(
                    "Try to find pet recycle (" + str(count) + "/10)", self.from_python)
                if count > 10:
                    return False
                count = count + 1
                time.sleep(1)
                pet_recycle_coords = self.founfIconInScreen(self.img_path + '\\game_items', 'pet_recycle', 0, False, self.captureWorker.screenshot, False)
            self.clickOnCoords(pet_recycle_coords)
            time.sleep(1)
            return True


    def checkInventoryPercentage(self, screenshot):
        hsv = cv.cvtColor(screenshot, cv.COLOR_BGR2HSV)

        # Definir el rango de colores que deseas detectar en HSV
        lower_color = np.array([0, 75, 75])
        upper_color = np.array([255, 255, 255])

        mask = cv.inRange(hsv, lower_color, upper_color)
        # Calcular el número de píxeles negros
        num_black_pixels = cv.countNonZero(
            (mask == 0).astype(np.uint8) if np.any(mask) else mask)
        total_pixels = mask.shape[0] * mask.shape[1]
        # if not color found and only found black return 0
        if not np.any(mask):
            return 0
        black_ratio = num_black_pixels / total_pixels
        percent = 100 - int(black_ratio * 100)
        return int(percent)

    def checkInventory(self, percentageLimit):
        if self.openInventory() is False:
            return False
        # crop image 741, 509 to 754, 537
        cropped = self.captureWorker.screenshot[509:537, 741:754]
        ActualPercertage = self.checkInventoryPercentage(cropped)

        self.send_text_to_bot.send(
            "The inventory is at " + str(ActualPercertage) + "%", self.from_python, 'yellow')
        self.send_text_to_bot.send(
            "% tocheck inventory " + str(percentageLimit) + "%", self.from_python, 'yellow')

        # press esc
        pyautogui.press('esc')
        if ActualPercertage >= percentageLimit:
            # checkinventory
            return True
        else:
            # NOT checkinventory
            return False

    def goToFisherman(self):
        self.send_text_to_bot.send("Going to fisherman", self.from_python)
        if self.openMap(True) == False:
            self.send_text_to_bot.send(
                "Error opening map", self.from_python, 'red')
            return False
        time.sleep(1)
        self.mouseMoveTo((144, 278))
        time.sleep(1)
        BFMFoundIcon = False
        Fails = 0
        while BFMFoundIcon is False:
            if Fails > 4:
                self.send_text_to_bot.send(
                    "We are stuck to find fisherman", self.from_python, 'red')
                return False
            response = RunFindImage(self.src_window, self.img_path +
                                    '\\mapLegend', 'fisherman', self.captureWorker.screenshot)
            if response['fisherman'] == 'notfound':
                self.mouseWheel(-150, 1)
                time.sleep(1)
                Fails = Fails + 1
            else:
                print(response)
                PositionOFFM_x = response['fisherman'].split('|')[0]
                PositionOFFM_y = response['fisherman'].split('|')[1]
                BFMFoundIcon = True
        # click on the fisherman
        self.clickOnCoords(
            (int(PositionOFFM_x), int(PositionOFFM_y)))
        time.sleep(1)
        # click on the teleport button
        self.clickOnNavigateOrTeleport()
        for i in range(3):
            time.sleep(1)
            self.send_text_to_bot.send(
                'Waiting to teleport to fisherman: ' + str(3 - i), self.from_python, 'purple')
        self.waitForTheArrivalToSpot()
        if self.checkIfPlayerIsNearTo('fisherman') is False:
            self.send_text_to_bot.send(
                "Error arriving to fisherman", self.from_python, 'red')
            return False
        return True

    def buyBait(self):
        # # press f
        pyautogui.press('f')
        time.sleep(1)
        # find and click on shop image
        shop_image_coords = self.founfIconInScreen(
            self.img_path + '\\fishing', 'shop', 3, False, self.captureWorker.screenshot, False)
        if shop_image_coords == (0, 0):
            self.send_text_to_bot.send(
                "Error finding shop button", self.from_python, 'red')
            return False
        self.clickOnCoords(shop_image_coords)
        time.sleep(2)
        number_of_fish_coords = self.founfIconInScreen(
            self.img_path + '\\fishing', 'amount', 2, False, self.captureWorker.screenshot, False)
        if number_of_fish_coords == (0, 0):
            self.send_text_to_bot.send(
                "Can't buy more bait", self.from_python, 'red')
            self.pressKey('esc')
            time.sleep(2)
            return True
        self.clickOnCoords((809, 464))
        time.sleep(2)
        self.clickOnCoords((879, 341))
        time.sleep(1)
        self.clickOnCoords((879, 341))
        time.sleep(1)
        self.clickOnCoords((863, 404))
        time.sleep(1)
        self.clickOnCoords((821, 514))
        time.sleep(1)
        self.pressKey('esc')
        time.sleep(2)
        return True

    def sellFish(self, SecondsToTurnLoot):
        # # press f
        pyautogui.press('f')
        time.sleep(1)
        # find and click on fish_trading image
        fish_trading_image_coords = self.founfIconInScreen(
            self.img_path + '\\fishing', 'fish_trading', 3, False, self.captureWorker.screenshot, False)
        if fish_trading_image_coords == (0, 0):
            self.send_text_to_bot.send(
                "Error finding fish_trading button", self.from_python, 'red')
            return False
        self.clickOnCoords(fish_trading_image_coords)
        time.sleep(2)
        self.clickOnCoords((481, 526))
        time.sleep(2)
        # find exchange button
        exchange_image_coords = self.founfIconInScreen(
            self.img_path + '\\fishing', 'exchange', 2, False, self.captureWorker.screenshot, False, False, 0.9)
        if exchange_image_coords == (0, 0):
            self.send_text_to_bot.send(
                "We have no fish to sell", self.from_python, 'red')
            self.pressKey('esc')
            time.sleep(2)
            return True
        self.clickOnCoords(exchange_image_coords)
        for i in range(10):
            time.sleep(1)
            self.send_text_to_bot.send(
                'Waiting to loot: ' + str(10 - i), self.from_python, 'purple')
            
        self.move_circle_8_directions(SecondsToTurnLoot)

        checkLootThread = self.threads.get_thread('CheckLoot')
        checkLootThread.in_BESTIARY = True  # for reverse movement
        self.threads.resume_thread('CheckLoot')
        while checkLootThread.times_to_not_found_loot < 20:
            fish_trading_image_coords = self.founfIconInScreen(
            self.img_path + '\\fishing', 'fish_trading', 0, False, self.captureWorker.screenshot, False)
            if fish_trading_image_coords != (0, 0):
                self.send_text_to_bot.send(
                    "MissClick on fish_trading button", self.from_python, 'red')
                self.clickOnCoords((501, 63))
            self.send_text_to_bot.send(
                "Waiting to found all loot in screen", self.from_python, 'yellow')
            time.sleep(5)
        self.threads.pause_thread('CheckLoot')

        return True

    def goToFish(self, fish_data):
        self.send_text_to_bot.send(
            "Going to '" + fish_data['name'] + "'", self.from_python)
        if fish_data['near_fisherman'] == True:
            self.send_text_to_bot.send(
                "The spot is near to fisherman", self.from_python)
            # while talk icon is found
            while self.checkIfPlayerIsNearTo('fisherman') is True:
                self.processing_movement_output(
                    fish_data['near_fisherman_move'])
                time.sleep(0.2)
                self.processing_movement_output('NK')
                time.sleep(0.2)
        else:
            if self.openMap(True) == False:
                self.send_text_to_bot.send(
                    "Error opening map", self.from_python, 'red')
                return False
            time.sleep(1)
            self.mouseMoveTo((144, 278))
            time.sleep(1)
            BFMFoundIcon = False
            Fails = 0
            while BFMFoundIcon is False:
                if Fails > 4:
                    self.send_text_to_bot.send(
                        "We are stuck to find + '" + fish_data['name'] + "'", self.from_python, 'red')
                    return False
                response = RunFindImage(self.src_window, self.img_path + '\\mapLegend',
                                        fish_data['left_menu_image'], self.captureWorker.screenshot)
                if response[fish_data['left_menu_image']] == 'notfound':
                    self.mouseWheel(-150, 1)
                    time.sleep(1)
                    Fails = Fails + 1
                else:
                    print(response)
                    PositionOFFM_x = response[fish_data['left_menu_image']].split('|')[
                        0]
                    PositionOFFM_y = response[fish_data['left_menu_image']].split('|')[
                        1]
                    BFMFoundIcon = True
            # click on the fisherman
            self.clickOnCoords(
                (int(PositionOFFM_x), int(PositionOFFM_y)))
            time.sleep(2)
            self.clickOnCoords((510, 99))
            time.sleep(2)
            self.mouseMoveTo((456, 368))
            time.sleep(1)
            self.ctrl_scrollv2(800, 3)
            time.sleep(1)
            
            if fish_data['drag_mouse'] is not None:
                for drag_mouse in fish_data['drag_mouse']:
                    self.mouseDragTo(drag_mouse['initial_position'],
                                        drag_mouse['final_position'], "left")
                    time.sleep(1)
            # time.sleep(99)
            random.shuffle(fish_data['spot_coords'])
            self.clickOnCoords(fish_data['spot_coords'][0])
            # click on the teleport button
            self.clickOnNavigateOrTeleport()
            for i in range(3):
                time.sleep(1)
                self.send_text_to_bot.send(
                    'Waiting to teleport to ' + fish_data['name'] + ': ' + str(3 - i), self.from_python, 'purple')
            self.waitForTheArrivalToSpot()
        if self.checkIfPlayerIsNearTo('fishzone') is False:
            self.send_text_to_bot.send(
                "Error arriving to " + fish_data['name'], self.from_python, 'red')
            return False
        self.send_text_to_bot.send(
            "Arrived to " + fish_data['name'], self.from_python, 'green')
        if fish_data['fish_zone_random_movements'] is not None:
            self.send_text_to_bot.send(
                "Make random movement", self.from_python)
            random.shuffle(fish_data['fish_zone_random_movements'])
            self.processing_movement_output(
                        fish_data['fish_zone_random_movements'][0])
            time.sleep(0.2)
            self.processing_movement_output('NK')
            time.sleep(0.2)
            if self.checkIfPlayerIsNearTo('fishzone') is False:
                count = 0
                while self.checkIfPlayerIsNearTo('fishzone') is False:
                    if count > 10:
                        self.send_text_to_bot.send(
                            "Error checking fish zone", self.from_python, 'red')
                        return False
                    self.processing_reverse_movement_output(
                        fish_data['fish_zone_random_movements'][0])
                    time.sleep(0.2)
                    self.processing_reverse_movement_output('NK')
                    time.sleep(0.2)
                    count = count + 1
        return True
    
    import re

    def getQuantityOfItem(self, image_coords, type_of_item):
        if type_of_item == 'yellow_dust':
            lower_color = np.array([25, 189, 82], dtype=np.uint8)
            upper_color = np.array([27, 205, 139], dtype=np.uint8)
        elif type_of_item == 'scrap':
            lower_color = np.array([15, 151, 78], dtype=np.uint8)
            upper_color = np.array([27, 207, 165], dtype=np.uint8)

        crop_image = self.captureWorker.screenshot[image_coords[1] + 17:image_coords[1] + 17 + 14, image_coords[0] - 10:image_coords[0] + 22]

        # Redimensiona la imagen
        crop_image = cv.resize(crop_image, (0, 0), fx=2, fy=2)

        # Convierte la imagen a formato HSV
        hsv_image = cv.cvtColor(crop_image, cv.COLOR_BGR2HSV)

        # Filtra los píxeles en el rango de colores
        mask = cv.inRange(hsv_image, lower_color, upper_color)

        # Aplica la máscara a la imagen original
        filtered_image = cv.bitwise_and(crop_image, crop_image, mask=mask)

        # Convierte la imagen filtrada a escala de grises
        gray_image = cv.cvtColor(filtered_image, cv.COLOR_BGR2GRAY)

        # Mejora el contraste y aplica umbralización
        _, thresholded_image = cv.threshold(gray_image, 0, 255, cv.THRESH_BINARY + cv.THRESH_OTSU)

        inverted_image = cv.bitwise_not(thresholded_image)

        # Redimensiona la imagen nuevamente si es necesario
        scaled_image = cv.resize(inverted_image, (0, 0), fx=2, fy=2)
        custom_config = r'--oem 3 --psm 6 outputbase digits'
        text = pytesseract.image_to_string(scaled_image, config=custom_config)

        # Utiliza una expresión regular para extraer solo los números
        numbers = re.findall(r'\d+', text)

        # Convierte la lista de números a una cadena
        cleaned_text = ''.join(numbers)

        # Print in red
        print("\033[91m" + "------------> " + cleaned_text + "\033[0m")

        return cleaned_text

    def move_circle_8_directions(self, seconds):
        seconds = int(seconds)
        start_time = time.time()

        while time.time() - start_time < seconds:
            angle = (time.time() - start_time) * pi  # Ajusta la velocidad aquí

            # Calcula las coordenadas en un círculo
            x = 5 * cos(angle)  # Ajusta el radio del círculo aquí
            y = 5 * sin(angle)  # Ajusta el radio del círculo aquí

            # Calcula la dirección hacia las coordenadas calculadas
            best_choice = self.determine_direction(x, y)

            # Mueve el personaje en la dirección determinada
            self.processing_movement_output(best_choice)

            # Ajusta el tiempo de espera para cambiar la velocidad de movimiento circular
            time.sleep(0.05)  # Puedes ajustar este valor según tus preferencias
        self.processing_movement_output('NK')
        self.processing_movement_output('NK')
        self.processing_movement_output('NK')
        self.processing_movement_output('NK')

    def determine_direction(self, x, y):
        # Esta función determina la dirección en función de las coordenadas (x, y)
        # Puedes ajustar esto según tus necesidades específicas
        angle = atan2(y, x)
        angle_deg = angle * (180 / pi)
        angle_deg += 360  # Asegura que el ángulo esté en el rango [0, 360)

        # Dividimos el círculo en 8 direcciones
        directions = ['→', '↗', '↑', '↖', '←', '↙', '↓', '↘']
        index = round(angle_deg / 45) % 8

        return directions[index]