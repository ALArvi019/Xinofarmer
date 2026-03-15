import threading
import time
from findImage import RunFindImage
import gc


class CheckEssences(threading.Thread):
    def __init__(self, threads, src_window, img_path, send_text_to_bot, from_python, Moveplayer, inc_path, fileName, language, move_to_bestiary, left_menu, spot_safe_zone, checkBestyaryEveryIfNotification=10, checkBestyaryEveryIfNotificationNotFound=120):
        threading.Thread.__init__(self)
        self.moveplayer = Moveplayer
        self.stopped = False
        self.paused = False
        self.captureWorker = threads.get_thread('CaptureWorker')
        self.src_window = src_window
        self.img_path = img_path
        self.send_text_to_bot = send_text_to_bot
        self.from_python = from_python
        self.threads = threads
        self.fight = threads.get_thread('Fight')
        self.already_in_safe_zone = False
        self.inc_path = inc_path
        self.fileName = fileName
        self.language = language
        self.checkLoot = threads.get_thread('CheckLoot')
        self.move_to_bestiary = move_to_bestiary
        self.left_menu = left_menu
        self.spot_safe_zone = spot_safe_zone
        self.blacksmith = threads.get_thread('Blacksmith')
        self.memory_clean = False
        self.checkisdead = threads.get_thread('CheckIsDead')
        self.need_to_go_to_bestiary = False
        self.already_check_bestiary = True
        self.checkBestyaryEveryIfNotification = int(checkBestyaryEveryIfNotification)
        self.checkBestyaryEveryIfNotificationNotFound = int(checkBestyaryEveryIfNotificationNotFound)

    def pause(self):
        self.paused = True

    def stop(self):
        self.stopped = True

    def resume(self):
        self.paused = False

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
                if self.checkisdead.player_is_dead is False:
                    self.send_text_to_bot.send(
                        "Checking bestiary NOW", self.from_python, 'brown')
                    self.blacksmith.pause()
                    if self.need_to_go_to_bestiary is True:
                        self.gotoBestiaryManual()
                    else:
                        self.checkLeftMenuEssences()
                    self.blacksmith.resume()
                else:
                    self.send_text_to_bot.send(
                        "We can't check the bestiary, the player is dead", self.from_python, 'red')
                self.already_in_safe_zone = False
            except Exception as e:
                print(e)
                print("Error checking essences")
            if self.already_check_bestiary:
                self.send_text_to_bot.send(
                        "Checking bestiary in " + str(self.checkBestyaryEveryIfNotificationNotFound) + " sec", self.from_python, 'brown')
                time.sleep(self.checkBestyaryEveryIfNotificationNotFound)
            else:
                self.send_text_to_bot.send(
                        "Checking bestiary every " + str(self.checkBestyaryEveryIfNotification) + " sec", self.from_python, 'brown')
                time.sleep(self.checkBestyaryEveryIfNotification)

    def checkLeftMenuEssences(self):
        # CKECK LEFT MENU ICON NOTIFICATION
        response = RunFindImage(
            self.src_window, self.img_path + '\\game_items', 'notifications', self.captureWorker.screenshot)
        if response['notifications'] == 'notfound':
            self.already_check_bestiary = True
            return False
        else:
            self.send_text_to_bot.send(
                "Left notification found", self.from_python, 'brown')
            self.send_text_to_bot.send(
                "we need check bestiary", self.from_python, 'brown')
            # CHECK AGAIN IF NOTIFICATION IS STILL THERE
            response = RunFindImage(
                self.src_window, self.img_path + '\\game_items', 'notifications', self.captureWorker.screenshot)
            if response['notifications'] == 'notfound':
                self.send_text_to_bot.send(
                    "Left notification FALSE POSITIVE CONTINUE", self.from_python, 'brown')
                self.already_check_bestiary = True
                return False
            else:
                self.already_check_bestiary = False
                if self.checkIsNOTRunning() is True:
                    return
                self.threads.pause_all_threads(
                    ['CheckEssences', 'CaptureWorker', 'CheckIsDead', 'Fight'])
                self.moveplayer.processing_movement_output('NK')
                for i in range(5):
                    self.send_text_to_bot.send(
                        'time left to continue: ' + str(5 - i), self.from_python, 'purple')
                    self.moveplayer.processing_movement_output('NK')
                    self.fight.checkFightIsRunning(5, False)
                    time.sleep(1)
                self.fight.checkFightIsRunning()
                if self.checkIsNOTRunning() is True:
                    return
                self.send_text_to_bot.send(
                    'Look like no monster is attacking now', self.from_python, 'green')
                # CLICK IN NOTIFICATION ICON AND DELETE X ICONS
                PositionOFBS_x = response['notifications'].split('|')[0]
                PositionOFBS_y = response['notifications'].split('|')[1]
                self.moveplayer.clickOnCoords(
                    (int(PositionOFBS_x), int(PositionOFBS_y)))
                self.send_text_to_bot.send(
                    "Left notification clicked", self.from_python, 'brown')
                time.sleep(1)
                response = RunFindImage(
                    self.src_window, self.img_path + '\\game_items', 'x_icon')
                while response['x_icon'] != 'notfound':
                    self.moveplayer.processing_movement_output('NK')
                    self.send_text_to_bot.send(
                        "X icon found", self.from_python, 'green')
                    Position_xicon_x = response['x_icon'].split('|')[0]
                    Position_xicon_y = response['x_icon'].split('|')[1]
                    self.moveplayer.clickOnCoords(
                        (int(Position_xicon_x), int(Position_xicon_y)))
                    self.send_text_to_bot.send(
                        "X icon clicked", self.from_python, 'green')
                    time.sleep(2)
                    response = RunFindImage(
                        self.src_window, self.img_path + '\\game_items', 'x_icon')
                if self.checkIsNOTRunning() is True:
                    return
                self.moveplayer.processing_movement_output('NK')
                time.sleep(2)
                self.moveplayer.processing_movement_output('NK')
                # CHECK IF ESSENCE IS READY TO GRAB
                if self.checkEssenceInMenu(PositionOFBS_x, PositionOFBS_y):
                    self.goToBestiaryMasterFunction()
                else:
                    self.send_text_to_bot.send(
                        "Essence not found, continue", self.from_python, 'red')
                    self.threads.resume_all_threads()
                    return False
                
    def gotoBestiaryManual(self):
        self.send_text_to_bot.send('Bestiary already checked', self.from_python, 'brown')
        self.threads.pause_all_threads(
                    ['CheckEssences', 'CaptureWorker', 'CheckIsDead', 'Fight'])
        self.moveplayer.processing_movement_output('NK')
        time.sleep(2)
        self.moveplayer.processing_movement_output('NK')
        for i in range(5):
            self.fight.checkFightIsRunning()
            self.threads.pause_all_threads(
                    ['CheckEssences', 'CaptureWorker', 'CheckIsDead', 'Fight'])
            self.send_text_to_bot.send(
                 'time left: ' + str(5 - i), self.from_python, 'purple')
            time.sleep(1)
        if self.checkIsNOTRunning() is True:
            return
        self.moveplayer.processing_movement_output('NK')
        self.send_text_to_bot.send("Going to bestiary", self.from_python, 'green')
        if self.moveplayer.openMap(True) == False:
            self.send_text_to_bot.send("Error opening map", self.from_python, 'red')
            return False
        time.sleep(1)
        if self.checkIsNOTRunning() is True:
            return
        self.moveplayer.mouseMoveTo((144, 278))
        time.sleep(1)
        BSFoundIcon = False
        Fails = 0
        while BSFoundIcon is False:
            if self.checkIsNOTRunning() is True:
                return
            if Fails > 4:
                self.send_text_to_bot.send(
                    "We are stuck in the bestiary", self.from_python, 'red')
                self.threads.resume_thread('CheckIsDead')
                return False
            response = RunFindImage(
                self.src_window, self.img_path + '\\mapLegend', 'horadric')
            if response['horadric'] == 'notfound':
                self.moveplayer.mouseWheel(-150, 1) 
                time.sleep(1)
                Fails = Fails + 1
            else:
                print(response)
                PositionOFBS_x = response['horadric'].split('|')[0]
                PositionOFBS_y = response['horadric'].split('|')[1]
                BSFoundIcon = True
        # click on the horadric
        self.moveplayer.clickOnCoords(
            (int(PositionOFBS_x), int(PositionOFBS_y)))
        time.sleep(1)
        # click on the teleport button
        self.moveplayer.clickOnNavigateOrTeleport()
        self.goToBestiaryMasterFunction()

    def goToBestiaryMasterFunction(self):
        self.need_to_go_to_bestiary = True
        if self.goToBestiary():
            self.moveplayer.pressKey('f')
            for i in range(20):
                time.sleep(1)
                self.send_text_to_bot.send(
                    'Waiting to check bestiary: ' + str(20 - i), self.from_python, 'purple')
            if self.checkIsNOTRunning() is True:
                return False
            self.moveplayer.pressKey('esc')
            time.sleep(2)
            self.moveplayer.clickOnCoords((365, 358))
            time.sleep(2)
            if self.checkIsNOTRunning() is True:
                return False
            response = RunFindImage(
                self.src_window, self.img_path + '\\game_items', 'hand_down')
            while response['hand_down'] != 'notfound':
                self.moveplayer.pressKey('f')
                time.sleep(1)
                response = RunFindImage(
                    self.src_window, self.img_path + '\\game_items', 'hand_down')
            time.sleep(2)
            response = RunFindImage(
                self.src_window, self.img_path + '\\game_items', 'hand_down', self.captureWorker.screenshot)
            while response['hand_down'] != 'notfound':
                self.moveplayer.pressKey('f')
                time.sleep(1)
                response = RunFindImage(
                    self.src_window, self.img_path + '\\game_items', 'hand_down')
            # self.moveplayer.MoveRandomly()
            self.moveplayer.processing_movement_output('NK')
            self.checkLoot.in_SPOT = False
            self.checkLoot.in_BESTIARY = True
            self.threads.resume_thread('CheckLoot')
            self.threads.pause_all_threads(
                ['CheckEssences', 'CaptureWorker', 'CheckLoot'])
            for i in range(10):
                self.threads.resume_thread('CheckLoot')
                response = RunFindImage(
                    self.src_window, self.img_path + '\\' + self.language + '\\' + 'farm', 'bestiary_screen_' + self.language, self.captureWorker.screenshot)
                if response['bestiary_screen_' + self.language] != 'notfound':
                    self.send_text_to_bot.send(
                        'Exit bestiary', self.from_python, 'green')
                    self.moveplayer.clickOnCoords((924, 58))
                    time.sleep(5)
                self.send_text_to_bot.send(
                    'Waiting to check loot: ' + str(10 - i), self.from_python, 'purple')
                time.sleep(1)
                self.threads.resume_thread('CheckLoot')
            if self.checkIsNOTRunning() is True:
                return False
            self.need_to_go_to_bestiary = False
        self.moveplayer.MoveRandomly()
        self.threads.runAgain()
        return True

    def checkEssenceInMenu(self, PositionOFBS_x, PositionOFBS_y):
        response = RunFindImage(
            self.src_window, self.img_path + '\\game_items', 'bestiary')
        if response['bestiary'] == 'notfound':
            print("bestiary not found")
            return False
        else:
            self.threads.pause_all_threads(
                ['CheckEssences', 'CaptureWorker', 'CheckIsDead', 'Fight'])
            # self.moveplayer.clickOnCoords(
            #     (int(PositionOFBS_x), int(PositionOFBS_y)))
            time.sleep(2)
            # IF ESSENCE IS READY TO GRAB, GO TO SAFE ZONE

            response = RunFindImage(
                self.src_window, self.img_path + '\\game_items', 'bestiary', self.captureWorker.screenshot)
            if response['bestiary'] == 'notfound':
                print("bestiary not found")
                self.already_in_safe_zone = False
                return False
            else:
                if self.already_in_safe_zone is False:
                    if self.moveplayer.GoToSafeZone(self.left_menu, self.spot_safe_zone) is True:
                        self.already_in_safe_zone = True
                self.fight.checkFightIsRunning(5, False)
                if self.checkIsNOTRunning() is True:
                    return False
                self.send_text_to_bot.send(
                    'Waiting 5 seconds to check if any monster attack', self.from_python, 'purple')
                for i in range(5):
                    self.fight.checkFightIsRunning(5, False)
                    self.send_text_to_bot.send(
                        'time left: ' + str(5 - i), self.from_python, 'purple')
                    time.sleep(1)
                self.fight.checkFightIsRunning(5, False)
                time.sleep(1)

                # goToBlacksmith(True)
                self.threads.pause_thread('CheckLife')
                if self.blacksmith.goToBlacksmith(True) is False:
                    self.send_text_to_bot.send(
                            "Error going to blacksmith", self.from_python, 'red')
                    self.moveplayer.pressKey('esc')
                    time.sleep(2)
                    self.moveplayer.clickOnCoords((365, 358))
                else:
                    if self.blacksmith.process_blacksmith_task(True) is False:
                        self.send_text_to_bot.send(
                            "Error processing blacksmith task", self.from_python, 'red')
                        self.moveplayer.pressKey('esc')
                        time.sleep(2)
                        self.moveplayer.clickOnCoords((365, 358))
                self.send_text_to_bot.send(
                    "Delay 5 seconds before continue", self.from_python, 'yellow')
                self.moveplayer.clickOnCoords(
                    (int(PositionOFBS_x), int(PositionOFBS_y)))
                time.sleep(2)
                response = RunFindImage(
                self.src_window, self.img_path + '\\game_items', 'bestiary', self.captureWorker.screenshot)
                if response['bestiary'] == 'notfound':
                    print("bestiary not found")
                    self.already_in_safe_zone = False
                    return False
                bestiry_position_x = response['bestiary'].split('|')[0]
                bestiry_position_y = response['bestiary'].split('|')[1]
                self.moveplayer.clickOnCoords(
                    (int(bestiry_position_x), int(bestiry_position_y)))
                self.send_text_to_bot.send(
                    "Bestiary clicked", self.from_python, 'green')
                return True

    def goToBestiary(self):
        if self.checkIsNOTRunning() is True:
            return False
        self.threads.pause_all_threads(
            ['CheckEssences', 'CaptureWorker', 'CheckIsDead'])
        if self.checkIsNOTRunning() is True:
            return False
        self.moveplayer.waitForTheArrivalToSpot()
        if self.checkIsNOTRunning() is True:
            return False

        times_to_move = 0
        if self.move_to_bestiary is not None:
            for i in range(60):
                if times_to_move < 6:
                    for elemento in self.move_to_bestiary:
                        numero = elemento[0]
                        direccion = elemento[1]
                        self.moveplayer.manual_move(direccion, numero)
                        print("move to bestiary")
                        times_to_move += 1
                if self.moveplayer.checkIfPlayerIsNearTo('bestiary'):
                    self.send_text_to_bot.send(
                        "Arrived to bestiary", self.from_python, 'green')
                    break
                time.sleep(1)
                self.send_text_to_bot.send(
                    'Waiting to arrive to bestiary: ' + str(60 - i), self.from_python, 'purple')
        else:
            if self.checkIsNOTRunning() is True:
                return False
            if self.moveplayer.checkIfPlayerIsNearTo('bestiary') is False:
                self.send_text_to_bot.send(
                    "Error arriving to bestiary", self.from_python, 'red')
                return False
        return True
