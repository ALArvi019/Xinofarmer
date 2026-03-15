
import threading
import time

class CheckDungeonTime(threading.Thread):
    def __init__(self, threads, send_text_to_bot, from_python, moveplayer, img_path, dungeon_over_time=600):
        threading.Thread.__init__(self)
        self.stopped = False
        self.is_running = True
        self.paused = False
        self.actual_time = 0
        self.threads = threads
        self.send_text_to_bot = send_text_to_bot
        self.from_python = from_python
        self.dungeon_over_time = dungeon_over_time
        self.captureWorker = threads.get_thread('CaptureWorker')
        self.rundungeonOrchestration = None
        self.RunDungeonThread = threads.get_thread('RunDungeonThread')
        self.fight = threads.get_thread('Fight')
        self.moveplayer = moveplayer
        self.img_path = img_path
        self.last_message_time = 0
        if not hasattr(self, 'tmp_dungeon_over_time'):
            self.tmp_dungeon_over_time = self.dungeon_over_time
        else:
            if self.dungeon_over_time != self.tmp_dungeon_over_time:
                self.dungeon_over_time = self.tmp_dungeon_over_time

    def pause(self):
        self.paused = True

    def resume(self):
        self.paused = False

    def stop(self):
        self.stopped = True

    def run(self):
        while self.stopped is False:
            try:
            # if 1 == 1:
                if self.paused is True:
                    time.sleep(0.5)
                    self.last_message_time = 0
                    continue
                
                if self.actual_time == 0:
                    if self.paused is True:
                        continue
                    self.actual_time = time.time()

                if self.RunDungeonThread.check_if_player_is_in_special_event_dungeon() is not False:
                    if self.RunDungeonThread.check_if_player_is_in_special_event_dungeon() is not False:
                        dungeon_special_event_coords = self.RunDungeonThread.check_if_player_is_in_special_event_dungeon()
                        if dungeon_special_event_coords is not False:
                            if self.paused is True:
                                continue
                            self.send_text_to_bot.send('Player is in special event dungeon, stopping all threads.', self.from_python, 'red')
                            self.actual_time = self.dungeon_over_time
                            self.send_text_to_bot.send(
                                "Detect special event", self.from_python)
                            self.moveplayer.clickOnCoords(dungeon_special_event_coords)
                            time.sleep(4)

                if self.RunDungeonThread.check_if_player_is_in_dungeon(1, False) is False:
                    if self.RunDungeonThread.check_if_player_is_in_dungeon(1, False) is False:
                        if self.RunDungeonThread.check_if_player_is_in_dungeon(1, False) is False:
                            if self.paused is True:
                                continue
                            self.send_text_to_bot.send('Player is not in dungeon??, stopping all threads.', self.from_python, 'red')
                            self.actual_time = self.dungeon_over_time

                if self.last_message_time == 0:
                    if self.paused is True:
                        continue
                    self.last_message_time = time.time()

                # print time left every minute
                if self.calculate_dungeon_time(self.last_message_time) >= 30:
                    # self.send_text_to_bot.send('\\[]
                    calc = self.dungeon_over_time - self.calculate_dungeon_time(self.actual_time)
                    if calc < 0:
                        calc = 0
                    print("\033[1;31;40m [DUNGEON TIME] \033[0m" + str(calc) + " seconds left.")
                    self.send_text_to_bot.send(str(calc) + " seconds to leave dungeon.", self.from_python, 'red')
                    self.last_message_time = time.time()
                if self.paused is True:
                    continue
                # 5 minutes
                # print in yellow self.actual_time
                print("\033[1;33;40m [DUNGEON TIME] \033[0m" + str(self.actual_time) + " seconds.")
                print("\033[1;33;40m [DUNGEON TIME] \033[0m" + str(self.calculate_dungeon_time(self.actual_time)) + " seconds.")
                print("\033[1;33;40m [DUNGEON TIME] \033[0m" + str(self.dungeon_over_time) + " seconds.")
                if self.calculate_dungeon_time(self.actual_time) >= self.dungeon_over_time:
                    self.fight.force_fight = False
                    print("\033[1;31;40m [DUNGEON TIME] \033[0m" + "Dungeon time is over, please leave the dungeon.")
                    self.send_text_to_bot.send('Dungeon time is over, please leave the dungeon.', self.from_python, 'red')
                    self.actual_time = 0
                    self.force_exit_dungeon()
                    while self.RunDungeonThread.check_if_player_is_in_dungeon(2) is True:
                        self.send_text_to_bot.send('Player is still in dungeon, waiting 5 seconds to check again.', self.from_python, 'red')
                        self.force_exit_dungeon()
                        for i in range(5):
                            self.send_text_to_bot.send(str(5 - i) + ' seconds left to check if player is still in dungeon.', self.from_python, 'purple')
                            time.sleep(1)
                    if self.rundungeonOrchestration is None:
                        self.rundungeonOrchestration = self.threads.get_thread('RunDungeonOrchestration')
                    self.rundungeonOrchestration.setAllStepsToFalse()
                    self.send_text_to_bot.send(
                        'command|finishdungeonfromxfNF', self.from_python, False, True)
                    self.threads.pause_all_threads()

            except Exception as e:
                print("\033[1;31;40m [DUNGEON TIME] \033[0m" + "Error in checkDungeonTime.py")
                print(e)
                continue
            time.sleep(1)

    def calculate_dungeon_time(self, actual_time):
        return int(time.time() - actual_time)

    def force_exit_dungeon(self, from_dungeon_orchestration=False):

        if from_dungeon_orchestration is False:
            self.threads.pause_all_threads(['CheckIsDead', 'CaptureWorker'])
        else:
            self.threads.pause_all_threads(['CheckIsDead', 'CaptureWorker', 'RunDungeonOrchestration'])
        self.threads.resume_thread('Fight')
        self.threads.resume_thread('CheckLife')
        self.moveplayer.processing_reverse_movement_output('NK')
        self.moveplayer.processing_reverse_movement_output('NK')
        time.sleep(2)
        while self.fight.checkFightIsRunning() is True:
            time.sleep(2)
        if from_dungeon_orchestration is False:
            self.threads.pause_all_threads(['CheckIsDead', 'CaptureWorker'])
        else:
            self.threads.pause_all_threads(['CheckIsDead', 'CaptureWorker', 'RunDungeonOrchestration'])
        self.moveplayer.clickOnCoords((713, 134))
        time.sleep(2)
        # click 576, 357
        self.moveplayer.clickOnCoords((576, 357))
        time.sleep(10)