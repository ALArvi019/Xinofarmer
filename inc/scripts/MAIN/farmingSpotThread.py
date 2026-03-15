import threading
import time
from movePlayer import moveplayer
from findImage import RunFindImage

class FarmingSpotThread(threading.Thread):

    def __init__(self, threads, src_window, inc_path, fileName, send_text_to_bot, from_python, language, acceptPartyInvite, ranged, dead, telegramConfig, username, spot_coords, skills_means, checkPartyLeader, checkBestyaryEveryIfNotification, checkBestyaryEveryIfNotificationNotFound, modelname):
        threading.Thread.__init__(self)
        self.src_window = src_window
        self.inc_path = inc_path
        self.fileName = fileName
        self.send_text_to_bot = send_text_to_bot
        self.from_python = from_python
        self.language = language
        self.acceptPartyInvite = acceptPartyInvite
        self.ranged = ranged
        self.dead = dead
        self.telegramConfig = telegramConfig
        self.username = username
        self.spot_coords = spot_coords
        self.threads = threads
        self.skills_means = skills_means
        self.stopped = False
        self.paused = False
        self.checkPartyLeader = checkPartyLeader
        self.checkBestyaryEveryIfNotification = checkBestyaryEveryIfNotification
        self.checkBestyaryEveryIfNotificationNotFound = checkBestyaryEveryIfNotificationNotFound
        self.modelname = modelname

    def pause(self):
        self.paused = True

    def stop(self):
        self.stopped = True

    def resume(self):
        self.paused = False

    def run(self):
        print("DEBUG: FarmingSpotThread started")
        print("DEBUG: self.stopped: " + str(self.stopped))
        print("DEBUG: self.paused: " + str(self.paused))
        while self.stopped is False:
            if self.paused is True:
                time.sleep(1)
                self.dead = True
                continue
            if True:
            # try:
                src_window = self.src_window
                inc_path = self.inc_path
                fileName = self.fileName
                send_text_to_bot = self.send_text_to_bot
                from_python = self.from_python
                language = self.language
                acceptPartyInvite = self.acceptPartyInvite
                ranged = self.ranged
                dead = self.dead
                telegramConfig = self.telegramConfig
                username = self.username
                spot_coords = self.spot_coords
                threads = self.threads
                skills_means = self.skills_means
                checkPartyLeader = self.checkPartyLeader
                checkBestyaryEveryIfNotification = self.checkBestyaryEveryIfNotification
                checkBestyaryEveryIfNotificationNotFound = self.checkBestyaryEveryIfNotificationNotFound
                modelname = self.modelname
                if modelname is None:
                    modelname = 'default'
                    self.modelname = modelname

                if modelname != 'default':
                    fileName = 'custom_model'

                send_text_to_bot.send("Running Farming Spot RUN", from_python)
                img_path = inc_path + '\\img'
                loot_path = img_path + '\\'+language+'\\loot_items'
                img_blacksmith_path = img_path + '\\'+language+'\\blacksmith'
                img_farm_path = img_path + '\\'+language+'\\farm'
                move_to_blacksmith = spot_coords[fileName]['move_to_blacksmith']
                move_to_bestiary = spot_coords[fileName]['move_to_bestiary']
                rectangle = spot_coords[fileName]['rectangle']
                timeToWait = spot_coords[fileName]['time_to_wait']
                left_menu = spot_coords[fileName]['left_menu']
                spot_safe_zone = spot_coords[fileName]['spot_safe_zone']
                left_menu_safe_zone = spot_coords[fileName]['left_menu_safe_zone']
                stuck_average = spot_coords[fileName]['stuck_average']

                try:
                    captureWorker = threads.create_thread(
                        'CaptureWorker', src_window, img_path)
                    threads.resume_thread('CaptureWorker')  
                except Exception as e:
                    print(e)
                    print("Error running captureWorker")

                if threads.get_thread('CustomSocketIO') is None:
                    customsocketio = threads.create_thread(
                        'CustomSocketIO', send_text_to_bot, from_python, username)
                    threads.resume_thread('CustomSocketIO')

                OrchestratorThread = threads.create_thread('OrchestratorThread', threads)
                threads.resume_thread('OrchestratorThread')

                Moveplayer = moveplayer(src_window, threads, img_path, language,send_text_to_bot, from_python)

                threads.moveplayer = Moveplayer

                if self.telegramConfig:
                    checkmessages = threads.create_thread(
                        'CheckMessages', threads, src_window, telegramConfig, username, send_text_to_bot, from_python, img_path, Moveplayer, language)
                
                checkisdead = threads.create_thread(
                    'CheckIsDead', threads, src_window, send_text_to_bot, from_python, Moveplayer, language, img_path)
                
                checklife = threads.create_thread(
                    'CheckLife', threads, Moveplayer, send_text_to_bot, from_python, img_path)
                
                fight = threads.create_thread(
                    'Fight', threads, skills_means, ranged, Moveplayer, send_text_to_bot, from_python, False, img_path)
                
                spotWorker = threads.create_thread(
                    'SpotWorker', threads, src_window, img_path, fileName, inc_path, send_text_to_bot, from_python, rectangle, Moveplayer, stuck_average, modelname)
                
                checkLoot = threads.create_thread(
                    'CheckLoot', threads, src_window, loot_path, send_text_to_bot, from_python, img_path, Moveplayer, False)
                
                blacksmith = threads.create_thread(
                    'Blacksmith', threads, src_window, img_blacksmith_path, language, Moveplayer, fileName, inc_path, move_to_blacksmith, send_text_to_bot, from_python, left_menu_safe_zone, spot_safe_zone)
                
                checkessences = threads.create_thread(
                    'CheckEssences', threads, src_window, img_path, send_text_to_bot, from_python, Moveplayer, inc_path, fileName, language, move_to_bestiary, left_menu_safe_zone, spot_safe_zone, checkBestyaryEveryIfNotification, checkBestyaryEveryIfNotificationNotFound)
                
                checkparty = threads.create_thread(
                    'CheckPartyInvite', threads, src_window, acceptPartyInvite, language, img_farm_path, send_text_to_bot, from_python, fileName, Moveplayer, checkPartyLeader)
                
                if modelname == 'default':
                    cheackactualmap = threads.create_thread(
                        'CheckActualMap', threads, src_window, send_text_to_bot, from_python, img_path, fileName, 10, 120)
                
                # before run threads, check if player is dead to go to spot site
                gotoSpot = False
                if dead and spot_coords[fileName]['go_to_spot'] is True:
                    continuerun = True
                    if Moveplayer.openMap(True) == False:
                        send_text_to_bot.send("Error opening map", from_python)
                        continuerun = False
                    if continuerun:
                        time.sleep(1)
                        Moveplayer.clickOnCoords(spot_coords[fileName]['left_menu'])
                        time.sleep(1)
                        # close left menu
                        Moveplayer.clickOnCoords((832, 543))
                        time.sleep(1)
                        # 509, 142
                        Moveplayer.clickOnCoords((509, 142))
                        time.sleep(1)
                        Moveplayer.clickOnCoords(spot_coords[fileName]['map_position'])
                        time.sleep(1)
                        if Moveplayer.clickOnNavigateOrTeleport(spot_coords[fileName]['map_position']) is False:
                            continue
                        Moveplayer.clickOnCoords(
                            (spot_coords[fileName]['map_position'][0], spot_coords[fileName]['map_position'][1] - 50))
                        threads.resume_thread('Fight')
                        while timeToWait > 0:
                            send_text_to_bot.send(
                                "Waiting to arrive to spot: " + str(timeToWait) + " seconds", from_python)
                            time.sleep(1)
                            timeToWait -= 1
                        gotoSpot = True

                threads.resume_thread('Fight')

                if gotoSpot:
                    Moveplayer.waitForTheArrivalToSpot()
                    checkLoot.in_SPOT = True
                else:
                    checkLoot.in_SPOT = True

                if self.paused:
                    continue

                    # star spot thread worker
                threads.resume_thread('CheckMessages')
                threads.resume_thread('CheckIsDead')
                threads.resume_thread('CheckLife')
                threads.resume_thread('Fight')
                threads.resume_thread('SpotWorker')
                threads.resume_thread('CheckLoot')
                threads.resume_thread('Blacksmith')
                threads.resume_thread('CheckEssences')
                threads.resume_thread('CheckPartyInvite')
                threads.resume_thread('CheckActualMap')
                self.paused = True

            # except Exception as e:
            #     print(e)
            #     print("Error running spot")
            #     send_text_to_bot.send('Error running spot, wait 5 seconds to retry', from_python)
            #     time.sleep(5)
        time.sleep(1)

    def reboot(self):
        self.stopped = False
        self.paused = False
        self.run()