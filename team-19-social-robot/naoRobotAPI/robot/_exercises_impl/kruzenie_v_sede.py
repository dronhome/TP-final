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

import ruky_v_sede_dole
import ruky_v_sede_hore

from robot_exercise_utils import RobotExerciseUtils
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))


module_path = os.path.join(os.getcwd(), 'sadanie')
if module_path not in sys.path:
    sys.path.append(module_path)

import stand_up_from_chair
import sitting_position_for_extending_legs as sit_on_chair

module_path = os.path.join(os.getcwd(), 'rozpazovanie_nohy_ruky')
if module_path not in sys.path:
    sys.path.append(module_path)

import daj_ruky_k_telu_zo_zakladneho_sedu as ruky_k_telu_zo_zakladneho_sedu


class KruzenieVSede(RobotExerciseUtils):
    is_ending = False

      
    def __init__(self, naoqi_instance):
        super(KruzenieVSede, self).__init__(naoqi_instance)

        self.exercise_name = 'arm_sit_circling'
        self.starting_sentence = 'Začíname cvičiť krúženie rukami v sede, opakujťe po mňe'
        self.is_sitting = True
    
    def start_forefooting(self):
        sit_on_chair_times = [[time / self.FAST_MODE_MULTIPLIER for time in times] for times in sit_on_chair.times] if self.FAST_MODE else sit_on_chair.times
        self.naoqi.motionProxy.angleInterpolationBezier(sit_on_chair.names, sit_on_chair_times, sit_on_chair.keys)
        self.naoqi.motionProxy.angleInterpolationBezier(ruky_k_telu_zo_zakladneho_sedu.names, ruky_k_telu_zo_zakladneho_sedu.times, ruky_k_telu_zo_zakladneho_sedu.keys)
    
    def end_forefooting(self):
        stand_up_from_chair_times = [[time / self.FAST_MODE_MULTIPLIER for time in times] for times in stand_up_from_chair.times] if self.FAST_MODE else sit_on_chair.times
        self.naoqi.motionProxy.angleInterpolationBezier(stand_up_from_chair.names, stand_up_from_chair_times, stand_up_from_chair.keys)


    def run_exercise(self, score, message, conn):
        
        if message == 'arm_sit_circling_start':
            
            self.naoqi.postureProxy.goToPosture(self.zakladna_pozicia_statia, 0.5)
            
            if self.naoqi.er:
                conn.send("getEmotion_start".encode())
                message = conn.recv(1024)
                self.say_emotion_start(message, '')
            
            self.naoqi.speak_or_message(self.starting_sentence)
            self.start_forefooting()
            conn.send("ExerciseContinue_ksr".encode())

        elif message == 'arm_sit_circling_end':
            self.is_ending = True

            if self.naoqi.er:
                conn.send("getEmotion_End".encode())
                message = conn.recv(1024)
                self.say_emotion_end(message)

         
            self.naoqi.speak_or_message("Koniec cvičenia, Pripravíme sa na ďalší cvik.")
            self.end_forefooting()
            conn.send("ExerciseContinue_ksr".encode())
        
        elif message == 'arm_sit_circling_down':
            self.naoqi.speak_or_message("Otoč ruky dole")
            self.naoqi.motionProxy.angleInterpolationBezier(ruky_v_sede_dole.names, ruky_v_sede_dole.times, ruky_v_sede_dole.keys)
            conn.send("ExerciseContinue_ksr".encode())
        
        elif message == 'arm_sit_circling_up' and self.is_ending is False:
            
            self.say_score(score + 1, conn)
            self.naoqi.speak_or_message("Vzpaž ruky nad hlavu")

            self.naoqi.motionProxy.angleInterpolationBezier(ruky_v_sede_hore.names, ruky_v_sede_hore.times, ruky_v_sede_hore.keys)

            conn.send("ExerciseContinue_ksr".encode())
    
    def warning_say(self, message):
        if "ZLE_hore" in message :
            self.naoqi.speak_or_message('Nemáš vystrete ruky nad hlavu')
        
        elif "Base_hore" in message:
            self.naoqi.speak_or_message('Prosím vpaž ruky hore')
           
        
        elif "ZLE_dole" in message:
            self.naoqi.speak_or_message('Polož ruky dole')
