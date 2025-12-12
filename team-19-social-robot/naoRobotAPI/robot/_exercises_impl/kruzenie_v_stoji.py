# -*- coding: utf-8 -*-

import time
import math
import random
import sys
import os

from robot_exercise_utils import RobotExerciseUtils
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

module_path = os.path.join(os.getcwd(), 'kruzenie')
if module_path not in sys.path:
    sys.path.append(module_path)

import ruky_v_stoji_dole

import ruky_v_stoji_hore


class KruzenieVStoji(RobotExerciseUtils):
    is_ending = False

      
    def __init__(self, naoqi_instance):
        super(KruzenieVStoji, self).__init__(naoqi_instance)

        self.exercise_name = 'arm_circling'
        self.starting_sentence = 'Začíname cvičiť krúženie rukami v stoji, opakuj po mňe'
    
    def run_exercise(self, score, message, conn):
        
        if message == 'arm_circling_start':
            
            self.naoqi.postureProxy.goToPosture(self.zakladna_pozicia_statia, 0.5)
            
            if self.naoqi.er:
                conn.send("getEmotion_start".encode())
            else:
                self.naoqi.speak_or_message(self.starting_sentence)
                conn.send("ExerciseContinue_kr".encode())

        elif message == 'arm_circling_end':
            self.is_ending = True

            self.naoqi.postureProxy.goToPosture(self.zakladna_pozicia_statia, 0.5)

            if self.naoqi.er:
                 conn.send("getEmotion_end".encode())
            else:
                self.naoqi.speak_or_message("Super. Zvládľi sme to na jednotku.")
        
        elif message == 'arm_circling_down':
            self.naoqi.speak_or_message("Otoč ruky dole")
            self.naoqi.motionProxy.angleInterpolationBezier(ruky_v_stoji_dole.names, ruky_v_stoji_dole.times, ruky_v_stoji_dole.keys)
            
            time.sleep(0.5)
            conn.send("ExerciseContinue_kr".encode())
        
        elif message == 'arm_circling_up' and self.is_ending is False:
           
            
            self.say_score(score, conn)

            self.naoqi.speak_or_message("Vzpaž ruky nad hlavu")

            self.naoqi.motionProxy.angleInterpolationBezier(ruky_v_stoji_hore.names, ruky_v_stoji_hore.times, ruky_v_stoji_hore.keys)

            conn.send("ExerciseContinue_kr".encode())
    
    def warning_say(self, message):
        if "ZLE_hore" in message :
            self.naoqi.speak_or_message('Nemáš vystrete ruky nad hlavu')
        
        elif "Base_hore" in message:
            self.naoqi.speak_or_message('Prosím vpaž ruky hore')
           
        
        elif "ZLE_dole" in message:
            self.naoqi.speak_or_message('Polož ruky dole')
          
