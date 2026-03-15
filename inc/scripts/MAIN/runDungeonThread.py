import threading
import time
from movePlayer import moveplayer


class RunDungeonThread(threading.Thread):

    def __init__(self, threads, src_window, images_path, dungeon_name, language, skills_means, send_text_to_bot, from_python, go_to_dungeon, solo, time_to_exit, time_to_wait_party):
        threading.Thread.__init__(self)
        self.src_window = src_window
        self.img_path = images_path
        self.dungeon_name = dungeon_name
        self.language = language
        self.threads = threads
        self.skills_means = skills_means
        self.stopped = False
        self.paused = False
        self.send_text_to_bot = send_text_to_bot
        self.from_python = from_python
        self.go_to_dungeon = go_to_dungeon
        self.moveplayer = None
        self.captureWorker = None
        self.checkDungeonTime = None
        self.solo = solo
        self.time_to_exit = time_to_exit
        self.time_to_wait_party = time_to_wait_party
        self.special_event = False
        self.movement_in_front_of_door = {
            "kikuras" : ['↗'],
            "namari" : None,
            "king_breach" : ['↗']
        }
        self.movement_special_event = {
            "kikuras" : ['↘'],
            "namari" : None,
            "king_breach" : ['↗']
        }

    def pause(self):
        self.paused = True

    def stop(self):
        self.stopped = True

    def resume(self):
        self.paused = False

    def run(self):
        print("DEBUG: RunDungeonThread started")
        while self.stopped is False:
            
            if self.paused is True:
                time.sleep(1)
                continue
            # if 1 == 1:
            try:
                print("DEBUG: RunDungeonThread running")
                loot_path = self.img_path + '\\'+self.language+'\\loot_items'
                img_farm_path = self.img_path + '\\'+self.language+'\\farm'
                inc_path = self.img_path + '\\..'

                try:
                    captureWorker = self.threads.create_thread(
                        'CaptureWorker', self.src_window, self.img_path)
                    self.captureWorker = captureWorker
                    self.threads.resume_thread('CaptureWorker')
                except Exception as e:
                    print(e)
                    print("Error running captureWorker")

                Moveplayer = moveplayer(
                    self.src_window, self.threads, self.img_path, self.language, self.send_text_to_bot, self.from_python)
                self.moveplayer = Moveplayer
                self.threads.moveplayer = Moveplayer

                checkisdead = self.threads.create_thread(
                    'CheckIsDead', self.threads, self.src_window, self.send_text_to_bot, self.from_python, Moveplayer, self.language, self.img_path, False, True)
                
                fight = self.threads.create_thread(
                    'Fight', self.threads, self.skills_means, False, Moveplayer, self.send_text_to_bot, self.from_python, self.solo, self.img_path)
                
                dungeonWorker = self.threads.create_thread(
                    'DungeonWorker', self.threads, self.src_window, self.img_path, self.dungeon_name, inc_path, self.send_text_to_bot, self.from_python, (0,0), Moveplayer)

                checklife = self.threads.create_thread(
                    'CheckLife', self.threads, Moveplayer, self.send_text_to_bot, self.from_python, self.img_path)

                checkLoot = self.threads.create_thread(
                    'CheckLoot', self.threads, self.src_window, loot_path, self.send_text_to_bot, self.from_python, self.img_path, Moveplayer, False, True)
                
                # self, threads, src_window, wantPartyInvite, language, img_farm_path, send_text_to_bot, from_python, fileName, moveplayer, checkPartyLeader):
                checkPartyInvite = self.threads.create_thread(
                    'CheckPartyInvite', self.threads, self.src_window, False, self.language, img_farm_path, self.send_text_to_bot, self.from_python, 'CheckPartyInvite', Moveplayer, False)
                self.threads.resume_thread('CheckPartyInvite')

                checkDungeonTime = self.threads.create_thread(
                    'CheckDungeonTime', self.threads, self.send_text_to_bot, self.from_python, Moveplayer, self.img_path, self.time_to_exit)

                runDungeonOrchestration = self.threads.create_thread(
                    'RunDungeonOrchestration', self.threads, self.src_window, self.img_path, self.dungeon_name, self.language, self.send_text_to_bot, self.from_python, Moveplayer, self.solo)
                runDungeonOrchestration.special_event = False

                CheckDungeonLoot = self.threads.create_thread(
                    'CheckDungeonLoot', self.threads, self.src_window, self.send_text_to_bot, self.from_python, Moveplayer, self.img_path)
                
                CheckDungeonMandatoryStep = self.threads.create_thread(
                    'CheckDungeonMandatoryStep', self.threads, self.src_window, self.send_text_to_bot, self.from_python, Moveplayer, self.img_path, self.dungeon_name, self.language, self.solo)
                

                if self.go_to_dungeon:
                    if self.solo:
                        continuerun = True
                        if Moveplayer.openMap(True) == False:
                            self.send_text_to_bot.send(
                                "Error opening map", self.from_python)
                            continuerun = False
                        if continuerun:
                            # 1 GO TO DUNGEON ENTRANCE-----------------------
                            if self.go_to_dungeon_entrance() == False:
                                continue
                            # 2 OPEN THE FIND PARTY BUTTON ENTRANCE-----------------------
                            if self.open_find_party_screen() == False:
                                continue
                            if self.enter_dungeon_without_party() == False:
                                continue
                            self.go_to_dungeon = False
                        else:
                            time.sleep(1)
                            continue
                    else:
                        if self.check_if_party_is_ready():
                            continue
                        continuerun = True
                        if Moveplayer.openMap(True) == False:
                            self.send_text_to_bot.send(
                                "Error opening map", self.from_python)
                            continuerun = False
                        if continuerun:
                            if self.check_if_party_is_ready():
                                continue
                            if self.check_if_party_is_ready():
                                continue
                            # 1 GO TO DUNGEON ENTRANCE-----------------------
                            if self.go_to_dungeon_entrance() == False:
                                continue
                            if self.check_if_party_is_ready():
                                continue
                            # 0 REMOVE DISCONNECTED PLAYER-----------------------
                            self.remove_player_disconnected()
                            # 2 OPEN THE FIND PARTY BUTTON ENTRANCE-----------------------
                            if self.check_if_party_is_ready():
                                continue
                            if self.open_find_party_screen() == False:
                                continue
                            # 3 CHECK IF WE ALREADY FINDING GROUP-----------------------
                            if self.check_if_party_is_ready():
                                continue
                            if self.find_dungeon_party() == False:
                                print("DEBUG: Error finding party")
                                continue
                            self.go_to_dungeon = False
                        else:
                            time.sleep(1)
                            continue
                
                # check if all threads are initialized
                self.threads.wait_until_thread_initialized('CaptureWorker')
                self.threads.wait_until_thread_initialized('DungeonWorker')
                self.threads.wait_until_thread_initialized('CheckIsDead')
                self.threads.wait_until_thread_initialized('CheckLife')
                self.threads.wait_until_thread_initialized('Fight')
                self.threads.wait_until_thread_initialized('CheckLoot')
                self.threads.wait_until_thread_initialized('CheckPartyInvite')
                self.threads.wait_until_thread_initialized('RunDungeonOrchestration')
                self.threads.wait_until_thread_initialized('CheckDungeonMandatoryStep')

                if self.solo and self.special_event == True:
                    runDungeonOrchestration.special_event = True

                self.threads.resume_thread('RunDungeonOrchestration')
                self.go_to_dungeon = True
                self.paused = True

            except Exception as e:
                print("DEBUG: RunDungeonThread exception: " + str(e))
                time.sleep(1)
                continue

    def remove_player_disconnected(self):
        # check if player is disconnected
        player_disconnected_coords = self.moveplayer.founfIconInScreen(
            self.img_path + '\\game_items', 'player_disconnect', 1, False, self.captureWorker.screenshot)
        while player_disconnected_coords != (0, 0):
            self.send_text_to_bot.send(
                "Player disconnected, remove from party", self.from_python)
            self.moveplayer.clickOnCoords(player_disconnected_coords)
            time.sleep(1)
            # find remove  party icon
            remove_party_icon_coords = self.moveplayer.founfIconInScreen(
                self.img_path + '\\game_items', 'delete_player_' + self.language, 1, False, self.captureWorker.screenshot)
            if remove_party_icon_coords != (0, 0):
                self.moveplayer.clickOnCoords(remove_party_icon_coords)
                time.sleep(1)
            player_disconnected_coords = self.moveplayer.founfIconInScreen(
                self.img_path + '\\game_items', 'player_disconnect', 1, False, self.captureWorker.screenshot)

    def find_dungeon_party(self):
        wait_for_party = False
        for i in range(3):
            if self.check_if_party_is_ready():
                return True
            find_party_icon_coords = self.moveplayer.founfIconInScreen(
                self.img_path + '\\game_items', 'find_party_' + self.language, 1, False, self.captureWorker.screenshot, False)
            if find_party_icon_coords != (0, 0):
                wait_for_party = True
                break
            time.sleep(1)
        if find_party_icon_coords != (0, 0):
            self.send_text_to_bot.send(
                "Search party", self.from_python)
            self.moveplayer.clickOnCoords(find_party_icon_coords)
            time.sleep(1)
        if wait_for_party == False:
            # check if cancel button is in screen
            for i in range(3):
                if self.check_if_party_is_ready():
                    return True
                find_cancel_icon_coords = self.moveplayer.founfIconInScreen(
                    self.img_path + '\\game_items', 'cancel_' + self.language, 1, False, self.captureWorker.screenshot, False)
                if find_cancel_icon_coords != (0, 0):
                    wait_for_party = True
                    break
                time.sleep(1)
        if wait_for_party == False:
            # check if finding party is in screen
            for i in range(3):
                if self.check_if_party_is_ready():
                    return True
                find_party_icon_coords = self.moveplayer.founfIconInScreen(
                    self.img_path + '\\game_items', 'finding_party_' + self.language, 1, False, self.captureWorker.screenshot, False)
                if find_party_icon_coords != (0, 0):
                    wait_for_party = True
                    break
                time.sleep(1)
        if wait_for_party == False:
            # check if refuse button is in screen
            for i in range(3):
                if self.check_if_party_is_ready():
                    return True
                find_refuse_icon_coords = self.moveplayer.founfIconInScreen(
                    self.img_path + '\\game_items', 'refuse_' + self.language, 1, False, self.captureWorker.screenshot, False)
                if find_refuse_icon_coords != (0, 0):
                    wait_for_party = True
                    break
                time.sleep(1)
        if wait_for_party == False:
            # no more  combination exists
            self.send_text_to_bot.send(
                "Error finding party1", self.from_python)
            self.threads.resume_thread('CheckIsDead')
            self.threads.pause_thread('Fight')
            self.moveplayer.pressKey('esc')
            return False
        # wait for party
        actualtime = time.time()
        player_party_coords = self.moveplayer.founfIconInScreen(
            self.img_path + '\\game_items', 'player_party', 1, False, self.captureWorker.screenshot, False)
        while player_party_coords != (0, 0):
            time.sleep(1)
            player_party_coords = self.moveplayer.founfIconInScreen(
                self.img_path + '\\game_items', 'player_party', 1, False, self.captureWorker.screenshot, False)
            find_party_icon_coords = self.moveplayer.founfIconInScreen(
                self.img_path + '\\game_items', 'find_party_' + self.language, 1, False, self.captureWorker.screenshot, False)
            if find_party_icon_coords != (0, 0):
                self.moveplayer.clickOnCoords(find_party_icon_coords)
                time.sleep(1)
            self.send_text_to_bot.send(
                "Waiting for party (" + str(int(time.time() - actualtime)) + "/"+ str(self.time_to_wait_party)+")", self.from_python, "blue")
            if time.time() - actualtime > self.time_to_wait_party:
                self.send_text_to_bot.send(
                    "Error finding party", self.from_python)
                self.threads.resume_thread('CheckIsDead')
                self.threads.pause_thread('Fight')
                self.moveplayer.pressKey('esc')
                return False
            if self.check_if_party_is_ready():
                return True
            find_refuse_icon_coords = self.moveplayer.founfIconInScreen(
                    self.img_path + '\\game_items', 'refuse_' + self.language, 4, False, self.captureWorker.screenshot, False)
            if self.check_if_party_is_ready():
                return True
            if find_refuse_icon_coords != (0, 0):
                if self.check_if_party_is_ready():
                    return True
                self.moveplayer.clickOnCoords(find_refuse_icon_coords)
                time.sleep(1)
                self.send_text_to_bot.send(
                        "Refuse party, not 4 players found", self.from_python)
                return self.find_dungeon_party()

        # press enter dungeon and wait all party members 839, 460
        self.send_text_to_bot.send(
                    "Enter dungeon1", self.from_python)
        self.moveplayer.clickOnCoords((839, 460))
        time.sleep(1)
        if self.check_if_player_is_in_dungeon():
            return True
        else:
            return False
        
    def enter_dungeon_without_party(self):
         # press enter dungeon and wait all party members 839, 460
        self.send_text_to_bot.send(
                    "Enter dungeon--", self.from_python)
        self.moveplayer.clickOnCoords((839, 460))
        time.sleep(1)
        if self.check_if_player_is_in_dungeon():
            return True
        else:
            return False

    def check_if_party_is_ready(self):
        find_refuse_icon_coords = self.moveplayer.founfIconInScreen(
            self.img_path + '\\game_items', 'refuse_' + self.language, 1, False, self.captureWorker.screenshot, False)
        if find_refuse_icon_coords != (0, 0):
            player_party_coords = self.moveplayer.founfIconInScreen(
                self.img_path + '\\game_items', 'player_party', 1, False, self.captureWorker.screenshot)
            if player_party_coords == (0, 0):
                self.send_text_to_bot.send(
                    "Enter dungeon", self.from_python)
                self.moveplayer.clickOnCoords((839, 460))
                for i in range(10):
                    self.send_text_to_bot.send(
                        "Enter dungeon (" + str(i+1) + "/10)", self.from_python)
                if self.check_if_player_is_in_dungeon():
                    return True
        return False
    
    def check_if_player_is_in_dungeon(self, retry = 10, show_msg=True):
        # TO DO: WAITING FOR PLAYERS
        # load_screen_coords = self.moveplayer.founfIconInScreen(
        #     self.img_path + '\\game_items', 'load_screen', 1, False, self.captureWorker.screenshot)
        dungeon_intro_coords = self.moveplayer.founfIconInScreen(
            self.img_path + '\\game_items', 'dungeon_intro', 1, False, self.captureWorker.screenshot, False)
        inside_dungeon_icon_coords = self.moveplayer.founfIconInScreen(
            self.img_path + '\\game_items', 'inside_dungeon_icon', 1, False, self.captureWorker.screenshot, False)
        inside_dungeon_icon_coords_2 = self.moveplayer.founfIconInScreen(
            self.img_path + '\\game_items', 'inside_dungeon_icon_2', 1, False, self.captureWorker.screenshot, False)
        dungeon_special_event_coords = self.moveplayer.founfIconInScreen(
            self.img_path + '\\game_items', 'dungeon_special_event', 1, False, self.captureWorker.screenshot, False)
        # 10 try
        inside = False
        special_event = False
        for i in range(retry):
            if show_msg:
                self.send_text_to_bot.send(
                "Check if player is inside dungeon (" + str(i+1) + "/" + str(retry) + ")", self.from_python, "blue")
            # if load_screen_coords != (0, 0):
            #     self.send_text_to_bot.send(
            #         "Loading screen", self.from_python)
            #     time.sleep(2)
            #     continue
            if dungeon_intro_coords != (0, 0):
                if show_msg:
                    self.send_text_to_bot.send(
                    "Dungeon intro", self.from_python)
                self.moveplayer.clickOnCoords(dungeon_intro_coords)
                time.sleep(4)
            if dungeon_special_event_coords != (0, 0):
                if show_msg:
                    self.send_text_to_bot.send(
                    "Detect special event", self.from_python)
                self.moveplayer.clickOnCoords(dungeon_special_event_coords)
                time.sleep(2)
                special_event = True
            if inside_dungeon_icon_coords != (0, 0) or inside_dungeon_icon_coords_2 != (0, 0):
                if inside_dungeon_icon_coords_2 != (0, 0):
                    # 56, 176
                    self.send_text_to_bot.send("expand left menu", self.from_python)
                    self.moveplayer.clickOnCoords((52,219))
                inside = True
                break
            time.sleep(1)
            # load_screen_coords = self.moveplayer.founfIconInScreen(
            #     self.img_path + '\\game_items', 'load_screen', 1, False, self.captureWorker.screenshot)
            dungeon_intro_coords = self.moveplayer.founfIconInScreen(
                self.img_path + '\\game_items', 'dungeon_intro', 1, False, self.captureWorker.screenshot, False)
            inside_dungeon_icon_coords = self.moveplayer.founfIconInScreen(
                self.img_path + '\\game_items', 'inside_dungeon_icon', 1, False, self.captureWorker.screenshot, False)
            inside_dungeon_icon_coords_2 = self.moveplayer.founfIconInScreen(
                self.img_path + '\\game_items', 'inside_dungeon_icon_2', 1, False, self.captureWorker.screenshot, False)
            dungeon_special_event_coords = self.moveplayer.founfIconInScreen(
            self.img_path + '\\game_items', 'dungeon_special_event', 1, False, self.captureWorker.screenshot, False)
        if inside:
            if show_msg:
                self.send_text_to_bot.send(
                    "Inside dungeon", self.from_python, "blue")
            if special_event:
                timeout_special_event = time.time()
                while self.moveplayer.checkIfPlayerIsNearTo('portal') is False:
                    self.moveplayer.processing_movement_output(
                        self.movement_special_event[self.dungeon_name][0])
                    time.sleep(0.2)
                    self.processing_movement_output('NK')
                    time.sleep(0.2)
                    if time.time() - timeout_special_event > 30:
                        self.send_text_to_bot.send(
                            "Not found portal, exit dungeon", self.from_python, "red")
                        self.moveplayer.clickOnCoords((713, 134))
                        time.sleep(2)
                        self.moveplayer.clickOnCoords((576, 357))
                        time.sleep(10)
                        return False
                self.moveplayer.pressKey('f')
                self.special_event = True
            return True
        else:
            if show_msg:
                self.send_text_to_bot.send(
                    "Not inside dungeon", self.from_python, "blue")
        return False
    
    def check_if_player_is_in_special_event_dungeon(self):
        dungeon_special_event_coords = self.moveplayer.founfIconInScreen(
            self.img_path + '\\game_items', 'dungeon_special_event', 1, False, self.captureWorker.screenshot, False)
        if dungeon_special_event_coords != (0, 0):
            return dungeon_special_event_coords
        return False
        

    def open_find_party_screen(self):
        loot_coords = self.moveplayer.founfIconInScreen(
            self.img_path + '\\game_items', 'hand_down', 1, False, self.captureWorker.screenshot)
        while loot_coords != (0, 0):
            self.moveplayer.clickOnCoords(loot_coords)
            time.sleep(1)
        door_coords = self.moveplayer.founfIconInScreen(
            self.img_path + '\\game_items', 'hand_up', 4, False, self.captureWorker.screenshot)
        if door_coords == (0, 0):
            self.send_text_to_bot.send(
                "Error finding dungeon door", self.from_python)
            self.threads.resume_thread('CheckIsDead')
            self.threads.pause_thread('Fight')
            return False
        self.threads.pause_thread('Fight')
        self.moveplayer.clickOnCoords(door_coords)
        time.sleep(1)
        return True

    def go_to_dungeon_entrance(self):
        entrance_coords = self.moveplayer.founfIconInScreen(self.img_path + '\\'+self.language+'\\dungeons\\' +
                                                            self.dungeon_name, self.dungeon_name+'_entrance_icon_' + self.language, 4, True)
        # check if entrance_coords is (0,0) and try again
        if entrance_coords == (0, 0):
            self.send_text_to_bot.send(
                "Error finding dungeon entrance", self.from_python)
            self.threads.resume_thread('CheckIsDead')
            time.sleep(1)
            self.moveplayer.pressKey('esc')
            time.sleep(1)
            return False
        self.moveplayer.clickOnCoords(entrance_coords)
        time.sleep(1)
        if self.moveplayer.clickOnNavigateOrTeleport() is False:
            return False
        time.sleep(1)
        self.threads.resume_thread('Fight')
        self.threads.resume_thread('CheckIsDead')
        for i in range(3):
            time.sleep(1)
            self.send_text_to_bot.send(
                'Waiting to teleport to dungeon: ' + str(3 - i), self.from_python)
        self.moveplayer.waitForTheArrivalToSpot()
        door_coords = self.moveplayer.founfIconInScreen(
            self.img_path + '\\game_items', 'hand_up', 1, False, self.captureWorker.screenshot)
        if door_coords == (0, 0):
            if self.movement_in_front_of_door[self.dungeon_name] != None:
                for direction in self.movement_in_front_of_door[self.dungeon_name]:
                    self.moveplayer.processing_movement_output(direction)
                    time.sleep(1)
                    self.moveplayer.processing_movement_output('NK')
        return True
