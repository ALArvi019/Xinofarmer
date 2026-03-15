import threading
from sendTextToBot import SendTextToBot
from threads import Threads
from checksColors import CheckColors
import time



class runDungeon():

    def __init__(self, src_window, images_path, dungeon_name, language, send_text_to_bot, from_python, solo, time_to_exit, time_to_wait_party, replay_dungeon):
        self.src_window = src_window
        self.images_path = images_path
        self.dungeon_name = dungeon_name.lower()
        self.language = language
        self.threads = Threads()
        self.send_text_to_bot = send_text_to_bot
        self.from_python = from_python
        self.solo = solo
        self.time_to_exit = time_to_exit
        self.time_to_wait_party = time_to_wait_party
        self.replay_dungeon = replay_dungeon

    def RunDungeon(self):
        print("DEBUG: RunDungeon")
        print("DEBUG: src_window: " + self.src_window)
        print("DEBUG: images_path: " + self.images_path)
        print("DEBUG: dungeon_name: " + self.dungeon_name)
        print("DEBUG: language: " + self.language)
        print("DEBUG: send_text_to_bot: " + str(self.send_text_to_bot))
        print("DEBUG: from_python: " + str(self.from_python))
        print("DEBUG: solo: " + str(self.solo))
        print("DEBUG: time_to_exit: " + str(self.time_to_exit))
        print("DEBUG: time_to_wait_party: " + str(self.time_to_wait_party))
        print("DEBUG: replay_dungeon: " + str(self.replay_dungeon))

        if self.replay_dungeon is True or self.replay_dungeon is 'True':
            go_to_dungeon = False
        else:
            go_to_dungeon = True

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
                self.RunFarmingSpot()

        rundungeon = self.threads.create_thread(
              'RunDungeonThread', self.threads, self.src_window, self.images_path, self.dungeon_name, self.language, skills_means, self.send_text_to_bot, self.from_python, go_to_dungeon, self.solo, self.time_to_exit, self.time_to_wait_party)
        # BELOW ONLY FOR DEBUG
            # 'RunDungeonThread', self.threads, self.src_window, self.images_path, self.dungeon_name, self.language, skills_means, self.send_text_to_bot, self.from_python, False, self.solo, self.time_to_exit, self.time_to_wait_party)

        rundungeon.go_to_dungeon = go_to_dungeon
        self.threads.resume_thread('RunDungeonThread')
        return 'Ok'
    
# for i in list(range(4))[::-1]:
#     print(i+1)
#     time.sleep(1)

# send_text_to_bot = SendTextToBot()
# # (self, src_window, images_path, dungeon_name, language, send_text_to_bot, from_python, solo, time_to_exit, time_to_wait_party):
# rundungeon = runDungeon("LDPlayer", "path\\to\\immortal_xinofarmer\\inc\\img",
#                               "kikuras", 'en', send_text_to_bot, True, True, 600, 600)
# rundungeon.RunDungeon()