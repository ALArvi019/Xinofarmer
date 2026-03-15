import threading
import time
import gc
from findImage import RunFindImage
from readINI import ReadINIFile


class CheckCyrangarEnd(threading.Thread):
    def __init__(self, threads, src_window, send_text_to_bot, from_python, moveplayer, language, img_path):
        threading.Thread.__init__(self)
        self.moveplayer = moveplayer
        self.stopped = False
        self.paused = False
        self.count_player_dead = 0
        self.send_text_to_bot = send_text_to_bot
        self.from_python = from_python
        self.threads = threads
        self.memory_clean = False
        self.captureWorker = threads.get_thread('CaptureWorker')
        self.language = language
        self.src_window = src_window
        self.img_path = img_path
        self.cyrangar_over_time = ReadINIFile(
            img_path + '\\..\\..\\setup.ini', 'Cyrangar', 'Time_to_exit', '999').lower()
        self.cyrangar_over_time = int(self.cyrangar_over_time)
        if not hasattr(self, 'tmp_cyrangar_over_time'):
            self.tmp_cyrangar_over_time = self.cyrangar_over_time
        else:
            if self.cyrangar_over_time != self.tmp_cyrangar_over_time:
                self.cyrangar_over_time = self.tmp_cyrangar_over_time
        self.last_check = time.time()

    def pause(self):
        self.paused = True

    def resume(self):
        self.paused = False

    def stop(self):
        self.stopped = True

    def run(self):
        while self.stopped is False:
            # print("DEBUG: CheckCyrangarEnd run")
            if self.paused is True:
                if self.memory_clean is True:
                    gc.collect()
                    self.memory_clean = False
                time.sleep(0.5)
                continue
            try:
                self.memory_clean = True

                if int(time.time() - self.last_check) >= 10:
                    self.last_check = time.time()
                    self.send_text_to_bot.send('Time to STOP: ' + str(self.tmp_cyrangar_over_time) + " seconds", self.from_python, 'red')

                self.tmp_cyrangar_over_time -= 1
                if self.tmp_cyrangar_over_time <= 0:
                    self.tmp_cyrangar_over_time = self.cyrangar_over_time
                    self.send_text_to_bot.send('Cyrangar time over, stopping Fight.', self.from_python, 'red')
                    self.threads.pause_thread('Fight')
                    # # sum to self.last_check 1000 minutes
                    self.last_check += 60000

                response1 = RunFindImage(
                        self.src_window, self.img_path + '\\' + self.language + '\cyrangar', 'completed' , self.captureWorker.screenshot)
                response2 = RunFindImage(
                        self.src_window, self.img_path + '\\' + self.language + '\cyrangar', 'result' , self.captureWorker.screenshot)
                # print("DEBUG: response1: " + str(response1))
                # print("DEBUG: response2: " + str(response2))
                if response1['completed'] == 'notfound' and response2['result'] == 'notfound':
                    time.sleep(1)
                    continue
                else:
                    self.exitCyrangar()
                    self.pause()
            except Exception as e:
                print(e)
                print("Error checking cyrangar end")
            time.sleep(1)

    def exitCyrangar(self):
        response1 = RunFindImage(
                        self.src_window, self.img_path + '\\' + self.language + '\cyrangar', 'completed' , self.captureWorker.screenshot)
        response2 = RunFindImage(
                        self.src_window, self.img_path + '\\' + self.language + '\cyrangar', 'result' , self.captureWorker.screenshot)
        
        if response1['completed'] != 'notfound':
            self.send_text_to_bot.send('Cyrangar completed, exiting1', self.from_python, 'green')
            time.sleep(5)
            self.moveplayer.clickOnCoords((478, 368))
            time.sleep(5)
            self.send_text_to_bot.send('Cyrangar completed, exiting', self.from_python, 'green')
            time.sleep(5)
            self.moveplayer.clickOnCoords((478, 368))
            time.sleep(5)
        if response2['result'] != 'notfound':
            self.send_text_to_bot.send('Cyrangar completed, exiting', self.from_python, 'green')
            time.sleep(5)
            self.moveplayer.clickOnCoords((478, 368))
            time.sleep(5)

        response = RunFindImage(
                        self.src_window, self.img_path + '\game_items', 'hand_up' , self.captureWorker.screenshot)
        actualtime = time.time()
        self.threads.pause_thread('EndlessModeCheckLine')
        self.threads.pause_thread('Fight')
        while response['hand_up'] == 'notfound' and time.time() - actualtime < 120:
            self.send_text_to_bot.send('Waiting for exit cyrangar ' + str(int(time.time() - actualtime)) + '/120', self.from_python, 'purple')
            response = RunFindImage(
                        self.src_window, self.img_path + '\game_items', 'hand_up' , self.captureWorker.screenshot)
            time.sleep(1)
        self.moveplayer.processing_movement_output('NK')
        self.moveplayer.processing_movement_output('NK')
        time.sleep(3)
        self.moveplayer.processing_movement_output('↗')
        time.sleep(5)
        self.moveplayer.processing_movement_output('NK')
        self.moveplayer.processing_movement_output('NK')
        self.send_text_to_bot.send('command|finishedendlessfromxf', self.from_python, False, True)
        self.threads.pause_all_threads()
        time.sleep(1)
        self.threads.pause_all_threads()
        time.sleep(1)
        self.threads.pause_all_threads()
        time.sleep(1)
        self.threads.pause_all_threads()
        