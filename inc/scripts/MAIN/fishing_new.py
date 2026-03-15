from threads import Threads
import threading
# only for debug --->
import time
from sendTextToBot import SendTextToBot

class runFishNew():

    def __init__(self, src_window, img_path, send_text_to_bot, from_python):
        self.src_window = src_window
        self.img_path = img_path
        self.send_text_to_bot = send_text_to_bot
        self.from_python = from_python
        self.threads = Threads()


    def RunFishNew(self):
        print("DEBUG: RunFishNew")
        print("DEBUG: src_window: " + self.src_window)
        print("DEBUG: ima_path: " + self.img_path)
        print("DEBUG: send_text_to_bot: " + str(self.send_text_to_bot))
        print("DEBUG: from_python: " + str(self.from_python))
        
        print(threading.enumerate())
        for thread in threading.enumerate():
                try:
                    thread.pause()
                except:
                    pass

        fishnew = self.threads.create_thread(
            'FishNewThread', self.threads, self.src_window, self.img_path, self.send_text_to_bot, self.from_python)
        self.threads.resume_thread('FishNewThread')
        return 'Ok'


# for i in list(range(4))[::-1]:
#     print(i+1)
#     time.sleep(1)

# send_text_to_bot = SendTextToBot()

# runfishnew = runFishNew("LDPlayer", "path\\to\\immortal_xinofarmer\\inc\\img", send_text_to_bot, True)
# runfishnew.RunFishNew()
