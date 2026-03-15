from findImage import RunFindImage
from checksColors import CheckColors
import time
import threading
import gc
import cv2 as cv
import numpy as np
from readINI import ReadINIFile



class Blacksmith(threading.Thread):
    def __init__(self, threads, src_window, img_blacksmith_path, language, Moveplayer, fileName, inc_path, move_to_blacksmith, send_text_to_bot, from_python, left_menu, spot_safe_zone):
        threading.Thread.__init__(self)
        self.src_window = src_window
        self.checksColors = CheckColors(src_window)
        self.stopped = False
        self.player_is_dead = False
        self.paused = False
        self.img_path = img_blacksmith_path
        self.captureWorker = threads.get_thread('CaptureWorker')
        self.language = language
        self.threads = threads
        self.fight = threads.get_thread('Fight')
        self.moveplayer = Moveplayer
        self.spotWorker = threads.get_thread('SpotWorker')
        self.fileName = fileName
        self.inc_path = inc_path
        self.move_to_blacksmith = move_to_blacksmith
        self.send_text_to_bot = send_text_to_bot
        self.from_python = from_python
        self.spot_safe_zone = spot_safe_zone
        self.left_menu = left_menu
        self.memory_clean = False
        self.count_inventory_full = 0
        self.pet_to_recycle = ReadINIFile(
            inc_path + '\\..\\setup.ini', 'Main', 'IHavePetWithBlacksmith', 'NO').lower()
        if self.pet_to_recycle == 'yes':
            self.pet_to_recycle = True
        else:
            self.pet_to_recycle = False

    def pause(self):
        self.paused = True

    def resume(self):
        self.paused = False

    def stop(self):
        self.stopped = True

    def checkIsNOTRunning(self):
        if self.paused is True or self.stopped is True:
            if self.memory_clean is True:
                gc.collect()
                self.memory_clean = False
            return True
        else:
            return False

    def run(self):
        while self.stopped is False:
            if self.checkIsNOTRunning() is True:
                time.sleep(0.5)
                continue
            try:
                self.memory_clean = True
                response = RunFindImage(self.src_window, self.img_path,
                                        'inventory_full_' + self.language, self.captureWorker.screenshot)
                if response['inventory_full_' + self.language] != 'notfound':
                    self.send_text_to_bot.send(
                        "Inventory is full", self.from_python, 'brown')
                    self.count_inventory_full += 1
                    # --------------------------------------------------
                    if self.checkIsNOTRunning() is True:
                        continue
                    self.threads.pause_all_threads(
                        ['Blacksmith', 'CaptureWorker', 'CheckIsDead', 'Fight'])
                    for i in range(5):
                        self.moveplayer.processing_movement_output('NK')
                        self.fight.checkFightIsRunning()
                        time.sleep(1)
                    self.fight.checkFightIsRunning()
                    if self.checkIsNOTRunning() is True:
                        continue
                    self.send_text_to_bot.send(
                        'Look like no monster is attacking now', self.from_python, 'green')
                    if self.pet_to_recycle is False:
                        self.moveplayer.GoToSafeZone(self.left_menu, self.spot_safe_zone)
                    self.fight.checkFightIsRunning()
                    self.send_text_to_bot.send(
                        'Waiting 5 seconds to check if any monster attack', self.from_python, 'purple')
                    for i in range(5):
                        time.sleep(1)
                        # self.moveplayer.processing_movement_output('NK')
                        self.fight.checkFightIsRunning()
                        self.send_text_to_bot.send(
                            'time left: ' + str(5 - i), self.from_python, 'purple')
                    self.fight.checkFightIsRunning()
                    if self.checkIsNOTRunning() is True:
                        continue
                    if self.goToBlacksmith() == False:
                        self.send_text_to_bot.send(
                            "Error going to blacksmith", self.from_python, 'red')
                        self.moveplayer.pressKey('esc')
                        time.sleep(2)
                        self.moveplayer.clickOnCoords((365, 358))
                        self.threads.runAgain()
                    else:
                        self.threads.pause_all_threads(
                            ['Blacksmith', 'CaptureWorker'])
                        if self.process_blacksmith_task() is False:
                            continue
                        # self.moveplayer.pressKey('f')
                        # count = 0
                        # runAgain = False
                        # if self.checkIsNOTRunning() is True:
                        #     continue
                        # while self.checkBlacksmithFeedback() is False:
                        #     time.sleep(1)
                        #     self.send_text_to_bot.send(
                        #         'Waiting to blacksmith button: ' + str(10 - count), self.from_python, 'purple')
                        #     count += 1
                        #     if count > 10:
                        #         runAgain = True
                        #         self.send_text_to_bot.send(
                        #             "Error waiting to blacksmith button", self.from_python, 'red')
                        #         self.moveplayer.clickOnCoords((676, 371))
                        #         break
                        # if runAgain is True:
                        #     self.threads.runAgain()
                        # else:
                        #     # click on feedback button 746, 370
                        #     self.moveplayer.clickOnCoords((746, 370))
                        #     time.sleep(1)
                        #     self.sellStuff()
                        #     self.count_inventory_full = 0
                        #     self.threads.runAgain()
                    # --------------------------------------------------
            except Exception as e:
                print(e)
                print("Error checking if inventory is full")
            time.sleep(0.5)

    def process_blacksmith_task(self, from_other_thread=False):
        self.moveplayer.pressKey('f')
        count = 0
        runAgain = False
        if from_other_thread is False:
            if self.checkIsNOTRunning():
                return False

        while not self.checkBlacksmithFeedback():
            time.sleep(1)
            count += 1
            runAgain = False
            self.send_text_to_bot.send('Waiting for blacksmith button: ' + str(10 - count), self.from_python, 'purple')
            if count > 10:
                runAgain = True
                self.send_text_to_bot.send("Error waiting for blacksmith button", self.from_python, 'red')
                self.moveplayer.clickOnCoords((676, 371))
                break

        if from_other_thread is False:
            if runAgain:
                self.threads.runAgain()
            else:
                self.moveplayer.clickOnCoords((746, 370))
                time.sleep(1)
                self.sellStuff()
                self.count_inventory_full = 0
                self.threads.runAgain()
        else:
            if runAgain:
                return False
            else:
                self.moveplayer.clickOnCoords((746, 370))
                time.sleep(1)
                self.sellStuff()
                self.count_inventory_full = 0
                return True

    def checkInBlacksmithScreen(self):
        response = RunFindImage(
            self.src_window, self.img_path, 'blacksmith_screen_' + self.language, self.captureWorker.screenshot)
        if 'notfound' in response:
            return False
        else:
            return True

    def checkBlacksmithFeedback(self):
        response = RunFindImage(
            self.src_window, self.img_path, 'bs_button1_' + self.language, self.captureWorker.screenshot)
        response2 = RunFindImage(
            self.src_window, self.img_path, 'bs_button2_' + self.language, self.captureWorker.screenshot)
        if response['bs_button1_' + self.language] == 'notfound' and response2['bs_button2_' + self.language] == 'notfound':
            return False
        else:
            return True

    def goToBlacksmith(self, from_other_thread=False):
        if self.pet_to_recycle is True:
            self.send_text_to_bot.send("Recycling pet", self.from_python, 'green')
            if self.moveplayer.openInventory() is False:
                self.send_text_to_bot.send("Error opening inventory", self.from_python, 'red')
                return False
            time.sleep(1)
            if self.moveplayer.foundPetIcon() is False:
                self.send_text_to_bot.send("Error finding pet icon", self.from_python, 'red')
                return False
            self.sellStuffByPet()
            return False
        self.send_text_to_bot.send("Going to blacksmith", self.from_python, 'green')
        if self.moveplayer.openMap(True) == False:
            self.send_text_to_bot.send("Error opening map", self.from_python, 'red')
            return False
        time.sleep(1)
        self.moveplayer.mouseMoveTo((144, 278))
        time.sleep(1)
        BSFoundIcon = False
        Fails = 0
        while BSFoundIcon is False:
            if Fails > 4:
                self.send_text_to_bot.send(
                    "We are stuck in the blacksmith", self.from_python, 'red')
                self.threads.resume_thread('CheckIsDead')
                return False
            response = RunFindImage(
                self.src_window, self.img_path + '\\..\\..\\mapLegend', 'blacksmith', self.captureWorker.screenshot)
            if response['blacksmith'] == 'notfound':
                self.moveplayer.mouseWheel(-150, 1) 
                time.sleep(1)
                Fails = Fails + 1
            else:
                print(response)
                PositionOFBS_x = response['blacksmith'].split('|')[0]
                PositionOFBS_y = response['blacksmith'].split('|')[1]
                BSFoundIcon = True
        # click on the blacksmithss
        self.moveplayer.clickOnCoords(
            (int(PositionOFBS_x), int(PositionOFBS_y)))
        time.sleep(1)
        # click on the teleport button
        self.moveplayer.clickOnNavigateOrTeleport()
        for i in range(3):
            time.sleep(1)
            self.send_text_to_bot.send(
                'Waiting to teleport to blacksmith: ' + str(3 - i), self.from_python, 'purple')
        if from_other_thread is False:
            if self.checkIsNOTRunning() is True:
                return False
        self.moveplayer.waitForTheArrivalToSpot()

        times_to_move = 0
        if self.move_to_blacksmith is not None:
            for i in range(60):
                if times_to_move < 6:
                    for elemento in self.move_to_blacksmith:
                        numero = elemento[0]
                        direccion = elemento[1]
                        self.moveplayer.manual_move(direccion, numero)
                        print('moving to blacksmith')
                        times_to_move += 1
                if self.moveplayer.checkIfPlayerIsNearTo('blacksmith'):
                    self.send_text_to_bot.send(
                        "Arrived to blacksmith", self.from_python, 'green')
                    break
                time.sleep(1)
                self.send_text_to_bot.send(
                    'Waiting to arrive to blacksmith: ' + str(60 - i), self.from_python, 'purple')
        else:
            if self.moveplayer.checkIfPlayerIsNearTo('blacksmith') is False:
                self.send_text_to_bot.send(
                    "Error arriving to blacksmith", self.from_python, 'red')
                return False
        return True

    def sellStuff(self):  
        time.sleep(3)
        response = RunFindImage(
            self.src_window, self.img_path, 'bs_button3_' + self.language, self.captureWorker.screenshot)
        if response['bs_button3_' + self.language] != 'notfound':
            self.moveplayer.clickOnCoords((394, 519))
            time.sleep(1)
            # YESS ALL --->
            self.moveplayer.clickOnCoords((528, 357))
            time.sleep(1)  
            # ---->      
            self.moveplayer.clickOnCoords((440, 520))
            time.sleep(1)
            # YESS ALL --->
            self.moveplayer.clickOnCoords((528, 357))
            time.sleep(1)  
            # ---->
            self.moveplayer.clickOnCoords((482, 519))
            time.sleep(3)
            # YESS ALL --->
            self.moveplayer.clickOnCoords((528, 357))
            time.sleep(1)
            # ---->
        print(response)
        self.send_text_to_bot.send(
            "Try to get stuff", self.from_python, 'yellow')
        self.getStuffElements()
        time.sleep(2)
        self.moveplayer.clickOnCoords((640, 510))
        time.sleep(3)
        self.moveplayer.pressKey('esc')
        time.sleep(1)

    def sellStuffByPet(self):
        # self.moveplayer.clickOnCoords((822, 525))
        # time.sleep(1)
        # self.moveplayer.clickOnCoords((870, 525))
        # time.sleep(1)
        # self.moveplayer.clickOnCoords((925, 525))
        time.sleep(3)
        self.send_text_to_bot.send(
            "Try to get stuff", self.from_python, 'yellow')
        self.getStuffElements()
        time.sleep(2)
        self.moveplayer.clickOnCoords((296, 505))
        time.sleep(3)
        self.moveplayer.pressKey('esc')
        time.sleep(1)

    def getStuffElements(self):
        yellow_dust_coords = self.moveplayer.founfIconInScreen(
            self.img_path + '\\..\\..\\game_items', 'yellow_dust', 0, False, self.captureWorker.screenshot, False, False, 0.95)
        scrap_coords = self.moveplayer.founfIconInScreen(
            self.img_path + '\\..\\..\\game_items', 'scrap', 0, False, self.captureWorker.screenshot, False, False, 0.95)
        if yellow_dust_coords != (0, 0):
            try:
                quantity_of_yellow_dust = self.moveplayer.getQuantityOfItem(yellow_dust_coords, 'yellow_dust')
                if int(quantity_of_yellow_dust) > 0:
                    self.send_text_to_bot.send(
                        "Yellow dust: " + str(quantity_of_yellow_dust), self.from_python, 'green')
                    self.send_text_to_bot.send(
                            'command|sendyellowdust|'+str(quantity_of_yellow_dust), self.from_python, False, True)
            except Exception as e:
                print(e)
                self.send_text_to_bot.send(
                    "Cant detect yellow dust", self.from_python, 'red')
        if scrap_coords != (0, 0):
            try:
                quantity_of_scrap = self.moveplayer.getQuantityOfItem(scrap_coords, 'scrap')
                if int(quantity_of_scrap) > 0:
                    self.send_text_to_bot.send(
                        "Scrap: " + str(quantity_of_scrap), self.from_python, 'green')
                    self.send_text_to_bot.send(
                            'command|sendscrap|'+str(quantity_of_scrap), self.from_python, False, True)
            except Exception as e:
                print(e)
                self.send_text_to_bot.send(
                    "Cant detect scrap", self.from_python, 'red')