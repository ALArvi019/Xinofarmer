
import threading
import time
import copy


class CheckDungeonMandatoryStep(threading.Thread):
    def __init__(self, threads, src_windows, send_text_to_bot, from_python, moveplayer, img_path, dungeon_name, language, solo_mode):
        threading.Thread.__init__(self)
        self.stopped = False
        self.is_running = True
        self.paused = False
        self.threads = threads
        self.send_text_to_bot = send_text_to_bot
        self.from_python = from_python
        self.captureWorker = threads.get_thread('CaptureWorker')
        self.RunDungeonOrchestration = threads.get_thread(
            'RunDungeonOrchestration')
        self.RunDungeonThread = threads.get_thread('RunDungeonThread')
        self.moveplayer = moveplayer
        self.img_path = img_path
        self.src_window = src_windows
        self.dungeon_name = dungeon_name
        self.language = language
        self.solo_mode = solo_mode
        self.step_part_order = {
            "before_start": 1,
            "in_progress": 2,
            "after_end": 3
        }
        self.feedback_order = {
            "before_feedback": 1,
            "in_progress": 2,
            "after_feedback": 3
        }
        self.dungeon_images = None

    def pause(self):
        self.paused = True

    def resume(self):
        self.paused = False

    def stop(self):
        self.stopped = True

    def run(self):
        print(
            f"\033[1;33;40m [CHECK DUNGEON MANDATORY STEP] \033[1;37;40m Starting check dungeon mandatory step")
        if self.solo_mode is True:
            keyToUse = "solo"
        else:
            keyToUse = "party"
        while self.stopped is False:
            # if 1 == 1:
            try:
                if self.paused is True:
                    time.sleep(0.5)
                    continue

                # print in yellow
                # print(
                #     f"\033[1;33;40m [CHECK DUNGEON MANDATORY STEP] \033[1;37;40m Checking {self.dungeon_name}")
                # print(
                #     f"\033[1;33;40m [CHECK DUNGEON MANDATORY STEP] \033[1;37;40m Actual step: {self.RunDungeonOrchestration.dungeon_imagesRDO}")
                # print(
                #     f"\033[1;33;40m [CHECK DUNGEON MANDATORY STEP] \033[1;37;40m Actual step: {self.dungeon_images}")

                if self.dungeon_images is None:
                    self.dungeon_images = copy.deepcopy(self.RunDungeonOrchestration.dungeon_imagesRDO)

                if self.dungeon_images is None:
                    time.sleep(0.5)
                    continue

                # check if dungeon is in list
                if self.dungeon_name not in self.dungeon_images:
                    print(
                        f"\033[1;31;40m [CHECK DUNGEON MANDATORY STEP] Dungeon {self.dungeon_name} not found in list \033[1;37;40m")
                    self.pause()
                    

                # check if dungeon has steps
                if len(self.dungeon_images[self.dungeon_name][keyToUse]) == 0:
                    print(
                        f"\033[1;31;40m [CHECK DUNGEON MANDATORY STEP] Dungeon {self.dungeon_name} has no steps for {keyToUse} \033[1;37;40m")
                    self.pause()

                # foreach all steps in dungeon
                for step in self.dungeon_images[self.dungeon_name][keyToUse]:
                    if self.paused is True:
                        break
                    # print(
                    #     f"\033[1;33;40m [CHECK DUNGEON MANDATORY STEP] \033[1;37;40m {step}")
                    path = step[0]['path']
                    file = step[0]['file']
                    feedback_image_coords = self.moveplayer.founfIconInScreen(
                        self.img_path + path, file, 0, False, self.captureWorker.screenshot, False)
                    # print in orange

                    # print(
                    #     f"\033[1;33;40m [CHECK DUNGEON MANDATORY STEP] \033[1;37;40m {file} -- {feedback_image_coords}")
                    # print(
                    #     f"\033[1;33;40m [CHECK DUNGEON MANDATORY STEP] \033[1;37;40m {self.RunDungeonOrchestration.actual_step} -- {step[0]['step_num']}")
                    # print(
                    #     f"\033[1;33;40m [CHECK DUNGEON MANDATORY STEP] \033[1;37;40m {self.step_part_order[self.RunDungeonOrchestration.actual_step_part]} -- {self.step_part_order[step[0]['step_part']]}")
                    # print(
                    #     f"\033[1;33;40m [CHECK DUNGEON MANDATORY STEP] \033[1;37;40m {self.feedback_order[self.RunDungeonOrchestration.actual_step_feedback]} -- {self.feedback_order[step[0]['feedback']]}")
                    if feedback_image_coords != (0, 0):
                        if (self.RunDungeonOrchestration.actual_step < step[0]['step_num']) or \
                            (self.RunDungeonOrchestration.actual_step == step[0]['step_num'] and
                             self.step_part_order[self.RunDungeonOrchestration.actual_step_part] <= self.step_part_order[step[0]['step_part']]) or \
                            (self.RunDungeonOrchestration.actual_step == step[0]['step_num'] and
                             self.RunDungeonOrchestration.actual_step_part == step[0]['step_part'] and
                             self.feedback_order[self.RunDungeonOrchestration.actual_step_feedback] < self.feedback_order[step[0]['feedback']]):
                            # Tu código si la condición se cumple

                            self.threads.pause_all_threads(
                                ['CheckIsDead', 'CaptureWorker'])
                            self.send_text_to_bot.send(
                                f"Found mandatory step {file} in {self.dungeon_name}", self.from_python, 'green')
                            self.send_text_to_bot.send(
                                f"Actual step: {self.RunDungeonOrchestration.actual_step}, going to step {step[0]['step_num']} {step[0]['step_part']} {step[0]['feedback']}", self.from_python, 'green')
                            while self.RunDungeonOrchestration.completely_stopped is False:
                                print(
                                    f"\033[1;33;40m [CHECK DUNGEON MANDATORY STEP] \033[1;37;40m Waiting for completely_stopped")
                                time.sleep(0.5)

                            # if self.feedback_order[step[0]['feedback']] == 1:
                            #     step_feedback = "after_feedback"
                            #     if self.step_part_order[step[0]['step_part']] == 1:
                            #         step_part = "after_end"
                            #         step_num = step[0]['step_num'] - 1
                            #     else:
                            #         if self.step_part_order[step[0]['step_part']] == 2:
                            #             step_part = "before_start"
                            #         if self.step_part_order[step[0]['step_part']] == 3:
                            #             step_part = "in_progress"
                            #         step_num = step[0]['step_num']
                            # else:
                            #     if self.feedback_order[step[0]['feedback']] == 2:
                            #         step_feedback = "before_feedback"
                            #     if self.feedback_order[step[0]['feedback']] == 3:
                            #         step_feedback = "in_progress"
                            #     step_part = step[0]['step_part']
                            #     step_num = step[0]['step_num']
                

                            # if step_num < 0:
                            #     step_num = 0
                            #     step_part == self.step_part_order[1]
                            #     step_feedback == self.feedback_order[1]

                            step_num = step[0]['step_num']
                            step_part = step[0]['step_part']
                            step_feedback = step[0]['feedback']

                            print(
                                f"\033[1;33;40m [CHECK DUNGEON MANDATORY STEP] \033[1;37;40m ------------------------------------")
                            print(
                                f"\033[1;33;40m [CHECK DUNGEON MANDATORY STEP] \033[1;37;40m step_num: {step_num}")
                            print(
                                f"\033[1;33;40m [CHECK DUNGEON MANDATORY STEP] \033[1;37;40m step_part: {step_part}")
                            print(
                                f"\033[1;33;40m [CHECK DUNGEON MANDATORY STEP] \033[1;37;40m step_feedback: {step_feedback}")

                            self.RunDungeonOrchestration.actual_step = step_num
                            self.RunDungeonOrchestration.force_step_part = step_part
                            self.RunDungeonOrchestration.force_step_feedback = step_feedback
                            self.threads.resume_all_threads()
                            # remove this step from list
                            # Convertir la tupla a lista, eliminar el primer elemento y volver a asignarla a la clave "kikuras"
                            self.dungeon_images[self.dungeon_name][keyToUse] = list(self.dungeon_images[self.dungeon_name][keyToUse])
                            self.dungeon_images[self.dungeon_name][keyToUse].pop(0)
                            self.dungeon_images[self.dungeon_name][keyToUse] = tuple(self.dungeon_images[self.dungeon_name][keyToUse])

                            break
                        self.pause()

                time.sleep(0.5)

            except Exception as e:
                 print(
                     "\033[1;31;40m [CHECK DUNGEON MANDATORY STEP] \033[1;37;40m")
                 print(e)
                 continue

            time.sleep(1)
