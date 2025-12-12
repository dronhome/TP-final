import time
import math
import random
import sys
import os

from robot_exercise_utils import RobotExerciseUtils
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import lower_arms_from_sitting_position


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


class forefootingArmRaising(RobotExerciseUtils):
      
    def __init__(self, naoqi_instance):
        super(forefootingArmRaising, self).__init__(naoqi_instance)

        self.exercise_name = ''

    def warning_say(self):
        pass
    
    def run_exercise(self, score, message, pending_messages, phase, conn):
        if message == 'forefooting_arm_raising_start,':
            sit_on_chair_times = [[time / self.FAST_MODE_MULTIPLIER for time in times] for times in sit_on_chair.times] if self.FAST_MODE else sit_on_chair.times
            self.naoqi.motionProxy.angleInterpolationBezier(sit_on_chair.names, sit_on_chair_times, sit_on_chair.keys)

            self.naoqi.speak_or_message("Začíname cvičiť prednožovaňie a zdvíhaňie rúk.")
            self.remove_items_by_value(pending_messages, score, -1, finished_phases)

        if message == 'forefooting_arm_raising_en':
            self.naoqi.speak_or_message("Koniec cvičenia, Pripravíme sa na ďalší cvik.")

            stand_up_from_chair_times = [[time / self.FAST_MODE_MULTIPLIER for time in times] for times in stand_up_from_chair.times] if self.FAST_MODE else sit_on_chair.times
            self.naoqi.motionProxy.angleInterpolationBezier(stand_up_from_chair.names, stand_up_from_chair_times, stand_up_from_chair.keys)

            self.naoqi.speak_or_message("Koniec cviku prednožovaňia a zdvíhaňia rúk.")
            self.remove_items_by_value(pending_messages, score, -2, finished_phases, False)


        if message == 'forefooting_arm_raising':
            if phase == 0 and finished_phases["0"] == False:
                finished_phases["0"] = True
                self.remove_items_by_value(pending_messages, score, 0, finished_phases)

                if self.MIRRORING is True:
                    pozdvihnutie_lavej_nohy1_times = [[time / self.FAST_MODE_MULTIPLIER for time in times] for times in lift_left_leg_on_chair1.times] if self.FAST_MODE else lift_left_leg_on_chair1.times
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

                shoulder_pitch = -1.4
                shoulder_roll = 0.0
                elbow_yaw = 0.0
                elbow_roll = 0.0
                wrist_yaw = 0.0

                left_arm_angles = [shoulder_pitch, shoulder_roll, elbow_yaw, elbow_roll, wrist_yaw]
                right_arm_angles = [shoulder_pitch, -shoulder_roll, -elbow_yaw, -elbow_roll, -wrist_yaw]

                self.naoqi.motionProxy.setAngles(["LShoulderPitch", "LShoulderRoll", "LElbowYaw", "LElbowRoll", "LWristYaw"] + 
                                        ["RShoulderPitch", "RShoulderRoll", "RElbowYaw", "RElbowRoll", "RWristYaw"],
                                        left_arm_angles + right_arm_angles, 
                                        0.1)  # 0.1 is the fraction of max speed
                

            
            elif phase == 3 and finished_phases["3"] == False and finished_phases["2"] == True:
                finished_phases["3"] = True
                self.remove_items_by_value(pending_messages, score, 3, finished_phases)

                self.naoqi.motionProxy.angleInterpolationBezier(lower_arms_from_sitting_position.names, lower_arms_from_sitting_position.times, lower_arms_from_sitting_position.keys)



            elif phase == 4 and finished_phases["4"] == False and finished_phases["3"] == True:
                finished_phases["4"] = True
                self.remove_items_by_value(pending_messages, score, 4, finished_phases)

                if self.MIRRORING is True:
                    lift_right_leg_on_chair_times1 = [[time / self.FAST_MODE_MULTIPLIER for time in times] for times in lift_right_leg_on_chair1.times] if self.FAST_MODE else lift_right_leg_on_chair1.times
                    lift_right_leg_on_chair_times2 = [[time / self.FAST_MODE_MULTIPLIER for time in times] for times in lift_right_leg_on_chair2.times] if self.FAST_MODE else lift_right_leg_on_chair2.times
                    lift_right_leg_on_chair_times3 = [[time / self.FAST_MODE_MULTIPLIER for time in times] for times in lift_right_leg_on_chair3.times] if self.FAST_MODE else lift_right_leg_on_chair3.times

                    self.naoqi.motionProxy.angleInterpolationBezier(lift_right_leg_on_chair1.names, lift_right_leg_on_chair_times1, lift_right_leg_on_chair1.keys)
                    self.naoqi.motionProxy.angleInterpolationBezier(lift_right_leg_on_chair2.names, lift_right_leg_on_chair_times2, lift_right_leg_on_chair2.keys)
                else:
                    pozdvihnutie_lavej_nohy1_times = [[time / self.FAST_MODE_MULTIPLIER for time in times] for times in lift_left_leg_on_chair1.times] if self.FAST_MODE else lift_left_leg_on_chair1.times
                    self.naoqi.motionProxy.angleInterpolationBezier(lift_left_leg_on_chair1.names, pozdvihnutie_lavej_nohy1_times, lift_left_leg_on_chair1.keys)


            
            elif phase == 5 and finished_phases["5"] == False and finished_phases["4"] == True:
                finished_phases["5"] = True
                self.remove_items_by_value(pending_messages, score, 5, finished_phases)

                self.naoqi.motionProxy.angleInterpolationBezier(vratenie_zdvihnutych_noh_v_sede.names, vratenie_zdvihnutych_noh_v_sede.times, vratenie_zdvihnutych_noh_v_sede.keys)



            elif phase == 6 and finished_phases["6"] == False and finished_phases["5"] == True:
                finished_phases["6"] = True
                self.remove_items_by_value(pending_messages, score, 6, finished_phases)

                self.naoqi.motionProxy.angleInterpolationBezier(vratenie_zdvihnutych_noh_v_sede.names, vratenie_zdvihnutych_noh_v_sede.times, vratenie_zdvihnutych_noh_v_sede.keys)
                shoulder_pitch = -1.4
                shoulder_roll = 0.0
                elbow_yaw = 0.0
                elbow_roll = 0.0
                wrist_yaw = 0.0

                left_arm_angles = [shoulder_pitch, shoulder_roll, elbow_yaw, elbow_roll, wrist_yaw]
                right_arm_angles = [shoulder_pitch, -shoulder_roll, -elbow_yaw, -elbow_roll, -wrist_yaw]

                self.naoqi.motionProxy.setAngles(["LShoulderPitch", "LShoulderRoll", "LElbowYaw", "LElbowRoll", "LWristYaw"] + 
                                        ["RShoulderPitch", "RShoulderRoll", "RElbowYaw", "RElbowRoll", "RWristYaw"],
                                        left_arm_angles + right_arm_angles, 
                                        0.1)  # 0.1 is the fraction of max speed
                
                
            elif phase == 7 and finished_phases["7"] == False and finished_phases["6"] == True:
                finished_phases["7"] = True

                self.naoqi.motionProxy.angleInterpolationBezier(lower_arms_from_sitting_position.names, lower_arms_from_sitting_position.times, lower_arms_from_sitting_position.keys)

                self.remove_items_by_value(pending_messages, score, 7, finished_phases)


            elif phase == 8 and finished_phases["8"] == False and finished_phases["7"] == True:
                finished_phases["8"] = True
                self.remove_items_by_value(pending_messages, score, 8, finished_phases, False)

                self.say_score(score + 1)

                finished_phases = {str(i): False for i in range(10)}