# -*- coding: utf-8 -*-

import time
import math
import random
import sys
import os

from robot_exercise_utils import RobotExerciseUtils
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import sit_exercise

module_path = os.path.join(os.getcwd(), 'sadanie')
if module_path not in sys.path:
    sys.path.append(module_path)


class Upazovanie(RobotExerciseUtils):
    
      
    def __init__(self, naoqi_instance):
        super(Upazovanie, self).__init__(naoqi_instance)
        self.exercise_name = 'tpose'
        self.starting_sentence = "Začiatok cviku, upažovanie"

    def warning_say(self, message):

        if 'Base_pos_back' in message:
            self.naoqi.speak_or_message("Prosím pripaž ruky")
            
        elif 'Base_pos' in message:
            self.naoqi.speak_or_message("Prosím upaž ruky")

        elif "tpose_arms_above" in message:
            self.naoqi.speak_or_message('Posuň upažené ruky nižšie na vodorovnu polohu.')
               
        elif "tpose_arms_below" in message:
            self.naoqi.speak_or_message('Posuň upažené ruky vyššie na vodorovnu polohu.')

        elif "tpose_arms_wrong" in message:
            self.naoqi.speak_or_message('Skús upažiť ruky vodorovne.')
               
    
    def run_exercise(self, score, message, conn):

        if message == 'tpose_down':

            # if uz_zdvihol_hlavu is False:
            #     # zdvihni_hlavu()
            #     uz_zdvihol_hlavu = True
                
            self.say_score(score, conn)
           
            if self.naoqi.is_physical is True:
                time.sleep(0.5)
            else:
                time.sleep(1)

            random.randint(0, 10)
            if score == 9:
                self.naoqi.speak_or_message("Posledný krát")
            else:
                self.naoqi.speak_or_message("Upaž ruky")
            
            time.sleep(0.5)
           

            # Adjustment of arms position (Up)
            self.naoqi.motionProxy.setAngles(["LShoulderRoll"], 1.3264502315, 0.3)
            self.naoqi.motionProxy.setAngles(["LElbowRoll"], 1.3264502315, 0.3)

            self.naoqi.motionProxy.setAngles(["RShoulderRoll"], -1.3264502315, 0.3)
            self.naoqi.motionProxy.setAngles(["RElbowRoll"], -1.3264502315, 0.3)

            if self.naoqi.is_physical is True:
                time.sleep(1)
            else:
                time.sleep(0.5)
            
            conn.send("ExerciseContinue_tposeE".encode())  
            
            print(score)

        elif message == 'tpose_up':

            if self.naoqi.is_physical is True:
                time.sleep(0.75)
            else:
                time.sleep(0.5)
            
            if score < 3:
                self.naoqi.speak_or_message("Pripaž ruky")
                # speechProxy.post.say(str("Pripažťe"))
            else:
                self.naoqi.speak_or_message("Pripaž ruky")
                # speechProxy.post.say(str("Pripažťe"))

            time.sleep(0.5)
            # Adjustment of arms position (Down)
            self.naoqi.motionProxy.setAngles(["LShoulderRoll"], 0.0, 0.3)
            self.naoqi.motionProxy.setAngles(["LElbowRoll"], 0.0, 0.3)

            self.naoqi.motionProxy.setAngles(["RShoulderRoll"], 0.0, 0.3)
            self.naoqi.motionProxy.setAngles(["RElbowRoll"], 0.0, 0.3)

            if self.naoqi.is_physical is True:
                time.sleep(0.75)
            else:
                time.sleep(0.25)

            conn.send("ExerciseContinue_tposeE".encode())
        
        elif message == 'tpose_start':
            
            self.naoqi.postureProxy.goToPosture(self.zakladna_pozicia_statia, 0.5)
            
            if self.naoqi.er:
                conn.send("getEmotion_start".encode())
            else:
                self.naoqi.speak_or_message(self.starting_sentence)
                conn.send("ExerciseContinue_tposeE".encode())

        elif message == 'tpose_end':
            self.naoqi.postureProxy.goToPosture(self.zakladna_pozicia_statia, 0.5)

            if self.naoqi.er:
                 conn.send("getEmotion_end".encode())
            else:
                self.naoqi.speak_or_message("Super. Zvládľi sme to na jednotku.")