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
import daj_ruky_k_telu_zo_zakladneho_sedu as ruky_k_telu_zo_zakladneho_sedu

module_path = os.path.join(os.getcwd(), 'predpazovanie_nohy_ruky')
if module_path not in sys.path:
    sys.path.append(module_path)

# Predpazovanie prava noha
import daj_ruky_k_telu_z_predpazenia_a_zdvihnutej_p_nohy as ruky_k_telu_z_predpazenia_a_zdvihnutej_p_nohy
import predpazovanie_a_zdvihanie_pravej_nohy_sucasne2 as predpazovanie_a_zdvihanie_pravej_nohy_sucasne2

# Predpazovanie lava noha
import daj_ruky_k_telu_z_predpazenia_a_zdvihnutej_l_nohy as ruky_k_telu_z_predpazenia_a_zdvihnutej_l_nohy
import predpazovanie_a_zdvihanie_lavej_nohy_sucasne as predpazovanie_a_zdvihanie_lavej_nohy_sucasne


class ForefootingPredpazovanie(RobotExerciseUtils):

   
      
    def __init__(self, naoqi_instance):
       

        self.starting_sentence = 'Začíname zdvíhať nohy na stoličke s predpažovaňím. Sadňi si na stoličku.'
        self.exercise_name = 'ForefootingPredpazovanie'
        self.say_emotion_after_end = False
        self.is_sitting = True
        super(ForefootingPredpazovanie, self).__init__(naoqi_instance)
    
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
        if message == 'forefooting_predpazovanie_start,':
            
            if self.naoqi.er:
                conn.send("getEmotion_forefootingStart".encode())
            else:
                self.naoqi.speak_or_message(self.starting_sentence)
                self.start_forefooting()
                conn.send(("ExerciseContinue_" + self.exercise_name).encode())

            self.remove_items_by_value(pending_messages, score, -1, self.finished_phases)
           

        if message == 'forefooting_predpazovanie_en':

            if self.naoqi.er:
                conn.send("getEmotion_forefootingEnd".encode())
            else:
                self.naoqi.speak_or_message("Koniec cvičenia, Pripravíme sa na ďalší cvik.")
                self.end_forefooting()
                conn.send(("ExerciseContinue_" + self.exercise_name).encode())

            self.remove_items_by_value(pending_messages, score, -2, self.finished_phases, False)

        if message == 'forefooting_predpazovanie':
            if phase == 0 and self.finished_phases["0"] == False: # We put robot to sit first, so we do it in start
                
                self.finished_phases["0"] = True
                self.remove_items_by_value(pending_messages, score, 0, self.finished_phases)

                if self.MIRRORING is True:
                    self.naoqi.motionProxy.angleInterpolationBezier(predpazovanie_a_zdvihanie_lavej_nohy_sucasne.names, predpazovanie_a_zdvihanie_lavej_nohy_sucasne.times, predpazovanie_a_zdvihanie_lavej_nohy_sucasne.keys)
                else:
                    self.naoqi.motionProxy.angleInterpolationBezier(predpazovanie_a_zdvihanie_pravej_nohy_sucasne2.names, predpazovanie_a_zdvihanie_pravej_nohy_sucasne2.times, predpazovanie_a_zdvihanie_pravej_nohy_sucasne2.keys)
                
                conn.send(("ExerciseContinue_" + self.exercise_name + str(phase)).encode())

            elif phase == 1 and self.finished_phases["1"] == False and self.finished_phases["0"] == True:

                self.finished_phases["1"] = True
                self.remove_items_by_value(pending_messages, score, 1, self.finished_phases)

                if self.MIRRORING is True:
                    self.naoqi.motionProxy.angleInterpolationBezier(ruky_k_telu_z_predpazenia_a_zdvihnutej_l_nohy.names, ruky_k_telu_z_predpazenia_a_zdvihnutej_l_nohy.times, ruky_k_telu_z_predpazenia_a_zdvihnutej_l_nohy.keys)
                else:
                    self.naoqi.motionProxy.angleInterpolationBezier(ruky_k_telu_z_predpazenia_a_zdvihnutej_p_nohy.names, ruky_k_telu_z_predpazenia_a_zdvihnutej_p_nohy.times, ruky_k_telu_z_predpazenia_a_zdvihnutej_p_nohy.keys)

                conn.send(("ExerciseContinue_" + self.exercise_name + str(phase)).encode())

            elif phase == 2 and self.finished_phases["2"] == False and self.finished_phases["1"] == True:

                self.finished_phases["2"] = True
                self.remove_items_by_value(pending_messages, score, 2, self.finished_phases)

                if self.MIRRORING is True:
                    self.naoqi.motionProxy.angleInterpolationBezier(predpazovanie_a_zdvihanie_pravej_nohy_sucasne2.names, predpazovanie_a_zdvihanie_pravej_nohy_sucasne2.times, predpazovanie_a_zdvihanie_pravej_nohy_sucasne2.keys)
                else:
                    self.naoqi.motionProxy.angleInterpolationBezier(predpazovanie_a_zdvihanie_lavej_nohy_sucasne.names, predpazovanie_a_zdvihanie_lavej_nohy_sucasne.times, predpazovanie_a_zdvihanie_lavej_nohy_sucasne.keys)
                
                conn.send(("ExerciseContinue_" + self.exercise_name + str(phase)).encode())

            elif phase == 3 and self.finished_phases["3"] == False and self.finished_phases["2"] == True:
                
                self.finished_phases["3"] = True
                self.remove_items_by_value(pending_messages, score, 3, self.finished_phases)

                if self.MIRRORING is True:
                    self.naoqi.motionProxy.angleInterpolationBezier(ruky_k_telu_z_predpazenia_a_zdvihnutej_p_nohy.names, ruky_k_telu_z_predpazenia_a_zdvihnutej_p_nohy.times, ruky_k_telu_z_predpazenia_a_zdvihnutej_p_nohy.keys)
                    import time
                    time.sleep(0.5)
                else:
                    self.naoqi.motionProxy.angleInterpolationBezier(ruky_k_telu_z_predpazenia_a_zdvihnutej_l_nohy.names, ruky_k_telu_z_predpazenia_a_zdvihnutej_l_nohy.times, ruky_k_telu_z_predpazenia_a_zdvihnutej_l_nohy.keys)

                conn.send(("ExerciseContinue_" + self.exercise_name + str(phase)).encode())

            elif phase == 4 and self.finished_phases["4"] == False and self.finished_phases["3"] == True:

                self.finished_phases["4"] = True
                self.remove_items_by_value(pending_messages, score, 4, self.finished_phases, False)

                self.say_score(score + 1, conn)

                self.finished_phases = {str(i): False for i in range(6)}
                
                conn.send(("ExerciseContinue_" + self.exercise_name + str(phase)).encode())

    def warning_say(self, message):
        leg_wrong = False

        if "ForefootingPred_a_zdvihni_pravu_nohu" in message:
            self.naoqi.speak_or_message('Zdvihniťe pravu nohu.')
            leg_wrong = True
            
        if "ForefootingPred_a_zdvihni_lavu_nohu" in message:
            self.naoqi.speak_or_message('Zdvihniťe ľavu nohu.')
            leg_wrong = True

        if "In_Base_pos_left" in message:
            self.naoqi.speak_or_message('Predpažťe ruky a zdvihniťe ľavu nohu.')
            return
        
        elif "In_Base_pos_right" in message:
            self.naoqi.speak_or_message('Predpažťe ruky a zdvihniťe pravu nohu.')
            return

        # - predpazenie
        elif "Predpazene_ruky_vysoko_a_odseba" in message:
            if leg_wrong is True:
                time.sleep(0.2)
                self.naoqi.speak_or_message('Potom posuň ruky nižšie na vodorvnu polohu a bližšie k sebe.')
            else:
                self.naoqi.speak_or_message('Posuň ruky nižšie na vodorvnu polohu a bližšie k sebe.')

        elif "Predpazene_ruky_vysoko_a_nespravne" in message:
            if leg_wrong is True:
                time.sleep(0.2)
                self.naoqi.speak_or_message('Potom daj ruky nižšie na vodorvnu pozíciu a do správnej polohy.')
            else:
                self.naoqi.speak_or_message('Daj ruky nižšie na vodorvnu polohu a do správnej polohy.')

        elif "Predpazene_ruky_vysoko" in message:
            if leg_wrong is True:
                time.sleep(0.2)
                self.naoqi.speak_or_message('Zároveň skús ruky posuň nižšie na vodorvnu polohu.')
            else:
                self.naoqi.speak_or_message('Skús ruky posuň nižšie na vodorvnu polohu.')

        elif "Predpazene_ruky_nizko_a_odseba" in message:
            if leg_wrong is True:
                time.sleep(0.2)
                self.naoqi.speak_or_message('Zároveň skús ruky posuň vyššie na vodorvnu polohu a priblížiť ich bližšie k sebe.')
            else:
                self.naoqi.speak_or_message('Skús ruky posuň vyššie na vodorvnu polohu a priblížiť ich k sebe.')

        elif "Predpazene_ruky_nizko_a_nespravne" in message: 
            if leg_wrong is True:
                time.sleep(0.2)
                self.naoqi.speak_or_message('Tiež daj ruky vyššie na vodorvnu polohu a do správnej polohy.')
            else:
                self.naoqi.speak_or_message('Daj ruky vyššie na vodorvnu polohu a do správnej polohy.')
               
        elif "Predpazene_ruky_nizko" in message:
            if leg_wrong is True:
                time.sleep(0.2)
                self.naoqi.speak_or_message('Zároveň daj ruky vyššie na vodorvnu pozíciu a do správnej polohy.')
            else:
                self.naoqi.speak_or_message('Skúste ruky posuň vyššie na vodorvnu polohu.')

         # Iné       
        elif "Predpazene_ruky_priliz_od_seba" in message:
            if leg_wrong is True:
                time.sleep(0.2)
                self.naoqi.speak_or_message('Tiež priblíž ruky trochu bližšie k sebe.')
            else:
                self.naoqi.speak_or_message('Priblíž ruky trochu bližšie k sebe.')
        
        elif "Predpazene_ruky_zle" in message:
            if leg_wrong is True:
                time.sleep(0.2)
                self.naoqi.speak_or_message('Tiež predpaž ruky na vodorovnú polohu')
            else:
                self.naoqi.speak_or_message('Predpaž ruky na vodorovnú polohu.')
            
        # Hlášky pre pravú ruku - predpazenie
        elif "Prava_ruka_vysoko_a_od_tela" in message:
            if leg_wrong is True:
                time.sleep(0.2)
                self.naoqi.speak_or_message('Potom pravú ruku daj o trošku nižšie a bližšie k ľavej ruke.')
            else:
                self.naoqi.speak_or_message('Pravú ruku daj trošku nižšie a bližšie k ľavej ruke.')

        elif "Prava_ruka_vysoko" in message:
            if leg_wrong is True:
                time.sleep(0.2)
                self.naoqi.speak_or_message('Potom pravú ruku skúste dať o trochu nižšie.')
            else:
                self.naoqi.speak_or_message('Pravú ruku skúste dať o trochu nižšie.')
               
        elif "Prava_ruka_nizko_a_od_tela" in message:
            if leg_wrong is True:
                time.sleep(0.2)
                self.naoqi.speak_or_message('Potom pravú ruku zdvihňi trochu vyššie a bližšie k ľavej ruke.')
            else:
                self.naoqi.speak_or_message('Pravú ruku zdvihňi trochu vyššie a bližšie k ľavej ruke.')

        elif "Prava_ruka_nizko" in message:
            if leg_wrong is True:
                time.sleep(0.2)
                self.naoqi.speak_or_message('Zároveň daj pravú ruku trošku vyššie.')
            else:
                self.naoqi.speak_or_message('Dajťe pravú ruku trošku vyššie.')

        elif "Prava_ruka_od_tela" in message:
            if leg_wrong is True:
                time.sleep(0.2)
                self.naoqi.speak_or_message('Zároveň pravú ruku priblíž viac k ľavej ruke.')
            else:
                self.naoqi.speak_or_message('Pravú ruku priblíž viac k ľavej ruke.')

        # Hlášky pre ľavú ruku - predpazenie
        elif "Lava_ruka_vysoko_a_od_tela" in message:
            if leg_wrong is True:
                time.sleep(0.2)
                self.naoqi.speak_or_message('Potom ľavú ruku daj o trošku nižšie a bližšie k pravej ruke.')
            else:
                self.naoqi.speak_or_message('Ľavú ruku daj trošku nižšie a bližšie k pravej ruke.')

        elif "Lava_ruka_vysoko" in message:
            if leg_wrong is True:
                time.sleep(0.2)
                self.naoqi.speak_or_message('Potom ľavú ruku skús dať o trochu nižšie.')
            else:
                self.naoqi.speak_or_message('Ľavú ruku skús dať o trochu nižšie.')

        elif "Lava_ruka_nizko_a_od_tela" in message:
            if leg_wrong is True:
                time.sleep(0.2)
                self.naoqi.speak_or_message('Potom ľavú ruku zdvihňi o trochu vyššie a bližšie k pravej ruke.')
            else:
                self.naoqi.speak_or_message('Ľavú ruku zdvihňi trochu vyššie a bližšie k pravej ruke.')

        elif "Lava_ruka_nizko" in message:
            if leg_wrong is True:
                time.sleep(0.2)
                self.naoqi.speak_or_message('Zároveň zdvihňi ľavú ruku trošku vyššie.')
            else:
                self.naoqi.speak_or_message('Zdvihnite ľavú ruku trošku vyššie.')

        elif "Lava_ruka_od_tela" in message:
            if leg_wrong is True:
                time.sleep(0.2)
                self.naoqi.speak_or_message('Zároveň ľavú ruku priblíž viac k pravej ruke.')
            else:
                self.naoqi.speak_or_message('Ľavú ruku priblíž viac k pravej ruke.')

        elif "Chyba" in message:
            if leg_wrong is True:
                time.sleep(0.2)
                self.naoqi.speak_or_message('Skús tiež lepšie predpažiť. Dbaj na to aby ruky boli vodorovné s tvojími ramenamy')
            else:
                self.naoqi.speak_or_message('Skús lepšie predpažiť. Dbaj na to aby ruky boli vodorovné s tvojími ramenamy')