
import threading
import time
from findImage import RunFindImage

class CheckDungeonLoot(threading.Thread):
    def __init__(self, threads, src_windows, send_text_to_bot, from_python, moveplayer, img_path):
        threading.Thread.__init__(self)
        self.stopped = False
        self.is_running = True
        self.paused = False
        self.threads = threads
        self.send_text_to_bot = send_text_to_bot
        self.from_python = from_python
        self.captureWorker = threads.get_thread('CaptureWorker')
        self.moveplayer = moveplayer
        self.img_path = img_path
        self.src_window = src_windows

    def pause(self):
        self.paused = True

    def resume(self):
        self.paused = False

    def stop(self):
        self.stopped = True

    def run(self):
        while self.stopped is False:
            try:
                if self.paused is True:
                    time.sleep(0.5)
                    continue
            
                response = RunFindImage(
                    self.src_window, self.img_path + '\\game_items', 'hand_down', self.captureWorker.screenshot, 0.8, False, False)
                if response['hand_down'] != 'notfound':
                                self.moveplayer.pressKey('f')

            except Exception as e:
                print("\033[1;31;40m [CHECK DUNGEON LOOT] \033[0m" + "Error in checkDungeonLoot.py")
                print(e)
                continue

            time.sleep(0.5)