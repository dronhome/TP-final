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

module_path = os.path.join(os.getcwd(), 'zdvihanie_na_stolicke')
if module_path not in sys.path:
    sys.path.append(module_path)

import lift_right_leg_on_chair1
import lift_right_leg_on_chair2
import lift_right_leg_on_chair3
import lift_left_leg_on_chair1

import vratenie_zdvihnutych_noh_v_sede

class forefootingOnChair(RobotExerciseUtils):
      
    def __init__(self, naoqi_instance):
        super(forefootingOnChair, self).__init__(naoqi_instance)

        self.exercise_name = ''

    def warning_say(self):
        pass
    
    def run_exercise(self, score, message, pending_messages, phase, conn):
        if message == 'forefooting_on_chair_start,':
            self.naoqi.speak_or_message("Začíname cvičiť prednožovaňie na stoličke.")

            sit_on_chair_times = [[time / self.FAST_MODE_MULTIPLIER for time in times] for times in sit_on_chair.times] if self.FAST_MODE else sit_on_chair.times
            self.naoqi.motionProxy.angleInterpolationBezier(sit_on_chair.names, sit_on_chair_times, sit_on_chair.keys)
            
            self.remove_items_by_value(pending_messages, score, -1, finished_phases)


        if message == 'forefooting_on_chair_en':

            self.naoqi.speak_or_message("Koniec cviku prednožovaňia na stoličke. Pripravíme sa na ďalší cvik.")

            stand_up_from_chair_times = [[time / self.FAST_MODE_MULTIPLIER for time in times] for times in stand_up_from_chair.times] if self.FAST_MODE else sit_on_chair.times
            self.naoqi.motionProxy.angleInterpolationBezier(stand_up_from_chair.names, stand_up_from_chair_times, stand_up_from_chair.keys)

            self.remove_items_by_value(pending_messages, score, -2, finished_phases, False)

        if message == 'forefooting_on_chair':
            if phase == 0 and finished_phases["0"] == False: # We put robot to sit first, so we do it in start
                finished_phases["0"] = True
                self.remove_items_by_value(pending_messages, score, 0, finished_phases)
                pozdvihnutie_lavej_nohy1_times = [[time / self.FAST_MODE_MULTIPLIER for time in times] for times in lift_left_leg_on_chair1.times] if self.FAST_MODE else lift_left_leg_on_chair1.times

                if self.MIRRORING is True:
                    self.naoqi.motionProxy.angleInterpolationBezier(lift_left_leg_on_chair1.names, pozdvihnutie_lavej_nohy1_times, lift_left_leg_on_chair1.keys)
                else:
                    lift_right_leg_on_chair_times1 = [[time / self.FAST_MODE_MULTIPLIER for time in times] for times in lift_right_leg_on_chair1.times] if self.FAST_MODE else lift_right_leg_on_chair1.times
                    lift_right_leg_on_chair_times2 = [[time / self.FAST_MODE_MULTIPLIER for time in times] for times in lift_right_leg_on_chair2.times] if self.FAST_MODE else lift_right_leg_on_chair2.times
                    lift_right_leg_on_chair_times3 = [[time / self.FAST_MODE_MULTIPLIER for time in times] for times in lift_right_leg_on_chair3.times] if self.FAST_MODE else lift_right_leg_on_chair3.times

                    self.naoqi.motionProxy.angleInterpolationBezier(lift_right_leg_on_chair1.names, lift_right_leg_on_chair_times1, lift_right_leg_on_chair1.keys)
                    self.naoqi.motionProxy.angleInterpolationBezier(lift_right_leg_on_chair2.names, lift_right_leg_on_chair_times2, lift_right_leg_on_chair2.keys)

                
            elif phase == 1 and finished_phases["1"] == False and finished_phases["0"] == True:
                finished_phases["1"] = True
                self.remove_items_by_value(pending_messages, score, 1, finished_phases)

                self.naoqi.motionProxy.angleInterpolationBezier(vratenie_zdvihnutych_noh_v_sede.names, vratenie_zdvihnutych_noh_v_sede.times, vratenie_zdvihnutych_noh_v_sede.keys)

            
            elif phase == 2 and finished_phases["2"] == False and finished_phases["1"] == True:
                finished_phases["2"] = True
                self.remove_items_by_value(pending_messages, score, 2, finished_phases)

                if self.MIRRORING is True:
                    lift_right_leg_on_chair_times1 = [[time / self.FAST_MODE_MULTIPLIER for time in times] for times in lift_right_leg_on_chair1.times] if self.FAST_MODE else lift_right_leg_on_chair1.times
                    lift_right_leg_on_chair_times2 = [[time / self.FAST_MODE_MULTIPLIER for time in times] for times in lift_right_leg_on_chair2.times] if self.FAST_MODE else lift_right_leg_on_chair2.times
                    lift_right_leg_on_chair_times3 = [[time / self.FAST_MODE_MULTIPLIER for time in times] for times in lift_right_leg_on_chair3.times] if self.FAST_MODE else lift_right_leg_on_chair3.times

                    self.naoqi.motionProxy.angleInterpolationBezier(lift_right_leg_on_chair1.names, lift_right_leg_on_chair_times1, lift_right_leg_on_chair1.keys)
                    self.naoqi.motionProxy.angleInterpolationBezier(lift_right_leg_on_chair2.names, lift_right_leg_on_chair_times2, lift_right_leg_on_chair2.keys)
                else:
                    pozdvihnutie_lavej_nohy1_times = [[time / self.FAST_MODE_MULTIPLIER for time in times] for times in lift_left_leg_on_chair1.times] if self.FAST_MODE else lift_left_leg_on_chair1.times
                    self.naoqi.motionProxy.angleInterpolationBezier(lift_left_leg_on_chair1.names, pozdvihnutie_lavej_nohy1_times, lift_left_leg_on_chair1.keys)



            elif phase == 3 and finished_phases["3"] == False and finished_phases["2"] == True:
                finished_phases["3"] = True
                self.remove_items_by_value(pending_messages, score, 3, finished_phases)

                self.naoqi.motionProxy.angleInterpolationBezier(vratenie_zdvihnutych_noh_v_sede.names, vratenie_zdvihnutych_noh_v_sede.times, vratenie_zdvihnutych_noh_v_sede.keys)


            elif phase == 4 and finished_phases["4"] == False and finished_phases["3"] == True:
                finished_phases["4"] = True
                self.remove_items_by_value(pending_messages, score, 4, finished_phases, False)

                self.say_score(score + 1)

                finished_phases = {str(i): False for i in range(6)}