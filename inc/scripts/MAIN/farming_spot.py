from threads import Threads
from checksColors import CheckColors
import time
import threading
from sendTextToBot import SendTextToBot

spot_coords = {
    'zavain1': {
        'left_menu': (110, 265),
        'map_position': (605, 235),
        'spot_safe_zone': (499, 339),
        'left_menu_safe_zone': (110, 265),
        'time_to_wait': 3,
        'go_to_spot': True,
        'move_to_blacksmith': None,
        'stuck_average': 40,
        'rectangle': (84, 75),
        'move_to_bestiary': [
            (1, "West"),
        ],
    },
    'zavain2': {
        'left_menu': (110, 265),
        'map_position': (605, 235),
        'spot_safe_zone': (499, 339),
        'left_menu_safe_zone': (110, 265),
        'time_to_wait': 3,
        'stuck_average': 40,
        'go_to_spot': True,
        'move_to_blacksmith': None,
        'rectangle': (84, 75),
        'move_to_bestiary': [
            (1, "West"),
        ],
    },
    'shassarsea': {
        'left_menu': (114, 181),
        'map_position': (531, 242),
        'spot_safe_zone': (544, 322),
        'left_menu_safe_zone': (114, 181),
        'stuck_average': 40,
        'go_to_spot': True,
        'time_to_wait': 3,
        'move_to_blacksmith': [
            (1, "NorthWest"),
        ],
        'rectangle': (44, 95),
        'move_to_bestiary': None,
    },
    'bilefen': {
        'left_menu': (127, 268),
        'map_position': (411, 353),
        'spot_safe_zone': (456, 306),
        'left_menu_safe_zone': (134, 178),
        'stuck_average': 40,
        'go_to_spot': True,
        'time_to_wait': 3,
        'move_to_blacksmith': None,
        'rectangle': (93, 94),
        'move_to_bestiary': None,
    },
    'realm': {
        'left_menu': (103, 269),
        'map_position': (429, 189),
        'spot_safe_zone': (429, 189),
        'left_menu_safe_zone': (103, 269),
        'stuck_average': 40,
        'go_to_spot': True,
        'time_to_wait': 3,
        'move_to_blacksmith': None,
        'rectangle': (93, 94),
        'move_to_bestiary': None,
    },
    'rift': {
        'left_menu': (111, 224),
        'map_position': (771, 312),
        'spot_safe_zone': (775, 334),
        'left_menu_safe_zone': (111, 224),
        'stuck_average': 40,
        'go_to_spot': False,
        'time_to_wait': 3,
        'move_to_blacksmith': None,
        'rectangle': (61, 94),
        'move_to_bestiary': None,
    },
    'storm': {
        'left_menu': (112, 226),
        'map_position': (431, 345),
        'go_to_spot': True,
        'spot_safe_zone': (443, 330),
        'left_menu_safe_zone': (112, 226),
        'stuck_average': 70,
        'time_to_wait': 3,
        'move_to_blacksmith': None,
        'rectangle': (40, 98),
        'move_to_bestiary': None,
    },
    'ancients': {
        'left_menu': (128, 354),
        'map_position': (521, 312),
        'go_to_spot': True,
        'spot_safe_zone': (521, 312),
        'left_menu_safe_zone': (128, 354),
        'stuck_average': 80,
        'time_to_wait': 3,
        'move_to_blacksmith': None,
        'rectangle': (39, 82),
        'move_to_bestiary': None,
    },
    'custom_model': {
        'left_menu': (128, 354),
        'map_position': (521, 312),
        'go_to_spot': False,
        'spot_safe_zone': (0, 0),
        'left_menu_safe_zone': (128, 354),
        'stuck_average': 80,
        'time_to_wait': 3,
        'move_to_blacksmith': None,
        'rectangle': (39, 82),
        'move_to_bestiary': None,
    },
}


class runFarmingSpot():

    def __init__(self, src_window, inc_path, fileName, send_text_to_bot, from_python, language, acceptPartyInvite, ranged, dead, telegramConfig, username, checkPartyLeader, CheckBestyaryEveryIfNotification, CheckBestyaryEveryIfNotificationNotFound, modelname):
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
        self.skills_means = None
        self.threads = Threads()
        self.checkPartyLeader = checkPartyLeader
        self.CheckBestyaryEveryIfNotification = CheckBestyaryEveryIfNotification
        self.CheckBestyaryEveryIfNotificationNotFound = CheckBestyaryEveryIfNotificationNotFound
        self.modelname = modelname


    def RunFarmingSpot(self):
        print("DEBUG: RunFarmingSpot")
        print("DEBUG: src_window: " + self.src_window)
        print("DEBUG: inc_path: " + self.inc_path)
        print("DEBUG: fileName: " + self.fileName)
        print("DEBUG: send_text_to_bot: " + str(self.send_text_to_bot))
        print("DEBUG: from_python: " + str(self.from_python))
        print("DEBUG: language: " + self.language)
        print("DEBUG: acceptPartyInvite: " + str(self.acceptPartyInvite))
        print("DEBUG: ranged: " + str(self.ranged))
        print("DEBUG: dead: " + str(self.dead))
        print("DEBUG: telegramConfig: " + str(self.telegramConfig))
        print("DEBUG: username: " + self.username)
        print("DEBUG: checkPartyLeader: " + str(self.checkPartyLeader))
        print("DEBUG: CheckBestyaryEveryIfNotification: " + str(self.CheckBestyaryEveryIfNotification))
        print("DEBUG: CheckBestyaryEveryIfNotificationNotFound: " + str(self.CheckBestyaryEveryIfNotificationNotFound))
        print("DEBUG: skills_means: " + str(self.skills_means))
        print("DEBUG: modelname: " + self.modelname)
        
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

        farmingspot = self.threads.create_thread(
            'FarmingSpotThread', self.threads, self.src_window, self.inc_path, self.fileName, self.send_text_to_bot, self.from_python, self.language, self.acceptPartyInvite, self.ranged, self.dead, self.telegramConfig, self.username, spot_coords, skills_means, self.checkPartyLeader, self.CheckBestyaryEveryIfNotification, self.CheckBestyaryEveryIfNotificationNotFound, self.modelname)
        self.threads.resume_thread('FarmingSpotThread')

        return 'Ok'


# for i in list(range(4))[::-1]:
#     print(i+1)
#     time.sleep(1)

# send_text_to_bot = SendTextToBot()
# runfarmspot = runFarmingSpot("LDPlayer", "path\\to\\inc",
#                               "ancients", send_text_to_bot, True, 'en', True, False, False, True, 'user@example.com', True)
# runfarmspot.RunFarmingSpot()
