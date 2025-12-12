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

import sitting_position_for_extending_legs as sit_on_chair
import daj_ruky_k_telu_zo_zakladneho_sedu as ruky_k_telu_zo_zakladneho_sedu

class Drepy(RobotExerciseUtils):
    is_ending = False
      
    def __init__(self, naoqi_instance):
        super(Drepy, self).__init__(naoqi_instance)

        self.exercise_name = 'SquatExercise'
        self.starting_sentence = 'Začíname cvičiť, drepy. Cvičiť začíname v stoji.'
    
    def run_exercise(self, score, message, conn):

        if message == 'squat_start':
            self.naoqi.postureProxy.goToPosture(self.zakladna_pozicia_statia, 0.5)
            if self.naoqi.er:
                conn.send("getEmotion_start".encode())
            else:
                self.naoqi.speak_or_message(self.starting_sentence)
                conn.send("ExerciseContinue_tposeE".encode())
          
        elif message == 'squat_end':
            self.is_ending = True
            if not self.naoqi.is_physical:
                end_msg1 = 'Ďakujeme za spoluprácu,'
                end_msg2 = 'budeme sa ťešiť aj na budúce.'
            else:  
                end_msg1 = 'Ďakujem, že sme spolu cvičili,'
                end_msg2 = 'Ňech ťi to vydrží.'
         
            if self.naoqi.er:
                 conn.send("getEmotion_end".encode())
            else:
                self.naoqi.speak_or_message("Výborňe, drepy máme za sebou")
                time.sleep(0.4)
                
                self.naoqi.speak_or_message(end_msg1)
                self.naoqi.speak_or_message(end_msg2)

        elif message == 'squat_up'  and self.is_ending is False:

            # self.naoqi.postureProxy.goToPosture(self.zakladna_pozicia_statia, 0.2)

            self.say_score(score, conn)

            self.naoqi.motionProxy.angleInterpolation(sit_exercise.names, sit_exercise.keys, sit_exercise.times, True)

            if score < 6:
                self.naoqi.speak_or_message("Urob podrep a predpaž")
            else:
                self.naoqi.speak_or_message("Podrep s nádychom")

            conn.send("ExerciseContinue_squatE".encode())

        elif message == 'squat_down':
            
            self.naoqi.postureProxy.goToPosture(self.zakladna_pozicia_statia, 0.5)

            if (score < 4 and score != 0) or (score == 7):
                self.naoqi.speak_or_message("Postav sa s výdychom")
            else:
                self.naoqi.speak_or_message("Postav sa")

            conn.send("ExerciseContinue_squatE".encode())
    
    def warning_say(self, message):

        if "squat_rozpaz" in message and self.warning_said:
            self.naoqi.speak_or_message('Prosím, o trošku posuň choďidla od seba')
            self.warning_said = False
        
        elif "squat_rozpaz_oprava" in message:
            self.naoqi.speak_or_message('Výborne, teraz po mňe opakuj.')
            self.warning_said = True
        
        elif "squat_zly_drep" in message:
            self.naoqi.speak_or_message('Ešťe ňižšie.')
            self.warning_said = True
        
        # Zaklad
        elif 'Base_pos_back' in message:
            self.naoqi.speak_or_message("Uz sa postav")

        elif 'Base_pos' in message:
            self.naoqi.speak_or_message("Prosím, spravťe drep")
        
        elif "V_drepe_predpazene_ruky_vysoko_a_odseba" in message:
            self.naoqi.speak_or_message('Predpaž ruky viacej k sebe a do nižšej polohy.')

        elif "V_drepe_predpazene_ruky_vysoko" in message:
            self.naoqi.speak_or_message('Predpaž ruky do nižšej polohy.')
        
        elif "V_drepe_predpazene_ruky_nizko_a_odseba" in message:
            self.naoqi.speak_or_message('Predpaž ruky viacej k sebe a do vyššiej polohy.')
        
        elif "V_drepe_predpazene_ruky_nizko" in message:
            self.naoqi.speak_or_message('Predpaž ruky do vyššiej polohy.')
        
        # Ine

        elif "V_drepe_predpazene_ruky_zle" in message:
            self.naoqi.speak_or_message('Predpažené ruky predpaž na vodorovnú polohu na úroveň tvojích ramien.')
        
        elif "V_drepe_predpazene_ruky_priliz_od_seba" in message:
            self.naoqi.speak_or_message('Predpažené ruky priblíž viacej k sebe.')
        
        # Prava ruka
        
        elif "V_drepe_prava_ruka_vysoko" in message:
            self.naoqi.speak_or_message('Daj pravú ruku nižšie.')
        
        elif "V_drepe_prava_ruka_nizko" in message:
            self.naoqi.speak_or_message('Daj pravú ruku vyššie.')
        
        elif "V_drepe_prava_ruka_nespravne" in message:
            self.naoqi.speak_or_message('Daj pravú ruku bližšie k lavej.')
            
        
        # lava ruka
        
        elif "V_drepe_lava_ruka_vysoko" in message:           
            self.naoqi.speak_or_message('Daj ľavú ruku nižšie.')
        
        elif "V_drepe_lava_ruka_nizko" in message:           
            self.naoqi.speak_or_message('Daj ľavú ruku vyššie.')
        
        elif "V_drepe_lava_ruka_nespravne" in message:           
            self.naoqi.speak_or_message('Daj ľavú ruku bližšie k pravej.')

        else:
             self.naoqi.speak_or_message('Niečo robíž zle.')
               