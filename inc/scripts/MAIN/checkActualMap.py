
import threading
import time
from findImage import RunFindImage

class CheckActualMap(threading.Thread):
    def __init__(self, threads, src_window, send_text_to_bot, from_python, img_path, actual_map_name, check_every_x_seconds=10, time_to_exit_if_not_in_map_in_seconds=120):
        threading.Thread.__init__(self)
        self.src_window = src_window
        self.stopped = False
        self.is_running = True
        self.paused = False
        self.threads = threads
        self.send_text_to_bot = send_text_to_bot
        self.from_python = from_python
        self.img_path = img_path
        self.actual_map_name = actual_map_name
        self.captureWorker = threads.get_thread('CaptureWorker')
        self.check_every_x_seconds = check_every_x_seconds
        self.time_to_exit_if_not_in_map_in_seconds = time_to_exit_if_not_in_map_in_seconds
        self.time_to_exit_if_not_in_map_in_seconds_counter = 0

    def pause(self):
        self.paused = True

    def resume(self):
        self.paused = False

    def stop(self):
        self.stopped = True

    def run(self):
        while self.stopped is False:
            # try:
            if 1 == 1:
                if self.paused is True:
                    time.sleep(0.5)
                    continue
                
                if self.check_if_player_is_in_map(self.actual_map_name) is False:
                    # print in red
                    print("\033[1;31;40m [ACTUAL MAP] \033[0m" + "Not in the map " + self.actual_map_name)
                    self.time_to_exit_if_not_in_map_in_seconds_counter += self.check_every_x_seconds
                    self.send_text_to_bot.send('Not in the map '+ self.actual_map_name + '?', self.from_python, 'red')
                    self.send_text_to_bot.send('Time to restart: ' + str(self.time_to_exit_if_not_in_map_in_seconds - self.time_to_exit_if_not_in_map_in_seconds_counter) + ' seconds', self.from_python, 'red')
                    if self.time_to_exit_if_not_in_map_in_seconds_counter >= self.time_to_exit_if_not_in_map_in_seconds:
                        self.send_text_to_bot.send('Not in the map ' + self.actual_map_name + ' RESTARTING SPOT', self.from_python, 'red')
                        self.time_to_exit_if_not_in_map_in_seconds_counter = 0
                        self.paused = True
                        self.threads.runAgain()
                else:
                    if self.time_to_exit_if_not_in_map_in_seconds_counter > 0:
                        self.send_text_to_bot.send('In the map ' + self.actual_map_name, self.from_python, 'green')
                    self.time_to_exit_if_not_in_map_in_seconds_counter = 0
                    # print debug in green
                    print("\033[1;32;40m [ACTUAL MAP] \033[0m" + self.actual_map_name)

            # except Exception as e:
                # print("\033[1;31;40m [ACTUAL MAP] \033[0m" + "Error in checkActualMap.py")
                # print(e)
                # continue
            time.sleep(self.check_every_x_seconds)

    def check_if_player_is_in_map(self, map_name):
        response = RunFindImage(
                                self.src_window, self.img_path + '\game_items', 'minimap_name_' + map_name , self.captureWorker.screenshot)
        # print response in yellow
        print("\033[1;33;40m [ACTUAL MAP] \033[0m" + str(response))
        if response['minimap_name_' + map_name] == 'notfound':
            return False
        else:
            return True