
import time
import math
import random
import sys
import os

from robot_exercise_utils import RobotExerciseUtils
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

module_path = os.path.join(os.getcwd(), 'iba_zdvihanie_noh')
if module_path not in sys.path:
    sys.path.append(module_path)

import left_leg_exercise
import right_leg_exercise
import go_back_to_stable_position
import go_back_to_stable_position_pld

class ZvihaniePravejNohy(RobotExerciseUtils):
    
      
    def __init__(self, naoqi_instance):
        super(ZvihaniePravejNohy, self).__init__(naoqi_instance)
        self.exercise_name = 'pnoha'
        self.starting_sentence = "Začiatok cviku, upažovanie"

    def run_exercise(self, score, message, conn):

        if message == 'lift_right_leg_start':
            self.naoqi.speak_or_message("Teraz vymeňťe strany.")
            self.naoqi.postureProxy.goToPosture(self.zakladna_pozicia_statia, 0.5)

        elif 'lift_right_leg_end' in message:
            self.motionProxy.angleInterpolationBezier(go_back_to_stable_position_pld.names, go_back_to_stable_position_pld.times, go_back_to_stable_position_pld.keys)
            self.naoqi.speak_or_message("Koniec dvíhaňia kolien. Dáme si petnásťsekundovú prestávku.")
            time.sleep(1)
            self.naoqi.postureProxy.goToPosture(self.zakladna_pozicia_statia, 0.5)


        elif message == 'right_leg_down':
            # set center of gravity to left leg
            self.motionProxy.post.angleInterpolation(
                left_leg_exercise.names, left_leg_exercise.keys, left_leg_exercise.times, True)

            time.sleep(3.5)

            self.say_score(score, conn)


            time.sleep(1)

            if score < 4:
                self.naoqi.speak_or_message("Zdvihňite pravé koleno a ľavú ruku upažťe")
                # speechProxy.post.say(str("Zdvihňite pravé koleno a ľavú ruku upažťe"))
            else:
                self.naoqi.speak_or_message("Zopakujeme znovu")
                # speechProxy.post.say(str("Zopakujeme znovu"))           

            jointNames = ["LKneePitch", "LAnklePitch", "LHipPitch", "RShoulderRoll", "RElbowRoll"]
            targetAngles = [
                [1.4],  # LKneePitch, adjusted to approximately 57.3 degrees
                [-0.65],  # LAnklePitch, adjusted to approximately -34.38 degrees
                [-0.8],  # LHipPitch, adjusted to approximately -40.15 degrees
                
                [-1.3264502315],  # RShoulderRoll, adjusted to approximately -57.3 degrees (negated for symmetry)
                [-1.3264502315]   # RElbowRoll, adjusted to approximately -57.3 degrees (negated for symmetry)
            ]
            times = [[3], [3], [3], [3], [3]]
            self.motionProxy.angleInterpolation(jointNames, targetAngles, times, False)

        elif message == 'right_leg_up':
            time.sleep(0.5)
            self.motionProxy.angleInterpolationBezier(go_back_to_stable_position_pld.names, go_back_to_stable_position_pld.times, go_back_to_stable_position_pld.keys)

            if score < 4:
                self.naoqi.speak_or_message("Poľožťe nohu na zem a ľavú ruku pripažťe")
                # speechProxy.post.say(str("Poľožťe nohu na zem a ľavú ruku pripažťe"))
