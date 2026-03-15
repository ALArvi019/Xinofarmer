import threading
import time
import random
from movePlayer import moveplayer
from readINI import ReadINIFile
from fishV2 import RunFishV2


class FishNewThread(threading.Thread):

    def __init__(self, threads, src_window, img_path, send_text_to_bot, from_python):
        threading.Thread.__init__(self)
        self.src_window = src_window
        self.img_path = img_path
        self.send_text_to_bot = send_text_to_bot
        self.from_python = from_python
        self.threads = threads
        self.stopped = False
        self.paused = False
        self.moveplayer = None
        self.blacksmith = None
        self.checkLoot = None
        self.captureWorker = None
        self.figth = None
        self.timeTolastInvCheck = None
        self.timeTolastBuyBait = None
        self.fish_zone = ReadINIFile(
            img_path + '\\..\\..\\setup.ini', 'Fish2', 'Zones', 'random').lower()
        self.mapName = ReadINIFile(
            img_path + '\\..\\..\\setup.ini', 'Fish2', 'Maps', 'Bilefen').lower()
        self.fish_type = ReadINIFile(
            img_path + '\\..\\..\\setup.ini', 'Fish2', 'Fish2Type', 'Gold').lower()
        self.total_fish_iterMin = int(ReadINIFile(
            img_path + '\\..\\..\\setup.ini', 'Fish2', 'Fish2_IterMin', 10))
        self.total_fish_iterMax = int(ReadINIFile(
            img_path + '\\..\\..\\setup.ini', 'Fish2', 'Fish2_IterMax', 10))
        self.CheckInventoryPercent = int(ReadINIFile(
            img_path + '\\..\\..\\setup.ini', 'Fish2', 'CHeckInventoryPercent', 40))
        self.SecondsToTurnLoot = int(ReadINIFile(
            img_path + '\\..\\..\\setup.ini', 'Fish2', 'roundcicles', 3))
        if self.fish_type == 'gold':
            self.timeFish = 155
        elif self.fish_type == 'epic':
            self.timeFish = 243
        elif self.fish_type == 'legendary':
            self.timeFish = 203
        elif self.fish_type == 'blue':
            self.timeFish = 63
        elif self.fish_type == 'white':
            self.timeFish = 5
        self.fish_root_data = {
            'bilefen': {
                'bridge1': {
                    'name': 'bridge1',
                    'left_menu_image': None,
                    'spot_coords': None,
                    'drag_mouse': None,
                    'near_fisherman': True,
                    'near_fisherman_move': '↙',
                    'fish_zone_random_movements': None
                },
                'bridge2': {
                    'name': 'bridge2',
                    'left_menu_image': 'port_justinian',
                    'spot_coords': [(577, 419),(566, 408)],
                    'drag_mouse': None,
                    'near_fisherman': False,
                    'near_fisherman_move': False,
                    'fish_zone_random_movements': ['↗', '↘', '↙']
                },
                'bridge3': {
                    'name': 'bridge3',
                    'left_menu_image': 'port_justinian',
                    'spot_coords': [(742, 260),(743, 270)],
                    'drag_mouse': [
                        {"initial_position": (561, 105), "final_position": (561, 433)},
                    ],
                    'near_fisherman': False,
                    'near_fisherman_move': False,
                    'fish_zone_random_movements': ['↗', '↙']
                },
                'bridge4': {
                    'name': 'bridge4',
                    'left_menu_image': 'port_justinian',
                    'spot_coords': [(573, 403)],
                    'drag_mouse': [
                        {"initial_position": (701, 521), "final_position": (443, 268)},
                    ],
                    'near_fisherman': False,
                    'near_fisherman_move': False,
                    'fish_zone_random_movements': ['↗', '↙']
                },
                # 485, 472
            },
            'cementery': {
                'nearfisherman': {
                    'name': 'nearfisherman',
                    'left_menu_image': None,
                    'spot_coords': None,
                    'drag_mouse': None,
                    'near_fisherman': True,
                    'near_fisherman_move': '↗',
                    'fish_zone_random_movements': None
                },
                'bridge1': {
                    'name': 'bridge1',
                    'left_menu_image': 'guard_watch',
                    'spot_coords': [(635, 267),(660, 267),(670, 265)],
                    'drag_mouse': [
                        {"initial_position": (917, 277), "final_position": (657, 277)},
                    ],
                    'near_fisherman': False,
                    'near_fisherman_move': False,
                    'fish_zone_random_movements': ['↗', '↘', '↙']
                },
            },
            'thundra': {
                'bridge1': {
                    'name': 'nearfisherman',
                    'left_menu_image': None,
                    'spot_coords': None,
                    'drag_mouse': None,
                    'near_fisherman': True,
                    'near_fisherman_move': '↘',
                    'fish_zone_random_movements': None
                },
            }
        }

    def shuffleFishData(self):
        if self.fish_zone == 'random':
            keys = list(self.fish_root_data[self.mapName].keys())
            random.shuffle(keys)
            random_key = random.choice(keys)
            self.fish_data = self.fish_root_data[self.mapName][random_key]
        else:
            self.fish_data = self.fish_root_data[self.mapName][self.fish_zone]

    def pause(self):
        self.paused = True

    def stop(self):
        self.stopped = True

    def resume(self):
        self.paused = False

    def run(self):
        print("DEBUG: RunFishNew STARTED")
        while self.stopped is False:
            if self.paused is True:
                time.sleep(1)
                self.dead = True
                continue
            # try:
            if 1 == 1:

                try:
                    self.captureWorker = self.threads.create_thread(
                        'CaptureWorker', self.src_window, self.img_path)
                    self.threads.resume_thread('CaptureWorker')
                except Exception as e:
                    print(e)
                    print("Error running captureWorker")

                # wait to captureWorker have a captureWorker.screenshot property available
                while self.captureWorker.screenshot is None:
                    self.send_text_to_bot.send(
                        'Waiting for thread to start', self.from_python, 'blue')
                    time.sleep(1)

                self.moveplayer = moveplayer(
                    self.src_window, self.threads, self.img_path, 'en', self.send_text_to_bot, self.from_python)

                self.blacksmith = self.threads.create_thread(
                    'Blacksmith', self.threads, self.src_window, self.img_path + '\\en\\blacksmith', 'en', self.moveplayer, 'fishNew', self.img_path+"\\..", None, self.send_text_to_bot, self.from_python, None, None)

                checkPartyInvite = self.threads.create_thread(
                    'CheckPartyInvite', self.threads, self.src_window, False, 'en', self.img_path + '\\en\\farm', self.send_text_to_bot, self.from_python, 'CheckPartyInvite', self.moveplayer, False)
                self.threads.resume_thread('CheckPartyInvite')

                self.checkLoot = self.threads.create_thread(
                    'CheckLoot', self.threads, self.src_window, self.img_path + '\\en\\loot_items', self.send_text_to_bot, self.from_python, self.img_path, self.moveplayer, False, False, True)

                CheckDungeonLoot = self.threads.create_thread(
                    'CheckDungeonLoot', self.threads, self.src_window, self.send_text_to_bot, self.from_python, self.moveplayer, self.img_path)
                self.threads.resume_thread('CheckDungeonLoot')

                self.figth = self.threads.create_thread(
                    'Fight', self.threads, self.src_window, False, self.moveplayer, self.send_text_to_bot, self.from_python, False, self.img_path)
                self.figth.set_survivor_mode(True)
                self.threads.resume_thread('Fight')

                if self.moveplayer.checkIfPlayerIsNearTo('exit_fish') is True:
                    self.send_text_to_bot.send(
                        'Player is fishing NOW', self.from_python, 'red')
                    self.threads.pause_thread('Fight')
                    startFishActualTime = time.time()
                    response = self.catchFish(startFishActualTime)
                    continue
                # > 5 minutes
                if self.timeTolastInvCheck is None or time.time() - self.timeTolastInvCheck > 60 * 5:
                    if self.inventoryCheck() is False:
                        continue
                    self.timeTolastInvCheck = time.time()
                else:
                    self.send_text_to_bot.send(
                        'Next inventory check in ' + str(int(60 * 5 - (time.time() - self.timeTolastInvCheck))) + ' seconds', self.from_python, 'blue')
                # > 5 minutes
                if self.timeTolastBuyBait is None or time.time() - self.timeTolastBuyBait > 60 * 5:
                    if self.buyBaitAndSell() is False:
                        continue
                    self.timeTolastBuyBait = time.time()
                else:
                    self.send_text_to_bot.send(
                        'Next buy bait in ' + str(int(60 * 5 - (time.time() - self.timeTolastBuyBait))) + ' seconds', self.from_python, 'blue')
                if self.goToFish() is False:
                    continue
                if self.startFish() is False:
                    continue

            # except Exception as e:
            #     print(e)
            #     # pritn in red
            #     print("\033[91m" + "DEBUG: RunFishNew ERROR" + "\033[0m")

            # ----------------------------------------------------------------
            # print("\033[91m" + "DEBUG: RunFishNew STOPPED" + "\033[0m")
            # # stop all threads
            # self.threads.stop_all_threads()
            # # exit script
            # exit()
            # ----------------------------------------------------------------
            # self.paused = True
        time.sleep(1)

    def reboot(self):
        self.stopped = False
        self.paused = False
        self.run()

    def inventoryCheck(self):
        needToCheckInventory = self.moveplayer.checkInventory(self.CheckInventoryPercent)
        if needToCheckInventory is True:
            self.send_text_to_bot.send(
                'Need to check inventory', self.from_python, 'blue')
            if self.blacksmith.goToBlacksmith(True) is False:
                self.send_text_to_bot.send(
                    "Error going to blacksmith", self.from_python, 'red')
                self.moveplayer.pressKey('esc')
                time.sleep(2)
                self.moveplayer.clickOnCoords((365, 358))
                return False
            else:
                if self.blacksmith.process_blacksmith_task(True) is False:
                    self.send_text_to_bot.send(
                        "Error processing blacksmith task", self.from_python, 'red')
                    self.moveplayer.pressKey('esc')
                    time.sleep(2)
                    self.moveplayer.clickOnCoords((365, 358))
                    return False
        else:
            self.send_text_to_bot.send(
                'No need to check inventory', self.from_python, 'blue')
        return True

    def buyBaitAndSell(self):
        # going to fisherman
        if self.moveplayer.goToFisherman() is False:
            self.send_text_to_bot.send(
                "Error going to fisherman", self.from_python, 'red')
            self.moveplayer.pressKey('esc')
            time.sleep(2)
            self.moveplayer.clickOnCoords((365, 358))
            return False
        else:
            # buying bait
            self.figth.checkFightIsRunning(5,False)
            self.send_text_to_bot.send('Buying bait', self.from_python, 'blue')
            if self.moveplayer.buyBait() is False:
                self.send_text_to_bot.send(
                    "Error buying bait", self.from_python, 'red')
                self.moveplayer.pressKey('esc')
                time.sleep(2)
                self.moveplayer.clickOnCoords((365, 358))
                return False
            else:
                # sell fish
                self.figth.checkFightIsRunning(5,False)
                self.send_text_to_bot.send(
                    'Selling fish', self.from_python, 'blue')
                if self.moveplayer.sellFish(self.SecondsToTurnLoot) is False:
                    self.send_text_to_bot.send(
                        "Error selling fish", self.from_python, 'red')
                    self.moveplayer.pressKey('esc')
                    time.sleep(2)
                    self.moveplayer.clickOnCoords((365, 358))
                    return False
        return True

    def goToFish(self):
        # going to fish
        self.figth.checkFightIsRunning(5,False)
        self.send_text_to_bot.send('Going to fish', self.from_python, 'blue')
        self.shuffleFishData()
        self.moveplayer.goToFish(self.fish_data)

    def startFish(self):
        actualIter = 1
        self.figth.checkFightIsRunning(5,False)
        if self.total_fish_iterMin == self.total_fish_iterMax:
            self.total_fish_iter = self.total_fish_iterMin
        else:
            self.total_fish_iter = random.randint(
                self.total_fish_iterMin, self.total_fish_iterMax)
        while actualIter <= self.total_fish_iter:
            self.send_text_to_bot.send(
                            'command|sendactualiter|'+str('('+str(actualIter)+'/'+str(self.total_fish_iter)+')'), self.from_python, False, True)
            while self.moveplayer.checkIfPlayerIsNearTo('loot_hand_down') is True:
                    self.send_text_to_bot.send(
                    'Player is near to loot', self.from_python, 'blue')
                    self.moveplayer.pressKey('f')
                    time.sleep(1)
            if self.moveplayer.checkIfPlayerIsNearTo('fishzone') is False:
                self.send_text_to_bot.send(
                    'Player is not near to fish zone2', self.from_python, 'red')
                self.timeTolastBuyBait -= 300
                return False
            self.threads.pause_thread('Fight')
            self.moveplayer.pressKey('f')
            launchRodActualTime = time.time()
            for i in range(0, 5):
                self.send_text_to_bot.send(
                    'Waiting for fishing gui: ' + str(5 - i), self.from_python, 'blue')
                time.sleep(1)
            if self.moveplayer.checkIfPlayerIsNearTo('exit_fish') is False:
                self.send_text_to_bot.send(
                    'Player is not near to fish zone3', self.from_python, 'red')
                return False
            timeLeft = None
            while time.time() - launchRodActualTime < self.timeFish:
                timeLeft = self.timeFish - (time.time() - launchRodActualTime)
                self.send_text_to_bot.send(
                    'Time left: ' + str(int(timeLeft)), self.from_python, 'blue')
                time.sleep(1)
                if self.stopped is True:
                    return False
                if self.paused is True:
                    return False

            startFishActualTime = time.time()
            response = self.catchFish(startFishActualTime)
            time.sleep(2)
            if response == 'failed':
                return False
            if response == 'found':
                self.send_text_to_bot.send(
                    'Fish found', self.from_python, 'green')
                self.send_text_to_bot.send(
                    'Iter ' + str(actualIter) + ' of ' + str(self.total_fish_iter), self.from_python, 'blue')
                actualIter += 1
            while self.moveplayer.checkIfPlayerIsNearTo('loot_hand_down') is True:
                    self.send_text_to_bot.send(
                    'Player is near to loot', self.from_python, 'blue')
                    self.moveplayer.pressKey('f')
                    time.sleep(1)
                
        # sum 300 seconds to self.timeTolastInvCheck and self.timeTolastBuyBait to force check inventory and buy bait after all iters
        self.timeTolastInvCheck -= 300
        self.timeTolastBuyBait = 300

    def catchFish(self, startFishActualTime):
            coords_fish_action = self.moveplayer.founfIconInScreen(
                self.img_path + '\\fishing', 'fish_action', 0, False, self.captureWorker.screenshot, False, False, 0.88)
            # esperando como maximo 90 segundos a que aparezca el icono de pescar
            self.send_text_to_bot.send(
                'Waiting for fish icon for max 90 seconds', self.from_python, 'blue')
            while coords_fish_action == (0, 0):
                if time.time() - startFishActualTime > 90:
                    self.send_text_to_bot.send(
                        'Too much time waiting for fish icon', self.from_python, 'red')
                    return False
                time.sleep(1)
                self.send_text_to_bot.send(
                        'Waiting for fish icon, time left: ' + str(int(90 - (time.time() - startFishActualTime))), self.from_python, 'blue')
                if self.stopped is True:
                    return False
                if self.paused is True:
                    return False
                coords_fish_action = self.moveplayer.founfIconInScreen(
                    self.img_path + '\\fishing', 'fish_action', 0, False, self.captureWorker.screenshot, False, False, 0.88)
            self.send_text_to_bot.send(
                'Fish icon found', self.from_python, 'green')
            self.moveplayer.clickOnCoords(coords_fish_action)
            return RunFishV2(self.captureWorker, self.img_path + '\\fishing', self.fish_type, self.src_window)