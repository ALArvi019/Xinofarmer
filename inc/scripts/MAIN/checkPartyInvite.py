import threading
import time
from findImage import RunFindImage
import gc
import cv2 as cv


class CheckPartyInvite(threading.Thread):
    def __init__(self, threads, src_window, wantPartyInvite, language, img_farm_path, send_text_to_bot, from_python, fileName, moveplayer, checkPartyLeader, checkIfPlayerIsInsideRaid = True):
        threading.Thread.__init__(self)
        self.moveplayer = moveplayer
        self.stopped = False
        self.paused = False
        self.wantPartyInvite = wantPartyInvite
        self.language = language
        self.captureWorker = threads.get_thread('CaptureWorker')
        self.src_window = src_window
        self.img_path = img_farm_path
        self.send_text_to_bot = send_text_to_bot
        self.from_python = from_python
        self.fileName = fileName
        self.countCheckPartyLeader = 0
        self.threads = threads
        self.pass_leadter_to_2nd_player_count = 0
        self.memory_clean = False
        self.checkPartyLeader = checkPartyLeader
        self.checkIfPlayerIsInsideRaidcheck = checkIfPlayerIsInsideRaid
        # self.debug_image = False

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
            # if 1 == 1:
            try:
                self.memory_clean = True
                self.checkPartyInvitePopup()
                if self.checkIfPlayerIsInsideRaid():
                    # check if the player is the leader of the party every 30 seconds
                    if self.countCheckPartyLeader > 5:
                        self.countCheckPartyLeader = 0
                        if self.checkPartyLeader:
                            print("Checking if player is party leader")
                            self.checkIfPlayerIsPartyLeader()
            except Exception as e:
                print(e)
                print("Error checking party invite")
            self.countCheckPartyLeader += 1
            # reset count avoid memory leak
            if self.countCheckPartyLeader > 10:
                self.countCheckPartyLeader = 0
            time.sleep(5)

    def checkPartyInvitePopup(self):
        try:
            # keys = key_check()
            # if 'P' in keys:
            #     if self.debug_image:
            #         self.debug_image = False
            #     else:
            #         self.debug_image = True

            # if self.debug_image:
            #     cv.imshow("screenshot", self.captureWorker.screenshot)
            #     cv.waitKey(1)

            response = RunFindImage(
                self.src_window, self.img_path, 'party_invite_' + self.language, self.captureWorker.screenshot)
            if response['party_invite_' + self.language] == 'notfound':
                return False
            else:
                PositionOFBS_x = response['party_invite_' +
                                          self.language].split('|')[0]
                PositionOFBS_y = response['party_invite_' +
                                          self.language].split('|')[1]
                # save self.captureWorker.screenshot screenshot+timestamp
                # cv.imwrite('screenshot' + str(time.time()) +
                #         '.png', self.captureWorker.screenshot)
                try:
                    response = RunFindImage(
                        self.src_window, self.img_path, 'party_invite_' + self.fileName + '_' + self.language, self.captureWorker.screenshot)
                except Exception as e:
                    response['party_invite_' + self.fileName + '_' + self.language] = 'notfound'
                response2 = RunFindImage(
                    self.src_window, self.img_path + '\..\..\game_items', 'bestiary_message_' + self.language, self.captureWorker.screenshot)
                if response['party_invite_' + self.fileName + '_' + self.language] == 'notfound' and response2['bestiary_message_' + self.language] == 'notfound':
                    self.send_text_to_bot.send(
                        "Party invite for " + self.fileName + " NOT found", self.from_python, 'red')
                    self.send_text_to_bot.send(
                        "Declining party invite", self.from_python, 'red')
                    self.moveplayer.clickOnCoords(
                        (int(PositionOFBS_x) - 40, int(PositionOFBS_y) + 10))
                    return False
                else:
                    self.send_text_to_bot.send(
                        "Party invite popup found", self.from_python, 'green')
                    if self.wantPartyInvite:
                        self.send_text_to_bot.send(
                            "Accepting party invite", self.from_python, 'green')
                        # (PositionOFBS_x, PositionOFBS_y) + (85, 35)
                        self.moveplayer.clickOnCoords(
                            (int(PositionOFBS_x) + 85, int(PositionOFBS_y) + 10))
                    else:
                        self.send_text_to_bot.send(
                            "Declining party invite", self.from_python, 'red')
                        # (PositionOFBS_x, PositionOFBS_y) + (251, 34)
                        self.moveplayer.clickOnCoords(
                            (int(PositionOFBS_x) - 40, int(PositionOFBS_y) + 10))
                return True
        except Exception as e:
            print(e)
            return False

    def checkIfPlayerIsInsideRaid(self):
        partyresponse = RunFindImage(
            self.src_window, self.img_path + '\..\..\game_items', 'party', self.captureWorker.screenshot)
        raidresponse = RunFindImage(
            self.src_window, self.img_path + '\..\..\game_items', 'assault_icon', self.captureWorker.screenshot)
        if partyresponse['party'] == 'notfound' and raidresponse['assault_icon'] == 'notfound':
            return False
        elif partyresponse['party'] != 'notfound' and raidresponse['assault_icon'] == 'notfound':
            return True
        elif partyresponse['party'] == 'notfound' and raidresponse['assault_icon'] != 'notfound':
            if self.checkIfPlayerIsInsideRaidcheck:
                self.threads.pause_all_threads(
                    ['CaptureWorker', 'CheckPartyInvite', 'CheckIsDead', 'CheckLife'])
                self.moveplayer.processing_movement_output('NK')
                self.send_text_to_bot.send(
                    "Player is inside raid", self.from_python, 'green')
                self.send_text_to_bot.send(
                    "Exiting raid", self.from_python, 'green')
                time.sleep(1)
                self.moveplayer.clickOnCoords((60, 78))
                time.sleep(1)
                # 130, 261
                self.moveplayer.clickOnCoords((130, 261))
                time.sleep(1)
                # 579, 361
                self.moveplayer.clickOnCoords((579, 361))
                self.threads.resume_all_threads()
                return False
            else:
                return True

    def checkIfPlayerIsPartyLeader(self):
        response = RunFindImage(
            self.src_window, self.img_path + '\..\..\game_items', 'party_leader', self.captureWorker.screenshot, 0.95)
        if response['party_leader'] == 'notfound':
            return False
        else:
            self.threads.pause_all_threads(
                ['CaptureWorker', 'CheckPartyInvite', 'CheckIsDead', 'CheckLife'])
            self.moveplayer.processing_movement_output('NK')
            self.send_text_to_bot.send(
                "Player is party leader", self.from_python, 'green')
            self.send_text_to_bot.send(
                "Passing party leader to 2nd player", self.from_python, 'green')
            time.sleep(1)
            # 130, 69
            self.moveplayer.clickOnCoords((130, 69))
            time.sleep(1)
            response = RunFindImage(
                self.src_window, self.img_path + '\..\..\game_items', 'make_leader_' + self.language, self.captureWorker.screenshot)
            if response['make_leader_' + self.language] == 'notfound':
                self.send_text_to_bot.send(
                    "Error passing party leader to 2nd player, maybe disconnected", self.from_python, 'red')
                self.pass_leadter_to_2nd_player_count += 1
                self.send_text_to_bot.send('Cheking ' + str(self.pass_leadter_to_2nd_player_count) + ' of 10', self.from_python)
                if self.pass_leadter_to_2nd_player_count > 10:
                    self.send_text_to_bot.send(
                        "Delete 2nd player from party", self.from_python, 'red')
                    self.delete2ndPlayerFromParty()
                self.threads.resume_all_threads()
                return False
            else:
                PositionOFBS_x = response['make_leader_' +
                                          self.language].split('|')[0]
                PositionOFBS_y = response['make_leader_' +
                                          self.language].split('|')[1]
                self.moveplayer.clickOnCoords(
                    (int(PositionOFBS_x), int(PositionOFBS_y)))
                time.sleep(1)
            self.threads.resume_all_threads()
            return True
        
    def delete2ndPlayerFromParty(self):
        self.moveplayer.clickOnCoords((132, 69))
        time.sleep(1)
        response = RunFindImage(
            self.src_window, self.img_path + '\..\..\game_items', 'delete_player_' + self.language, self.captureWorker.screenshot)
        if response['delete_player_' + self.language] == 'notfound':
            return False
        else:
            PositionOFBS_x = response['delete_player_' +
                                        self.language].split('|')[0]
            PositionOFBS_y = response['delete_player_' +
                                        self.language].split('|')[1]
            self.moveplayer.clickOnCoords(
                (int(PositionOFBS_x), int(PositionOFBS_y)))
            time.sleep(1)
            self.pass_leadter_to_2nd_player_count = 0
            return True

    def stop(self):
        self.stopped = True
