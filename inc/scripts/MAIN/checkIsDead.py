import threading
import time
import gc
from findImage import RunFindImage


class CheckIsDead(threading.Thread):
    def __init__(self, threads, src_window, send_text_to_bot, from_python, moveplayer, language, img_path, cyrangar=False, dungeon=False):
        threading.Thread.__init__(self)
        self.moveplayer = moveplayer
        self.stopped = False
        self.player_is_dead = False
        self.paused = False
        self.count_player_dead = 0
        self.send_text_to_bot = send_text_to_bot
        self.from_python = from_python
        self.threads = threads
        self.memory_clean = False
        self.captureWorker = threads.get_thread('CaptureWorker')
        self.rundungeon = threads.get_thread('RunDungeonThread')
        self.endlessthread = threads.get_thread('EndlessModeThread')
        self.language = language
        self.src_window = src_window
        self.img_path = img_path
        self.cyrangar = cyrangar
        self.dungeon = dungeon
        self.fight = None

    def pause(self):
        self.paused = True

    def resume(self):
        self.paused = False

    def run(self):
        while self.stopped is False:
            if self.paused is True:
                if self.memory_clean is True:
                    gc.collect()
                    self.memory_clean = False
                time.sleep(0.5)
                continue
            try:
                self.player_is_dead = False
                self.memory_clean = True
                if self.cyrangar is False:
                    checkPlayerIsDead = self.checkPlayerIsDead()
                    checkPlayerIsDeadAndRevive = self.checkPlayerIsDeadAndRevive()
                    checkPlayerIsDeadDungeon = self.checkPlayerIsDeadDungeon()
                    if checkPlayerIsDead is True or checkPlayerIsDeadAndRevive is True or checkPlayerIsDeadDungeon is True:
                        self.player_is_dead = True
                        self.threads.resume_thread('CheckIsDead')
                        if checkPlayerIsDeadDungeon is True:
                            self.threads.pause_all_threads(
                                ['CheckIsDead', 'CaptureWorker', 'Fight'])
                        else:
                            self.threads.pause_all_threads(
                                ['CheckIsDead', 'CaptureWorker'])
                        if checkPlayerIsDeadDungeon is True:
                            timetowait = 1
                        else:
                            timetowait = 10
                        for i in list(range(timetowait))[::-1]:
                            self.send_text_to_bot.send('Waiting ' + str(i + 1) + ' seconds to check if player is dead again',
                                                       self.from_python, 'pink')
                            time.sleep(1)
                        if self.checkPlayerIsDead() is True:
                            self.threads.pause_all_threads(
                                ['CheckIsDead', 'CaptureWorker'])
                            self.send_text_to_bot.send(
                                'Player is dead, reviving', self.from_python, 'pink')
                            self.revivePlayer()
                            self.player_is_dead = False
                            self.threads.runAgain()
                            continue
                        elif self.checkPlayerIsDeadAndRevive() is True:
                            self.threads.pause_all_threads(
                                ['CheckIsDead', 'CaptureWorker'])
                            self.send_text_to_bot.send(
                                'Player is dead, reviving', self.from_python, 'pink')
                            self.revivePlayerByPlayer()
                            self.player_is_dead = False
                            self.threads.runAgain()
                            continue
                        elif self.checkPlayerIsDeadDungeon() is True:
                            self.threads.pause_all_threads(
                                ['CheckIsDead', 'CaptureWorker'])
                            self.send_text_to_bot.send(
                                'Player is dead in dungeon, reviving', self.from_python, 'pink')
                            self.revivePlayerDungeon()
                            self.player_is_dead = False
                            self.rundungeon.go_to_dungeon = False
                            if self.fight is None:
                                self.fight = self.threads.get_thread('Fight')
                            self.fight.resumeSubThreads()
                            self.threads.runAgain('RunDungeonThread')
                            continue
                        else:
                            self.send_text_to_bot.send(
                                'Player is not dead, resuming', self.from_python, 'pink')
                            self.threads.resume_all_threads()
                else:
                    if self.checkPlayerIsDeadCyrangar() is True or self.checkPlayerIsDeadAndRevive() is True:
                        self.player_is_dead = True
                        self.threads.resume_thread('CheckIsDead')
                        self.threads.pause_all_threads(
                            ['CheckIsDead', 'CaptureWorker'])
                        time.sleep(1)
                        if self.checkPlayerIsDeadCyrangar() is True:
                            self.threads.pause_all_threads(
                                ['CheckIsDead', 'CaptureWorker'])
                            self.send_text_to_bot.send(
                                'Player is dead, reviving', self.from_python, 'pink')
                            while self.checkPlayerIsDeadCyrangar() is True:
                                self.revivePlayerCyrangar()
                                time.sleep(1)
                            self.player_is_dead = False
                            self.endlessthread.dead = True
                            self.threads.runAgain('EndlessModeThread')
                            continue
                        elif self.checkPlayerIsDeadAndRevive() is True:
                            self.threads.pause_all_threads(
                                ['CheckIsDead', 'CaptureWorker'])
                            self.send_text_to_bot.send(
                                'Player is dead, reviving', self.from_python, 'pink')
                            while self.checkPlayerIsDeadAndRevive() is True:
                                self.revivePlayerByPlayer()
                                time.sleep(1)
                            self.player_is_dead = False
                            self.threads.runAgain('EndlessModeThread')
                            continue
                        else:
                            self.send_text_to_bot.send(
                                'Player is not dead, resuming', self.from_python, 'pink')
                            self.threads.resume_all_threads()
                if self.checkIsDisconnected() is True:
                    self.player_is_dead = True
                    self.threads.resume_thread('CheckIsDead')
                    self.threads.pause_all_threads(
                        ['CheckIsDead', 'CaptureWorker'])
                    time.sleep(1)
                    if self.checkIsDisconnected() is True:
                        self.threads.pause_all_threads(
                            ['CheckIsDead', 'CaptureWorker'])
                        self.send_text_to_bot.send(
                            'Player is disconnected, reconnecting', self.from_python, 'pink')
                        while self.checkIsDisconnected() is True:
                            self.reconnect()
                            time.sleep(1)
                        self.player_is_dead = False
                        self.threads.runAgain()
                        continue

            except Exception as e:
                print(e)
                print("Error checking if player is dead")
                self.player_is_dead = False
            if self.cyrangar is True or self.dungeon is True:
                time.sleep(1)
            else:
                time.sleep(10)

    def checkPlayerIsDead(self):
        response = RunFindImage(
            self.src_window, self.img_path + '\game_items', 'dead_player_' + self.language, self.captureWorker.screenshot)
        if response['dead_player_' + self.language] == 'notfound':
            return False
        else:
            self.send_text_to_bot.send("The player is dead", self.from_python, 'pink')
            return True
        
    def checkPlayerIsDeadDungeon(self):
        response = RunFindImage(
            self.src_window, self.img_path + '\game_items', 'dead_player_dungeon_' + self.language, self.captureWorker.screenshot)
        if response['dead_player_dungeon_' + self.language] == 'notfound':
            return False
        else:
            self.send_text_to_bot.send("The player is dead", self.from_python, 'pink')
            return True

    def checkPlayerIsDeadAndRevive(self):
        response = RunFindImage(
            self.src_window, self.img_path + '\game_items', 'dead_player_by_' + self.language, self.captureWorker.screenshot)
        if response['dead_player_by_' + self.language] == 'notfound':
            return False
        else:
            self.send_text_to_bot.send("The player is dead", self.from_python, 'pink')
            return True

    def checkPlayerIsDeadCyrangar(self):
        response = RunFindImage(
            self.src_window, self.img_path + '\\' + self.language + '\cyrangar', 'resurrect', self.captureWorker.screenshot)
        if response['resurrect'] == 'notfound':
            return False
        else:
            self.send_text_to_bot.send("The player is dead", self.from_python, 'pink')
            return True

    def checkIsDisconnected(self):
        response = RunFindImage(
            self.src_window, self.img_path + '\screens', 'disconnected_' + self.language, self.captureWorker.screenshot)
        if response['disconnected_' + self.language] == 'notfound':
            return False
        else:
            self.send_text_to_bot.send(
                "The player is disconnected", self.from_python, 'pink')
            return True

    def revivePlayer(self):
        for i in list(range(10))[::-1]:
            if self.checkPlayerIsDead() is False:
                break
            self.send_text_to_bot.send(
                'Trying to revive player ' + str(10 - i) + ' of 10', self.from_python, 'pink')
            self.moveplayer.clickOnCoords((260, 432))
            time.sleep(2)
    
    def revivePlayerDungeon(self):
        for i in list(range(10))[::-1]:
            if self.checkPlayerIsDeadDungeon() is False:
                break
            self.send_text_to_bot.send(
                'Trying to revive player ' + str(10 - i) + ' of 10', self.from_python, 'pink')
            self.moveplayer.clickOnCoords((260, 432))
            # time.sleep(2)

    def revivePlayerByPlayer(self):
        for i in list(range(10))[::-1]:
            if self.checkPlayerIsDeadAndRevive() is False:
                break
            self.send_text_to_bot.send(
                'Trying to revive player by other player ' + str(10 - i) + ' of 10', self.from_python, 'pink')
            self.moveplayer.clickOnCoords((564, 360))
            time.sleep(2)

    def revivePlayerCyrangar(self):
        for i in list(range(60))[::-1]:
            if self.checkPlayerIsDeadCyrangar() is False:
                break
            self.send_text_to_bot.send(
                'Trying to revive player ' + str(60 - i) + ' of 60', self.from_python, 'pink')
            self.moveplayer.clickOnCoords((469, 429))
            time.sleep(2)

    def reconnect(self):
        for i in list(range(10))[::-1]:
            if self.checkIsDisconnected() is False:
                break
            self.send_text_to_bot.send(
                'Trying to reconnect ' + str(10 - i) + ' of 10', self.from_python, 'pink')
            self.moveplayer.clickOnCoords((602, 351))
            time.sleep(2)

    def stop(self):
        self.stopped = True
