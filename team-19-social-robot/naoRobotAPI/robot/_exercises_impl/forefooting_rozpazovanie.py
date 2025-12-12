# -*- coding: utf-8 -*-
import time
import math
import random
import sys
import os

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


# Rozpazovanie lava noha
import daj_ruky_k_telu_z_rozpazenia_a_zdvihnutej_l_nohy as ruky_k_telu_z_rozpazenia_a_zdvihnutej_l_nohy
import rozpazovanie_a_zdvihanie_lavej_nohy_sucasne as rozpazovanie_a_zdvihanie_lavej_nohy_sucasne_l_nohy

# Rozpazovanie prava noha
import rozpazovanie_a_zdvihanie_pravej_nohy_sucasne as rozpazovanie_zdvihanie_pravej_nohy_sucasne
import daj_ruky_k_telu_z_rozpazenia as ruky_k_telu_z_rozpazenia



class ForefootingRozpazovanie(RobotExerciseUtils):
   
      
    def __init__(self, naoqi_instance):
        
        self.exercise_name = 'ForefootingRozpazovanie'
        
        self.starting_sentence = "Začíname zdvíhať nohy na stoličke s upažovaňím. Sadňi si na stoličku."
        self.say_emotion_after_end = False
        self.is_sitting = True
        super(ForefootingRozpazovanie, self).__init__(naoqi_instance)
    
    def start_forefooting(self):
        sit_on_chair_times = [[time / self.FAST_MODE_MULTIPLIER for time in times] for times in sit_on_chair.times] if self.FAST_MODE else sit_on_chair.times
        self.naoqi.motionProxy.angleInterpolationBezier(sit_on_chair.names, sit_on_chair_times, sit_on_chair.keys)
        self.naoqi.motionProxy.angleInterpolationBezier(ruky_k_telu_zo_zakladneho_sedu.names, ruky_k_telu_zo_zakladneho_sedu.times, ruky_k_telu_zo_zakladneho_sedu.keys)
    
    def end_forefooting(self):
        stand_up_from_chair_times = [[time / self.FAST_MODE_MULTIPLIER for time in times] for times in stand_up_from_chair.times] if self.FAST_MODE else sit_on_chair.times
        self.naoqi.motionProxy.angleInterpolationBezier(stand_up_from_chair.names, stand_up_from_chair_times, stand_up_from_chair.keys)

    def say_forefooting_emotion(self, message):
        if "start" in message:
            self.say_emotion_start(message, self.starting_sentence)
            self.start_forefooting()
        elif "end" in message:
            self.say_emotion_end(message)
            self.end_forefooting()

    def run_exercise(self, score, message, pending_messages, phase, conn):
        if message == 'forefooting_rozpazovanie_start,':

            self.remove_items_by_value(pending_messages, score, -1, self.finished_phases)

            if self.naoqi.er:
                conn.send("getEmotion_forefootingStart".encode())
            else:
                self.naoqi.speak_or_message(self.starting_sentence)
                self.start_forefooting()
                conn.send("ExerciseContinue_forefootingRoz".encode())

        if message == 'forefooting_rozpazovanie_en':
            if self.naoqi.er:
                conn.send("getEmotion_forefootingEnd".encode())
            else:
                self.naoqi.speak_or_message("Koniec cvičenia, Pripravíme sa na ďalší cvik.")
                self.end_forefooting()
                conn.send("ExerciseContinue_forefootingRoz".encode())

            self.remove_items_by_value(pending_messages, score, -2, self.finished_phases, False)

        if message == 'forefooting_rozpazovanie':
            if phase == 0 and self.finished_phases["0"] == False: # We put robot to sit first, so we do it in start
                
                self.finished_phases["0"] = True
                self.remove_items_by_value(pending_messages, score, 0, self.finished_phases)

                if self.MIRRORING is True:
                    self.naoqi.motionProxy.angleInterpolationBezier(rozpazovanie_a_zdvihanie_lavej_nohy_sucasne_l_nohy.names, rozpazovanie_a_zdvihanie_lavej_nohy_sucasne_l_nohy.times, rozpazovanie_a_zdvihanie_lavej_nohy_sucasne_l_nohy.keys)
                else:
                    self.naoqi.motionProxy.angleInterpolationBezier(rozpazovanie_zdvihanie_pravej_nohy_sucasne.names, rozpazovanie_zdvihanie_pravej_nohy_sucasne.times, rozpazovanie_zdvihanie_pravej_nohy_sucasne.keys)

                conn.send(("ExerciseContinue_forefootingRoz" + str(phase)).encode())
                
            elif phase == 1 and self.finished_phases["1"] == False and self.finished_phases["0"] == True:

                self.finished_phases["1"] = True
                self.remove_items_by_value(pending_messages, score, 1, self.finished_phases)

                if self.MIRRORING is True:
                    self.naoqi.motionProxy.angleInterpolationBezier(ruky_k_telu_z_rozpazenia_a_zdvihnutej_l_nohy.names, ruky_k_telu_z_rozpazenia_a_zdvihnutej_l_nohy.times, ruky_k_telu_z_rozpazenia_a_zdvihnutej_l_nohy.keys)
                else:
                    self.naoqi.motionProxy.angleInterpolationBezier(ruky_k_telu_z_rozpazenia.names, ruky_k_telu_z_rozpazenia.times, ruky_k_telu_z_rozpazenia.keys)
                
                conn.send(("ExerciseContinue_forefootingRoz" + str(phase)).encode())
            
            elif phase == 2 and self.finished_phases["2"] == False and self.finished_phases["1"] == True:

                self.finished_phases["2"] = True
                self.remove_items_by_value(pending_messages, score, 2, self.finished_phases)

                if self.MIRRORING is True:
                    self.naoqi.motionProxy.angleInterpolationBezier(rozpazovanie_zdvihanie_pravej_nohy_sucasne.names, rozpazovanie_zdvihanie_pravej_nohy_sucasne.times, rozpazovanie_zdvihanie_pravej_nohy_sucasne.keys)
                else:
                    self.naoqi.motionProxy.angleInterpolationBezier(rozpazovanie_a_zdvihanie_lavej_nohy_sucasne_l_nohy.names, rozpazovanie_a_zdvihanie_lavej_nohy_sucasne_l_nohy.times, rozpazovanie_a_zdvihanie_lavej_nohy_sucasne_l_nohy.keys)

                conn.send(("ExerciseContinue_forefootingRoz" + str(phase)).encode())

            elif phase == 3 and self.finished_phases["3"] == False and self.finished_phases["2"] == True:

                self.finished_phases["3"] = True
                self.remove_items_by_value(pending_messages, score, 3, self.finished_phases)

                if self.MIRRORING is True:
                    self.naoqi.motionProxy.angleInterpolationBezier(ruky_k_telu_z_rozpazenia.names, ruky_k_telu_z_rozpazenia.times, ruky_k_telu_z_rozpazenia.keys)
                else:
                    self.naoqi.motionProxy.angleInterpolationBezier(ruky_k_telu_z_rozpazenia_a_zdvihnutej_l_nohy.names, ruky_k_telu_z_rozpazenia_a_zdvihnutej_l_nohy.times, ruky_k_telu_z_rozpazenia_a_zdvihnutej_l_nohy.keys)

                conn.send(("ExerciseContinue_forefootingRoz" + str(phase)).encode())

            elif phase == 4 and self.finished_phases["4"] == False and self.finished_phases["3"] == True:

                self.finished_phases["4"] = True
                self.remove_items_by_value(pending_messages, score, 4, self.finished_phases, False)
                self.say_score(score + 1, conn)

                self.finished_phases = {str(i): False for i in range(6)}

                conn.send(("ExerciseContinue_forefootingRoz" + str(phase)).encode())
    
    def warning_say(self, message):
        if "In_Base_pos_left" in message:
            self.naoqi.speak_or_message('Rozpaž ruky a zdvihňi ľavu nohu.')
            return
        
        elif "In_Base_pos_right" in message:
            self.naoqi.speak_or_message('Rozpaž ruky a zdvihňi pravu nohu.')
            return
        
        elif "tpose_arms_above" in message:
            
            if "ForefootingRoz_a_zdvihni_pravu_nohu" in message:
                self.naoqi.speak_or_message('Posuň upažené ruky nižšie na vodorovnu polohu a zdvihňi pravu nohu.')
                
            elif "ForefootingRoz_a_zdvihni_lavu_nohu" in message:
                self.naoqi.speak_or_message('Posuň upažené ruky nižšie na vodorovnu polohu a zdvihňi ľavu nohu.')
                
            else:
                self.naoqi.speak_or_message('Posuň upažené ruky nižšie na vodorovnu polohu.')

        elif "tpose_arms_below" in message:
            if "ForefootingRoz_a_zdvihni_pravu_nohu" in message:
                self.naoqi.speak_or_message('Posuň upažené ruky vyššie na vodorovnu polohu a zdvihňi pravu nohu.')
                
            elif "ForefootingRoz_a_zdvihni_lavu_nohu" in message:
                self.naoqi.speak_or_message('Posuň upažené ruky vyššie na vodorovnu polohu a zdvihňi ľavú nohu.')
            else:
                self.naoqi.speak_or_message('Posuň upažené ruky vyššie na vodorovnu polohu.')

        elif "tpose_arms_wrong" in message:
            if "ForefootingRoz_a_zdvihni_pravu_nohu" in message:
                self.naoqi.speak_or_message('Skús rozpažiť vodorovne a zdvihňi pravú nohu.')
                
            elif "ForefootingRoz_a_zdvihni_lavu_nohu" in message:
                self.naoqi.speak_or_message('Skús rozpažiť vodorovne a zdvihňi ľavú nohu.')
            else:
                self.naoqi.speak_or_message('Skús rozpažiť vodorovne.')
        
        elif "ForefootingRoz_a_zdvihni_pravu_nohu" in message:
            self.naoqi.speak_or_message('zdvihňi pravu nohu.')
            
        elif "ForefootingRoz_a_zdvihni_lavu_nohu" in message:
            self.naoqi.speak_or_message('zdvihňi ľavu nohu.')
           
