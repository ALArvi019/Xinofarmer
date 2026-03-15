import threading
import time
from movePlayer import moveplayer
from readINI import ReadINIFile

class EndlessModeThread(threading.Thread):
    def __init__(self, threads, src_window, img_path, send_text_to_bot, from_python, language, telegramConfig, username, skills_means):
        threading.Thread.__init__(self)
        self.stopped = False
        self.paused = False
        self.src_window = src_window
        self.img_path = img_path
        self.send_text_to_bot = send_text_to_bot
        self.from_python = from_python
        self.language = language
        self.telegramConfig = telegramConfig
        self.username = username
        self.threads = threads
        self.skills_means = skills_means
        self.dead = False
        self.stay_at_the_door = ReadINIFile(
            img_path + '\\..\\..\\setup.ini', 'Cyrangar', 'StayAtTheDoor', 'No').lower()
        if self.stay_at_the_door == 'yes':
            self.stay_at_the_door = True
        else:
            self.stay_at_the_door = False
        self.cyrangar_over_time = ReadINIFile(
            img_path + '\\..\\..\\setup.ini', 'Cyrangar', 'Time_to_exit', '999').lower()
        self.cyrangar_over_time = int(self.cyrangar_over_time)
        self.get_fog_bane = ReadINIFile(
            img_path + '\\..\\..\\setup.ini', 'Cyrangar', 'get_fog_bane', 'Yes').lower()
        if self.get_fog_bane == 'yes':
            self.get_fog_bane = True
        else:
            self.get_fog_bane = False

        

    def pause(self):
        self.paused = True

    def stop(self):
        self.stopped = True

    def resume(self):
        self.paused = False

    def run(self):
        print("DEBUG: EndlessModeThread started")
        print("DEBUG: self.stopped: " + str(self.stopped))
        print("DEBUG: self.paused: " + str(self.paused))
        while self.stopped is False:
            if self.paused is True:
                time.sleep(1)
                
                continue
            try:

                # self.send_text_to_bot.send("Running Endless RUN", self.from_python)

                img_farm_path = self.img_path + '\\' + self.language + '\\farm'
                loot_path = self.img_path + '\\' + self.language + '\\loot_items'

                try:
                    captureWorker = self.threads.create_thread(
                        'CaptureWorker', self.src_window, self.img_path)
                    self.threads.resume_thread('CaptureWorker')  
                except Exception as e:
                    print(e)
                    print("Error running captureWorker")

                if self.threads.get_thread('CustomSocketIO') is None:
                    customsocketio = self.threads.create_thread(
                        'CustomSocketIO', self.send_text_to_bot, self.from_python, self.username)
                    self.threads.resume_thread('CustomSocketIO')

                Moveplayer = moveplayer(self.src_window, self.threads, self.img_path, self.language, self.send_text_to_bot, self.from_python)

                self.threads.moveplayer = Moveplayer

                if self.telegramConfig and 1==2:
                    checkmessages = self.threads.create_thread(
                        'CheckMessages', self.threads, self.src_window, self.telegramConfig, self.username, self.send_text_to_bot, self.from_python, self.img_path, Moveplayer, self.language)
                
                checkisdead = self.threads.create_thread(
                    'CheckIsDead', self.threads, self.src_window, self.send_text_to_bot, self.from_python, Moveplayer, self.language, self.img_path, True)
                
                checklife = self.threads.create_thread(
                    'CheckLife', self.threads, Moveplayer, self.send_text_to_bot, self.from_python, self.img_path)
                
                fight = self.threads.create_thread(
                    'Fight', self.threads, self.skills_means, False, Moveplayer, self.send_text_to_bot, self.from_python, True, self.img_path)
                
                checkCynangarEnd = self.threads.create_thread(
                    'CheckCyrangarEnd', self.threads, self.src_window, self.send_text_to_bot, self.from_python, Moveplayer, self.language, self.img_path)
                if self.dead == False:
                    checkCynangarEnd.tmp_cyrangar_over_time = self.cyrangar_over_time
                    checkCynangarEnd.last_check = time.time()
                self.dead = False

                if self.stay_at_the_door is False:
                    endlessmodeCHeckline = self.threads.create_thread(
                        'EndlessModeCheckLine', self.threads, self.src_window, self.send_text_to_bot, self.from_python, Moveplayer, self.img_path)
                    
                endlessmodeCheckDoor = self.threads.create_thread(
                        'EndlessModeChecDoorAttack', self.threads, self.src_window, self.send_text_to_bot, self.from_python, Moveplayer, self.img_path)
                
                if self.get_fog_bane:
                    checkLoot = self.threads.create_thread(
                            'CheckLoot', self.threads, self.src_window, loot_path, self.send_text_to_bot, self.from_python, self.img_path, Moveplayer, True)
                
                # checkparty = self.threads.create_thread(
                #     'CheckPartyInvite', self.threads, self.src_window, False, self.language, img_farm_path, self.send_text_to_bot, self.from_python, 'cynangar', Moveplayer, False, False)
            
                self.send_text_to_bot.send("Stay at the door: " + str(self.stay_at_the_door), self.from_python, 'blue')
                    # star spot thread worker
                self.threads.resume_thread('CheckMessages')
                self.threads.resume_thread('CheckIsDead')
                self.threads.resume_thread('CheckLife')
                self.threads.resume_thread('Fight')
                self.threads.resume_thread('SpotWorker')
                self.threads.resume_thread('CheckLoot')
                self.threads.resume_thread('CheckPartyInvite')
                self.threads.resume_thread('CheckCyrangarEnd')
                self.threads.resume_thread('EndlessModeCheckLine')
                self.threads.resume_thread('EndlessModeChecDoorAttack')
                self.paused = True
                # Moveplayer.manual_move('NorthEast', 2)

            except Exception as e:
                print(e)
                print("Error running spot")
                self.send_text_to_bot.send('Error running spot, wait 5 seconds to retry', self.from_python)
                time.sleep(5)
        time.sleep(1)

    def reboot(self):
        self.stopped = False
        self.paused = False
        self.run()