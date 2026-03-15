from captureWorker import CaptureWorker
from checkLife import CheckLife
from checkIsDead import CheckIsDead
from fight import Fight
from checkLoot import CheckLoot
from spotWorker import SpotWorker
from dungeonWorker import DungeonWorker
from blacksmith import Blacksmith
from checkPartyInvite import CheckPartyInvite
from checkEssences import CheckEssences
from checkMessages import CheckMessages
from customsocketio import CustomSocketIO
from farmingSpotThread import FarmingSpotThread
from runDungeonThread import RunDungeonThread
from runDungeonOrchestration import RunDungeonOrchestration
from orchestratorThread import OrchestratorThread
from checkDungeonTime import CheckDungeonTime
from endlessModeThread import EndlessModeThread
from checkCyrangarEnd import CheckCyrangarEnd
from endlessmode_check_line import EndlessModeCheckLine
from endlessmode_check_door_attack import EndlessModeChecDoorAttack
from checkDungeonLoot import CheckDungeonLoot
from checkDungeonMandatoryStep import CheckDungeonMandatoryStep
from checkActualMap import CheckActualMap
from fishNewThread import FishNewThread
import threading
import sys
import time


class Threads:
    def __init__(self, moveplayer=None):
        self.conditionsRepeat = []
        self.md5StatusOfallThreads = []
        self.screenshothash = []
        self.moveplayer = moveplayer
        self.threads = {}
        self.list_of_threads_to_avoid = [
            'MainThread',
            '_MainThread',
            'CustomSocketIO',
            'FarmingSpotThread',
            'RunDungeonThread',
            'OrchestratorThread'
        ]
        for thread in threading.enumerate():
            th2 = thread.__str__()
            th2 = th2.split('(')[0]
            th2 = th2.split('<')[1]
            if th2 == 'FarmingSpotThread' or th2 not in self.list_of_threads_to_avoid or th2 == 'RunDungeonThread':
                self.threads[th2] = thread

    def create_thread(self, thread_name, *args):
        thread_found = False
        for thread_name1, thread in self.threads.items():
            if thread_name == thread_name1:
                # print('create_thread-thread_found:', thread_name)
                thread_found = True
                break
        if thread_found is True:
            return thread
        thread = getattr(sys.modules[__name__], thread_name)(*args)
        self.threads[thread_name] = thread
        # print('create_thread:', self.threads.keys())
        return thread

    def stop_all_threads(self):
        # print all threads keys
        # print('stop_all_threads:', self.threads.keys())
        for thread_name, thread in self.threads.items():
            if thread_name not in self.list_of_threads_to_avoid:
                try:
                    thread.stop()
                except Exception as e:
                    print('stop_all_threadsE>RR', str(e))
                    print('thread_name: ' + thread_name)
                # print('stop thread:', thread_name)

    def join_all_threads(self):
        for thread_name, thread in self.threads.items():
            if thread_name not in self.list_of_threads_to_avoid:
                try:
                    thread.join()  
                except Exception as e:
                    print('join_all_threadsE>RR', str(e))
                    print('thread_name: ' + thread_name)

    def pause_all_threads(self, avoid_thread_name_array=None):
        # print('DEBUG: pause_all_threads-----------------------------------')
        # print('DEBUG: avoid_thread_name_array: ' + str(avoid_thread_name_array))
        # print('DEBUG: self.list_of_threads_to_avoid: ' + str(self.list_of_threads_to_avoid))
        # print('DEBUG: self.threads: ' + str(self.threads.keys()))

        for thread_name, thread in self.threads.items():
            avoid_this_thread = False
            for avoid_thread in self.list_of_threads_to_avoid:
                if thread_name == avoid_thread:
                    avoid_this_thread = True

            if avoid_thread_name_array is not None:
                if isinstance(avoid_thread_name_array, str):
                    # convert in array
                    avoid_thread_name_array = [avoid_thread_name_array]

                # add CheckIsDead if not in array
                if 'CheckIsDead' not in avoid_thread_name_array:
                    avoid_thread_name_array.append('CheckIsDead')

                if 'OrchestratorThread' not in avoid_thread_name_array:
                    avoid_thread_name_array.append('OrchestratorThread')

                if 'CheckCyrangarEnd' not in avoid_thread_name_array:
                    avoid_thread_name_array.append('CheckCyrangarEnd')

                for avoid_thread in avoid_thread_name_array:
                    if thread_name == avoid_thread:
                        avoid_this_thread = True

            if avoid_this_thread is False:
                # print('pause_all_threads:', thread_name)
                try:
                    thread.pause()
                except Exception as e:
                    print('pause_all_threadsE>RR', str(e))
                    print('thread_name: ' + thread_name)

    def resume_all_threads(self):
        for thread_name, thread in self.threads.items():
            for thread_name2 in self.list_of_threads_to_avoid:
                if thread_name == thread_name2:
                    break
            else:
                # print('resume_all_threads:', thread_name)
                try:
                    thread.resume()
                except Exception as e:
                    print('resume_all_threadsE>RR', str(e))
                    print('thread_name: ' + thread_name)

    def pause_thread(self, thread_name):
        thread_found = False
        for thread_name1, thread in self.threads.items():
            if thread_name == thread_name1:
                thread_found = True
                break
        if thread_found is True and thread_name not in self.list_of_threads_to_avoid:
            try:
                thread.pause()
            except Exception as e:
                print('pause_threadE>RR', str(e))
                print('thread_name: ' + thread_name)

    def stop_thread(self, thread_name):
        thread_found = False
        for thread_name1, thread in self.threads.items():
            if thread_name == thread_name1:
                thread_found = True
                break
        if thread_found is True and thread_name not in self.list_of_threads_to_avoid:
            try:
                thread.stop()
            except Exception as e:
                print('stop_threadE>RR', str(e))
                print('thread_name: ' + thread_name)

    def join_thread(self, thread_name):
        thread_found = False
        for thread_name1, thread in self.threads.items():
            if thread_name == thread_name1:
                thread_found = True
                break
        if thread_found is True and thread_name not in self.list_of_threads_to_avoid:
            try:
                thread.join()
            except Exception as e:
                print('join_threadE>RR', str(e))
                print('thread_name: ' + thread_name)

    def resume_thread(self, thread_name):
        thread_found = False
        for thread_name1, thread in self.threads.items():
            if thread_name == thread_name1:
                thread_found = True
                break
        # print('\033[92m' + thread_name + '\033[0m')
        # print('thread_name-->:', thread_name)
        # print('thread_found-->:', thread_found)
        # print('self.list_of_threads_to_avoid-->:', self.list_of_threads_to_avoid)
        # print('thread_found-->:', thread_found)
        if (thread_found is True and thread_name not in self.list_of_threads_to_avoid) or \
            (thread_found is True and thread_name == 'FarmingSpotThread') or \
            (thread_found is True and thread_name == 'OrchestratorThread') or \
            (thread_found is True and thread_name == 'RunDungeonThread') or \
                (thread_found is True and thread_name == 'CustomSocketIO'):
            # try:
            #     print('resume_thread:', thread_name + ' is alive: ' + str(thread.is_alive()))
            # except Exception as e:
            #     print('resume_threadE>RR', str(e))

            if thread.is_alive() is False:
                # print('thread ' + thread_name + ' is not alive, starting it')
                try:
                    thread.start()
                except Exception as e:
                    print('resume_threadE>RR', str(e))
                    print('thread_name: ' + thread_name)
                try:
                    thread.resume()
                except Exception as e:
                    print('resume_threadE1>RR', str(e))
                    print('thread_name: ' + thread_name)
            else:
                # print('thread ' + thread_name + ' is alive, resuming it')
                try:
                    thread.resume()
                except Exception as e:
                    print('resume_threadE>RR', str(e))
                    print('thread_name: ' + thread_name)
            # print in yellow "-----------------"
            # print('\033[93m' + thread_name + '\033[0m')

    def start_thread(self, thread_name):
        thread_found = False
        for thread_name1, thread in self.threads.items():
            if thread_name == thread_name1:
                thread_found = True
                break
        if thread_found is True and thread_name not in self.list_of_threads_to_avoid:
            try:
                thread.start()
            except Exception as e:
                print('start_threadE>RR', str(e))
                print('thread_name: ' + thread_name)

    def get_thread(self, thread_name):
        thread_found = False
        for thread_name1, thread in self.threads.items():
            if thread_name == thread_name1:
                thread_found = True
                break
        if thread_found is True:
            return thread
        return None

    def runAgain(self, mainThread="FarmingSpotThread"):
        if self.get_thread('CheckIsDead').player_is_dead is False:
            self.pause_all_threads(['CheckIsDead', 'OrchestratorThread'])
            if mainThread == 'FarmingSpotThread':
                time.sleep(5)
            self.get_thread(mainThread).resume()
        else:
            print('runAgain not execute, player is dead')
            time.sleep(10)
            self.runAgain(mainThread)

    def wait_until_thread_initialized(self, thread_name):
        while self.get_thread(thread_name) is None:
            print('wait_until_thread_initialized: ' + thread_name)
            print('self.threads.keys(): ' + str(self.threads.keys()))
            time.sleep(1)

    def printStatusOfAllThreads(self):
        print('actual time: ' + str(time.time()))
        print('---------------------------------------------------------------------')
        for thread_name, thread in self.threads.items():
            # if thread.paused is True print True in red
            try:
                if thread.paused is True:
                    print('thread_name: ' + thread_name + ' is paused: ' +
                        '\033[91m' + str(thread.paused) + '\033[0m')
                else:
                    # print in green
                    print('thread_name: ' + thread_name + ' is paused: ' +
                        '\033[92m' + str(thread.paused) + '\033[0m')
            except Exception as e:
                print('printStatusOfAllThreadsE>RR', str(e))
                print('thread_name: ' + thread_name)
        print('---------------------------------------------------------------------')

    def checkStatusOfAllThreads(self):
        conditionsToExecuteRunAgain = [
            {
                'conditions': {
                    'CheckIsDead': True,
                },
                'numberOfRepeat': 3
            },
            {
                'conditions': {
                    'OrchestratorThread': True,
                },
                'numberOfRepeat': 1
            },
            {
                'conditions': {
                    'CheckEssences': True,
                    'Blacksmith': True,
                },
                'numberOfRepeat': 3
            },
            {
                'conditions': {
                    'FarmingSpotThread': True,
                    'SpotWorker': True,
                },
                'numberOfRepeat': 20
            },
        ]

        try:
            Actualmd5 = ''
            for thread_name, thread in self.threads.items():
                Actualmd5 += str(thread_name) + str(thread.paused)

            Actualmd5 = hash(Actualmd5)

            # save the last 10 md5
            self.md5StatusOfallThreads.append(Actualmd5)
            if len(self.md5StatusOfallThreads) > 10:
                self.md5StatusOfallThreads.pop(0)
        except Exception as e:
            print('checkStatusOfAllThreadsE>RR', str(e))

        # save the last 10 screenshot hash
        # self.get_thread('CaptureWorker').screenshot
        actualimage = self.get_thread('CaptureWorker').screenshot
        actualMd5image = ''
        if actualimage is not None:
            actualMd5image = hash(str(actualimage.tolist()))
            # save the last 10 screenshot hash
            self.screenshothash.append(actualMd5image)

        if len(self.screenshothash) > 10:
            self.screenshothash.pop(0)

        # print('len(self.screenshothash)' + str(len(self.screenshothash)))
        # print('len(self.md5StatusOfallThreads)' + str(len(self.md5StatusOfallThreads)))
        # print('len(set(self.screenshothash))' + str(len(set(self.screenshothash))))
        # print('len(set(self.md5StatusOfallThreads))' + str(len(set(self.md5StatusOfallThreads))))

        # check if the last 10 md5 are the same
        if len(self.screenshothash) >= 10 and len(self.md5StatusOfallThreads) >= 10 and len(set(self.md5StatusOfallThreads)) == 1 and len(set(self.screenshothash)) == 1:
            print('All threads are paused, runAgain')
            self.runAgain()

        for position, condition in enumerate(conditionsToExecuteRunAgain):
            # check if self.conditionsRepeat has enough elements, add 0 if necessary
            if position >= len(self.conditionsRepeat):
                self.conditionsRepeat.append(0)

            tmpRepeatConditions = self.conditionsRepeat[position]

            numberOffulfilled = 0
            for condition_thread_name, condition_paused_status in condition['conditions'].items():
                for thread_name, thread in self.threads.items():
                    if thread_name == condition_thread_name and thread.paused == condition_paused_status:
                        numberOffulfilled += 1

                if numberOffulfilled == len(condition['conditions']):
                    self.conditionsRepeat[position] += 1

            if tmpRepeatConditions == self.conditionsRepeat[position]:
                self.conditionsRepeat[position] = 0

            # print key and value of self.conditionsRepeat
            for key, value in enumerate(self.conditionsRepeat):
                if key == position:
                    print('self.conditionsRepeat[' + str(key) + ']: ' + str(value) + ' of ' + str(condition['numberOfRepeat']))

            if self.conditionsRepeat[position] == condition['numberOfRepeat']:
                print('Condition number ' + str(position) + ' fulfilled, runAgain')
                self.conditionsRepeat[position] = 0
                self.runAgain()
                break
    
    def check_if_all_threads_paused(self, avoid_thread_name_array=None):
        for thread_name, thread in self.threads.items():
            avoid_this_thread = False
            for avoid_thread in self.list_of_threads_to_avoid:
                if thread_name == avoid_thread:
                    avoid_this_thread = True

            if avoid_thread_name_array is not None:
                if isinstance(avoid_thread_name_array, str):
                    # convert in array
                    avoid_thread_name_array = [avoid_thread_name_array]

                # add CheckIsDead if not in array
                if 'CheckIsDead' not in avoid_thread_name_array:
                    avoid_thread_name_array.append('CheckIsDead')

                if 'OrchestratorThread' not in avoid_thread_name_array:
                    avoid_thread_name_array.append('OrchestratorThread')

                if 'CheckCyrangarEnd' not in avoid_thread_name_array:
                    avoid_thread_name_array.append('CheckCyrangarEnd')

                for avoid_thread in avoid_thread_name_array:
                    if thread_name == avoid_thread:
                        avoid_this_thread = True

            if avoid_this_thread is False:
                if thread.paused is False:
                    return False
                
        return True