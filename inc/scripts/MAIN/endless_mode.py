from threads import Threads
from checksColors import CheckColors
import time
import threading
from sendTextToBot import SendTextToBot




class runEndlessMode():
    def __init__(self, src_window, images_path, send_text_to_bot, from_python, language, telegramConfig, username):
        self.src_window = src_window
        self.img_path = images_path
        self.send_text_to_bot = send_text_to_bot
        self.from_python = from_python
        self.language = language
        self.telegramConfig = telegramConfig
        self.username = username
        self.threads = Threads()
        self.skills_means = None


    def RunENdlessMode(self):
        print("DEBUG: RunENdlessMode")
        print("DEBUG: src_window: " + self.src_window)
        print("DEBUG: inc_path: " + self.img_path)
        print("DEBUG: send_text_to_bot: " + str(self.send_text_to_bot))
        print("DEBUG: from_python: " + str(self.from_python))
        print("DEBUG: language: " + self.language)
        print("DEBUG: telegramConfig: " + str(self.telegramConfig))
        print("DEBUG: username: " + self.username)

        print(threading.enumerate())
        for thread in threading.enumerate():
                try:
                    thread.pause()
                except:
                    pass

        checkcolors = CheckColors(self.src_window)
        skills_means = None
        retyes = 0
        while skills_means is None:
            skills_means = checkcolors.define_mean_of_skills()
            retyes += 1
            time.sleep(1)
            if retyes > 5:
                self.send_text_to_bot.send(
                    "Error getting skills means", self.from_python)
                # wait 5 sec and run function again
                time.sleep(5)
                self.RunENdlessMode()

        endlessmode = self.threads.create_thread(
            'EndlessModeThread', self.threads, self.src_window, self.img_path, self.send_text_to_bot, self.from_python, self.language, self.telegramConfig, self.username, skills_means)
        self.threads.resume_thread('EndlessModeThread')

        return 'Ok'


# for i in list(range(4))[::-1]:
#      print(i+1)
#      time.sleep(1)

# send_text_to_bot = SendTextToBot()
# runfarmspot = runEndlessMode("LDPlayer", "path\\to\\inc\\img", send_text_to_bot, True, 'en', True, 'user@example.com')
# runfarmspot.RunENdlessMode()
