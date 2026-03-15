import threading
import time
from findLoot import FindLoot
from findImage import RunFindImage
from findObjectInMinimap import FindObjectInMinimap
import gc
from GeomUtil import GeomUtil
import math
from readINI import ReadINIFile


class CheckLoot(threading.Thread):
    def __init__(self, threads, src_window, loot_path, send_text_to_bot, from_python, img_path, moveplayer, cyrangar=False, dungeon=False, fish=False):
        threading.Thread.__init__(self)
        self.loot_path = loot_path
        self.src_window = src_window
        self.moveplayer = moveplayer
        self.stopped = False
        self.player_is_dead = False
        self.paused = False
        self.captureWorker = threads.get_thread('CaptureWorker')
        self.playerPositionInScreen = (480, 325)
        self.fight = threads.get_thread('Fight')
        self.spotWorker = threads.get_thread('SpotWorker')
        self.dungeonWorker = threads.get_thread('DungeonWorker')
        self.in_SPOT = False
        self.in_BESTIARY = False
        self.send_text_to_bot = send_text_to_bot
        self.from_python = from_python
        self.img_path = img_path
        self.memory_clean = False
        self.count_loot = 0
        self.times_to_not_found_loot = 0
        self.last_loottime = None
        self.cyrangar = cyrangar
        self.dungeon = dungeon
        self.loot_method = ReadINIFile(img_path + '\\..\\..\\setup.ini', 'Main', 'LootMethod', 'NonStop')
        if fish:
            self.loot_method = 'Stop'
        if cyrangar:
            self.loot_to_avoid = [
                                        'gold_label_en.png', 
                                        'gold_label_es.png', 
                                        'gold_label_1_en.png',
                                        'gold_label_2_en.png', 
                                        'globe_label_en.png', 
                                        'globe_label_es.png', 
                                        'globe_label_es.png', 
                                        'monstrous_essence.png', 
                                        'essence_label_en.png', 
                                        'essence_label_es.png', 
                                        'gold_label_es.png']
            self.colors_to_find = []
        elif dungeon:
            self.loot_to_avoid = [
                                        'gold_label_en.png', 
                                        'gold_label_es.png', 
                                        'gold_label_1_en.png',
                                        'gold_label_2_en.png', 
                                        'fogs_bane_es.png', 
                                        'fogs_bane_en.png', 
                                        'fogs_bane_label_en.png', 
                                        'fogs_bane_label_es.png', 
                                        'gold_label_es.png'
                                        ]
            self.colors_to_find = ['yellow', 'orange', 'blue']
        else:
            self.loot_to_avoid = [
                                        'gold_label_en.png', 
                                        'gold_label_es.png', 
                                        'gold_label_1_en.png',
                                        'gold_label_2_en.png', 
                                        'globe_label_en.png', 
                                        'globe_label_es.png', 
                                        'globe_label_es.png', 
                                        'globe_label_es.png', 
                                        'fogs_bane_es.png', 
                                        'fogs_bane_en.png', 
                                        'fogs_bane_label_en.png', 
                                        'fogs_bane_label_es.png', 
                                        'gold_label_es.png'
                                        ]
            self.colors_to_find = ['yellow', 'orange', 'blue']

    def pause(self):
        self.paused = True

    def resume(self):
        self.paused = False

    def run(self): 
        print('CheckLoot run 1st time')
        while self.stopped is False:
            if self.paused is True:
                self.times_to_not_found_loot = 0
                if self.memory_clean is True:
                    gc.collect()
                    self.memory_clean = False
                time.sleep(0.5)
                continue
            try:
                self.memory_clean = True
                if self.paused:
                    continue
                response = FindLoot(self.src_window, self.loot_path,
                                    self.captureWorker.screenshot, None, self.loot_to_avoid, self.colors_to_find)
                if self.cyrangar:
                    resp = FindObjectInMinimap(
                self.captureWorker, self.fight, self.moveplayer, self.img_path + '\\game_items', 'minimap_bane', True, 1, False)
                if 'notfound' not in response:
                    self.times_to_not_found_loot = 0
                    if self.last_loottime is not None:
                        if time.time() - self.last_loottime < 10:
                            self.count_loot += 1
                    else:
                        self.last_loottime = time.time()

                    if self.count_loot > 5:
                        self.send_text_to_bot.send(
                            'Loot found 5 times in a row, stopping', self.from_python, 'red')
                        self.count_loot = 0
                        if self.in_SPOT:
                            try:
                                self.spotWorker.resume()
                                self.dungeonWorker.resume()
                            except:
                                pass
                        continue
                    # print('LOOT FOUND spotworker paused')
                    try:
                        self.spotWorker.pause()
                        self.dungeonWorker.pause()
                    except:
                        pass
                    if self.loot_method == 'Stop':
                        self.moveplayer.no_keys()
                        self.moveplayer.releaseAllMovementKeys()
                    self.goToLoot(response)
                else:
                    self.times_to_not_found_loot += 1
                    if self.in_SPOT:
                        try:
                            self.spotWorker.resume()
                            self.dungeonWorker.resume()
                        except:
                            pass
            except Exception as e:
                print(e)
                print("Error checking loot")
            time.sleep(0.5)

    def goToLoot(self, resp):
        # print(resp)
        allKeys = ['orange', 'yellow', 'blue', 'essence_label_',
                   'monstrous_essence', 'globe_label_', 'fogs_bane_', 'fogs_bane_label_']

        for key in resp.keys():
            for key2 in allKeys:
                if key2 in key:
                    movement, distance = self.GetLootPos(
                        resp[key][0], self.playerPositionInScreen)
                    if key2 != 'orange':
                        self.send_text_to_bot.send(
                            'Found ' + str(key2) + ' go: ' + str(movement) + ' distance: ' + str(int(distance)), self.from_python, 'orange')
                    self.moveplayer.processing_movement_output(movement)
                    time.sleep(1)
                    response = RunFindImage(
                        self.src_window, self.img_path + '\\game_items', 'hand_down', self.captureWorker.screenshot, 0.8, False, False)
                    if response['hand_down'] != 'notfound':
                        self.moveplayer.pressKey('f')              
                    if self.in_BESTIARY:
                        self.moveplayer.processing_movement_output('NK')
                        self.moveplayer.processing_movement_output('NK')
                        self.moveplayer.processing_movement_output('NK')
                        time.sleep(1)
                        # move player to reverse direction of positionOfLoot
                        self.moveplayer.processing_reverse_movement_output(movement)
                        time.sleep(1)
                        self.moveplayer.processing_movement_output('NK')
                        self.moveplayer.processing_movement_output('NK')
                        self.moveplayer.processing_movement_output('NK')
                        response = RunFindImage(
                                self.src_window, self.img_path + '\\game_items', 'hand_down', self.captureWorker.screenshot, 0.8, False, False)
                        if response['hand_down'] != 'notfound':
                                self.moveplayer.pressKey('f')
                    # if self.dungeon:
                    if self.loot_method == 'Stop':
                        self.moveplayer.processing_movement_output('NK')


    def GetLootPos(self, object_position, player_position):
        movements = ['→', '↘', '↓', '↙', '←', '↖', '↑', '↗']
        distance = self.moveplayer.get_distance(player_position, object_position)
         # calculate angle between player and object
        delta_x = object_position[0] - player_position[0]
        delta_y = object_position[1] - player_position[1]
        angleInDegrees = math.atan2(
            delta_y, delta_x) * GeomUtil.toDEGREES

        # set angle between 0 and 360
        if angleInDegrees < 0:
            angleInDegrees += 360

        angleInDegrees = int(angleInDegrees)
        angleInDegrees = angleInDegrees + 22
        if angleInDegrees > 360:
            angleInDegrees = angleInDegrees - 360
        angleInDegrees = int(angleInDegrees / 45)
        movement = movements[angleInDegrees]
        # print('movement-->', movement)
        # self.send_text_to_bot.send("El jugador debe moverse hacia " + movement + " para alcanzar la puerta", self.from_python)
        # print('movement: ' + movement)
        

            
        # return movement and distance+
        return movement, distance

        # diff_x = lootPos[0] - playerPos[0]
        # diff_y = lootPos[1] - playerPos[1]
        # direction = ''
        # if diff_x > 0:
        #     if diff_y > 0:
        #         direction = 'SouthEast'
        #     elif diff_y < 0:
        #         direction = 'NorthEast'
        #     else:
        #         direction = 'East'
        # elif diff_x < 0:
        #     if diff_y > 0:
        #         direction = 'SouthWest'
        #     elif diff_y < 0:
        #         direction = 'NorthWest'
        #     else:
        #         direction = 'West'
        # else:
        #     if diff_y > 0:
        #         direction = 'South'
        #     elif diff_y < 0:
        #         direction = 'North'
        #     else:
        #         direction = 'North'
        # return direction

    def stop(self):
        self.stopped = True
