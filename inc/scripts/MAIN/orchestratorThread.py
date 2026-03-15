import threading
import time

class OrchestratorThread(threading.Thread):
    def __init__(self, threadsObject):
        threading.Thread.__init__(self)
        self.paused = False
        self.stopped = False
        self.threadsObject = threadsObject

    def run(self):
        print('OrchestratorThread run')
        while self.stopped is False:
            # try:
            #     self.threadsObject.printStatusOfAllThreads()
            # except Exception as e:
            #     print('OrchestratorThread runE>PS', str(e))

            if self.paused is True:
                time.sleep(0.5)
                continue
            
            try:
                self.threadsObject.checkStatusOfAllThreads()
            except Exception as e:
                print('OrchestratorThread runE>RR', str(e))

            time.sleep(30)
            

    def pause(self):
        self.paused = True

    def resume(self):
        self.paused = False

    def stop(self):
        self.stopped = True