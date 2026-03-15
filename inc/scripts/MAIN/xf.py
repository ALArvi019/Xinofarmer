from http.server import BaseHTTPRequestHandler, HTTPServer
from fish import RunFish
from findImage import RunFindImage
from findLoot import FindLoot
from farming_spot import runFarmingSpot
from run_dungeon import runDungeon
from fishing_new import runFishNew
from endless_mode import runEndlessMode
from sendTextToBot import SendTextToBot
from movePlayer import moveplayer
from threads import Threads
# from findCoords import RunFindCoords
# from findPath import RunFindPath
# from goTo import RunGoTo
# from dungeon import RunDungeon
import sys
import threading

send_text_to_bot = SendTextToBot()
# SET TRUE ONLY FOR DEVELOPMENT
from_python = False

farmingspot = None
rundungeon = None
endlessMode = None
fishingNew = None

token = sys.argv[1]
versionXF = '1.7.6'

class MyRequestHandler(BaseHTTPRequestHandler):

    def sendOKResponse(self, response):
        try:
            # send 200 OK response to client with response
            self.send_response(200)
            # send headers
            self.send_header('Content-type', 'text/plain')
            self.end_headers()
            # send response
            # print('Send->:', response)
            self.wfile.write(response.encode('utf-8'))
        except Exception as e:
            print('Error sending response:', e)
            # return 423 Locked
            self.send_error(423, "Locked")
        return

    def do_POST(self):
        global send_text_to_bot
        global from_python
        global farmingspot
        global rundungeon
        global endlessMode
        global fishingNew
        try:
            content_length = int(self.headers.get('Content-Length', 0))
            post_data = self.rfile.read(content_length)
            datos = post_data.decode("utf-8")
            data = datos.replace('\r', '').replace('\n', '')
            print("Datos recibidos:", data)

            if data == 'XF_2ndScript_Start':
                response = 'XF_2ndScript_Start'
                # print('Send:', response)
                self.sendOKResponse(response)
                return
            if data == 'XF_2ndScript_Version':
                response = versionXF
                # print('Send:', response)
                self.sendOKResponse(response)
                return
            command = data.split('|')[0]
            if command and command == 'XF_2ndScript_chUser':
                username = data.split('|')[1]
                if username is not None:
                    threads = Threads()
                    if threads.get_thread('CustomSocketIO') is None:
                        customsocketio = threads.create_thread(
                            'CustomSocketIO', send_text_to_bot, from_python, username)
                        threads.resume_thread('CustomSocketIO')
                else:
                    print('The username is empty')
                response = 'OK'
                self.sendOKResponse(response)
                return
            if command and command == 'fromXF':
                # print('Command:', command)
                action = data.split('|')[1]
                # print('Action:', action)
                if action == 'fish':
                    src_window = data.split('|')[2]
                    images_path = data.split('|')[3]
                    fish_type = data.split('|')[4]
                    response = RunFish(src_window, images_path, fish_type)
                    self.sendOKResponse(response)
                    return
                if action == 'findimage':
                    src_window = data.split('|')[2]
                    images_path = data.split('|')[3]
                    image_name = data.split('|')[4]
                    threshold = data.split('|')[5]
                    gray = data.split('|')[6]
                    if gray == 'True':
                        gray = True
                    else:
                        gray = False
                    response = RunFindImage(
                        src_window, images_path, image_name, None, threshold, True, gray)
                    # print('response:', response)
                    self.sendOKResponse(str(response))
                    return
                if action == 'findloot':
                    src_window = data.split('|')[2]
                    images_path = data.split('|')[3]
                    images_to_search = data.split('|')[4]
                    if images_to_search == 'None':
                        images_to_search = None
                    response = FindLoot(
                        src_window, images_path, None, images_to_search)
                    # print('response:', response)
                    # convert ' to " in response
                    response = str(response).replace("'", '"')
                    self.sendOKResponse(response)
                    return
                if action == 'farmingspot':
                    src_window = data.split('|')[2]
                    inc_path = data.split('|')[3]
                    map_name = data.split('|')[4]
                    language = data.split('|')[5]
                    acceptPartyInvite = data.split('|')[6]
                    telegramConfig = data.split('|')[7]
                    username = data.split('|')[8]
                    CheckPartyLeader = data.split('|')[9]
                    CheckBestyaryEveryIfNotification = data.split('|')[10]
                    CheckBestyaryEveryIfNotificationNotFound = data.split('|')[11]
                    modelname = data.split('|')[12]
                    if acceptPartyInvite == 'Yes':
                        acceptPartyInvite = True
                    else:
                        acceptPartyInvite = False
                    if telegramConfig == 'True':
                        telegramConfig = True
                    else:
                        telegramConfig = False
                    if CheckPartyLeader == 'Yes':
                        CheckPartyLeader = True
                    else:
                        CheckPartyLeader = False
                    print('map_name:', map_name)
                    self.sendOKResponse('OK')
                    if farmingspot is None:
                        farmingspot = runFarmingSpot(src_window, inc_path, map_name, send_text_to_bot, from_python,
                                                     language, acceptPartyInvite, False, True, telegramConfig, username, CheckPartyLeader, CheckBestyaryEveryIfNotification, CheckBestyaryEveryIfNotificationNotFound, modelname)
                        farmingspot.RunFarmingSpot()
                    return
                if action == 'fishingNew':
                    src_window = data.split('|')[2]
                    images_path = data.split('|')[3]
                    self.sendOKResponse('OK')
                    fishing = runFishNew(
                        src_window, images_path, send_text_to_bot, from_python)
                    fishing.RunFishNew()
                    return
                # Local $response = XF_2ndScript_Send("fromXF|dungeon|" & $Setup_Main_VMName & "|" & $XF_image_folder & "|" & $Setup_Dungeon_name & "|" & $gameLanguage)
                if action == 'dungeon':
                    src_window = data.split('|')[2]
                    images_path = data.split('|')[3]
                    dungeon_name = data.split('|')[4]
                    language = data.split('|')[5]
                    team_solo = data.split('|')[6]
                    time_to_exit = data.split('|')[7]
                    time_to_wait_party = data.split('|')[8] 
                    time_to_exit = int(time_to_exit)
                    time_to_wait_party = int(time_to_wait_party)
                    replay_dungeon = data.split('|')[9]
                    # check if time_to_exit is number
                    if isinstance(time_to_exit, int) is False:
                        time_to_exit = 600
                    # check if time_to_wait_party is number
                    if isinstance(time_to_wait_party, int) is False:
                        time_to_wait_party = 400
                    if team_solo == 'Team':
                        team_solo = False
                    else:
                        team_solo = True
                    if replay_dungeon == 'YES':
                        replay_dungeon = True
                    else:
                        replay_dungeon = False
                    self.sendOKResponse('OK')
                    rundungeon = runDungeon(
                        src_window, images_path, dungeon_name, language, send_text_to_bot, from_python, team_solo, time_to_exit, time_to_wait_party, replay_dungeon)
                    rundungeon.RunDungeon()
                if action == 'endless':
                    src_window = data.split('|')[2]
                    images_path = data.split('|')[3]
                    language = data.split('|')[4]
                    telegramConfig = data.split('|')[5]
                    username = data.split('|')[6]
                    if telegramConfig == 'True':
                        telegramConfig = True
                    else:
                        telegramConfig = False
                    self.sendOKResponse('OK')
                    endlessMode = runEndlessMode(
                        src_window, images_path, send_text_to_bot, from_python, language, telegramConfig, username)
                    endlessMode.RunENdlessMode()
                    return
                if action == 'stopfarmingspot':
                    try:
                        if farmingspot is not None or endlessMode is not None or rundungeon is not None:
                            src_window = data.split('|')[2]
                            print('threads12:', threading.enumerate())
                            # foreach al threads and stop them
                            for thread in threading.enumerate():
                                th2 = thread.__str__()
                                th2 = th2.split('(')[0]
                                th2 = th2.split('<')[1]
                                if thread.name != 'MainThread':
                                    try:
                                        thread.pause()
                                        print('pause thread:', th2)
                                        # thread.join()
                                    except:
                                        pass
                            Moveplayer = moveplayer(src_window)
                            Moveplayer.MoveRandomly()
                            Moveplayer.processing_movement_output('NK')
                            Moveplayer.processing_movement_output('NK')
                            Moveplayer.processing_movement_output('NK')
                            farmingspot = None
                        self.sendOKResponse('OK')
                        return
                    except Exception as e:
                        print('Error stopping farmingspot:', e)
                        self.sendOKResponse('OK')
                        return

                # if action == 'getcoords':
                #     src_window = data.split('|')[2]
                #     images_path = data.split('|')[3]
                #     image_name = data.split('|')[4]
                #     # remove end of line in image_name
                #     image_name = image_name.replace('\r', '').replace('\n', '')
                #     response = RunFindCoords(src_window, images_path, image_name)
                #     # print('response:', response)
                #     response = response + '@@@@'
                #     conn.send(response.encode('utf-8'))
                # if action == 'findpath':
                #     images_path = data.split('|')[2]
                #     image_name = data.split('|')[3]
                #     start_x = data.split('|')[4]
                #     start_y = data.split('|')[5]
                #     end_x = data.split('|')[6]
                #     end_y = data.split('|')[7]
                #     # remove end of line in end_y
                #     end_y = end_y.replace('\r', '').replace('\n', '')
                #     response = RunFindPath(images_path, image_name, start_x, start_y, end_x, end_y)
                #     # print('response:', response)
                #     response = response + '@@@@'
                #     conn.send(response.encode('utf-8'))
                # if action == 'goto':
                #     src_window = data.split('|')[2]
                #     images_path = data.split('|')[3]
                #     image_name = data.split('|')[4]
                #     end_x = data.split('|')[5]
                #     end_y = data.split('|')[6]
                #     # remove end of line in end_y
                #     end_y = end_y.replace('\r', '').replace('\n', '')
                #     response = RunGoTo(src_window, images_path, image_name, end_x, end_y)
                #     print('response:', response)
                #     response = response + '@@@@'
                #     conn.send(response.encode('utf-8'))
                # if action == 'dungeon':
                #     src_window = data.split('|')[2]
                #     images_path = data.split('|')[3]
                #     image_name = data.split('|')[4]
                #     # remove end of line in end_y
                #     image_name = image_name.replace('\r', '').replace('\n', '')
                #     response = RunDungeon(src_window, images_path, image_name)
                #     print('response:', response)
                #     response = response + '@@@@'
                #     conn.send(response.encode('utf-8'))
            else:
                self.send_error(400, "Unknown command")
        except Exception as e:
            print('ErrorXF:', e)
            # rturn 423 Locked
            self.send_error(423, "Locked")
        return

    def do_GET(self):
        self.send_error(400, "Not supported")

    def do_PUT(self):
        self.send_error(400, "Not supported")

    def do_DELETE(self):
        self.send_error(400, "Not supported")


if token == 'fromXF':
    server_address = ('', 9000)
    httpd = HTTPServer(server_address, MyRequestHandler)
    print('Listening on port 9000...')
    httpd.serve_forever()
