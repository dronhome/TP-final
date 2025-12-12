# -*- coding: utf-8 -*-
import time
import math
import random
import sys
import os

from robot_exercise_utils import RobotExerciseUtils
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import predpazenie_v_stoji

module_path = os.path.join(os.getcwd(), 'sadanie')
if module_path not in sys.path:
    sys.path.append(module_path)

import pripazenie_z_predpazenia
import sitting_position_for_extending_legs as sit_on_chair


class Predpazovanie(RobotExerciseUtils):
     
    
    def __init__(self, naoqi_instance):
        super(Predpazovanie, self).__init__(naoqi_instance)

        self.exercise_name = 'predpazovanie'
        self.starting_sentence = 'Začíname predpažovať. Buďeme cvičiť v stoji.'
    
    def run_exercise(self, score, message, pending_messages, phase, conn):
        if message == 'predpazovanie_start,':
            self.remove_items_by_value(pending_messages, score, -1, self.finished_phases, False)
            
            if self.naoqi.er:
                conn.send("getEmotion_start".encode())
            else:
                self.naoqi.speak_or_message(self.starting_sentence)
                conn.send("ExerciseContinue_tposeE".encode())

        if message == 'predpazovanie_en':
            
            # stand_up_from_chair_times = [[time / self.FAST_MODE_MULTIPLIER for time in times] for times in stand_up_from_chair.times] if self.FAST_MODE else sit_on_chair.times
            # naoqi.motionProxy.angleInterpolationBezier(stand_up_from_chair.names, stand_up_from_chair_times, stand_up_from_chair.keys)

            self.remove_items_by_value(pending_messages, score, -2, self.finished_phases, False)

            if self.naoqi.er:
                conn.send("getEmotion_end".encode())
            else:
                self.naoqi.speak_or_message("Koniec cvičenia, Pripravíme sa na ďalší cvik.")


        if message == 'predpazovanie':
            if phase == 0 and self.finished_phases["0"] == False:

                self.finished_phases["0"] = True
                self.remove_items_by_value(pending_messages, score, 0, self.finished_phases, False)
                self.naoqi.speak_or_message("Predpaž.")

                self.naoqi.motionProxy.angleInterpolationBezier(predpazenie_v_stoji.names, predpazenie_v_stoji.times, predpazenie_v_stoji.keys)

                conn.send("ExerciseContinue_predpazenie".encode())

            elif phase == 1 and self.finished_phases["1"] == False:

                self.finished_phases["1"] = True
                self.remove_items_by_value(pending_messages, score, 1, self.finished_phases)
                self.naoqi.speak_or_message("Pripaž.")
                self.naoqi.motionProxy.angleInterpolationBezier(pripazenie_z_predpazenia.names, pripazenie_z_predpazenia.times, pripazenie_z_predpazenia.keys)

                conn.send("ExerciseContinue_predpazenie".encode())


            elif phase == 2 and self.finished_phases["2"] == False and self.finished_phases["1"] == True:
                
                self.finished_phases["2"] = True
                self.remove_items_by_value(pending_messages, score, 2, self.finished_phases, False)

                self.say_score(score + 1, conn)

                self.finished_phases = {str(i): False for i in range(6)}
                
                conn.send("ExerciseContinue_predpazenie".encode())

    

    def warning_say(self, message):
        
         # - predpazenie
        if 'Base_pos_back' in message:
            self.naoqi.speak_or_message("Vráť ruky dole")
        
        elif 'Base_pos' in message:
            self.naoqi.speak_or_message("Prosím predpaž")
        

        elif "Predpazene_ruky_vysoko_a_odseba" in message:
            self.naoqi.speak_or_message('Posuň ruky nižšie na vodorvnu polohu a bližšie k sebe.')

        elif "Predpazene_ruky_vysoko_a_nespravne" in message:
            self.naoqi.speak_or_message('Daj ruky nižšie na vodorvnu úroveň a do správnej polohy.')

        elif "Predpazene_ruky_vysoko" in message:
            self.naoqi.speak_or_message('Skús ruky posunúť nižšie na vodorvnu polohu.')

        elif "Predpazene_ruky_nizko_a_odseba" in message:
            self.naoqi.speak_or_message('Skús ruky posunúť vyššie na vodorvnu polohu a priblížiť ich k sebe.')

        elif "Predpazene_ruky_nizko_a_nespravne" in message: 
            self.naoqi.speak_or_message('Daj ruky vyššie na vodorvnu úroveň a do správnej polohy.')
               
        elif "Predpazene_ruky_nizko" in message:
            self.naoqi.speak_or_message('Skús ruky posunúť vyššie na vodorvnu polohu.')
        
        elif "Predpazene_ruky_zle" in message:
           
            self.naoqi.speak_or_message('Predpaž ruky do správnej polohy.')
                
        elif "Predpazene_ruky_priliz_od_seba" in message:
           
            self.naoqi.speak_or_message('Priblíž ruky trochu bližšie k sebe.')
            
        # Hlášky pre pravú ruku - predpazenie

        elif "Prava_ruka_vysoko_a_od_tela" in message:
            self.naoqi.speak_or_message('Pravú ruku daj trošku nižšie a bližšie k ľavej ruke.')

        elif "Prava_ruka_vysoko" in message:
            self.naoqi.speak_or_message('Pravú ruku skús dať o trochu nižšie.')
               
        elif "Prava_ruka_nizko_a_od_tela" in message:
            self.naoqi.speak_or_message('Pravú ruku zdvihni trochu vyššie a bližšie k ľavej ruke.')

        elif "Prava_ruka_nizko" in message:
            self.naoqi.speak_or_message('Daj pravú ruku trošku vyššie.')

        elif "Prava_ruka_od_tela" in message:
            self.naoqi.speak_or_message('Pravú ruku priblíž viac k ľavej ruke.')

        # Hlášky pre ľavú ruku - predpazenie

        elif "Lava_ruka_vysoko_a_od_tela" in message:
            self.naoqi.speak_or_message('Ľavú ruku daj trošku nižšie a bližšie k pravej ruke.')

        elif "Lava_ruka_vysoko" in message:
            self.naoqi.speak_or_message('Ľavú ruku skús dať o trochu nižšie.')

        elif "Lava_ruka_nizko_a_od_tela" in message:
            self.naoqi.speak_or_message('Ľavú ruku zdvihni trochu vyššie a bližšie k pravej ruke.')

        elif "Lava_ruka_nizko" in message:
            self.naoqi.speak_or_message('Zdvihni ľavú ruku trošku vyššie.')

        elif "Lava_ruka_od_tela" in message:
            self.naoqi.speak_or_message('Ľavú ruku priblíž viac k pravej ruke.')

        elif "Chyba" in message:
            self.naoqi.speak_or_message('Skús lepšie predpažiť.')