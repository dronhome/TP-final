# -*- coding: utf-8 -*-

import json
import socket
import time
import math
import random
import sys
import os

from _exercises_impl.krizny_forefooting_in_lying import KriznyforefootingInLying
from _exercises_impl.robot_exercise_utils import NaoqiConnection
from _exercises_impl.predpazovanie import Predpazovanie
from _exercises_impl.forefooting_rozpazovanie import ForefootingRozpazovanie
from _exercises_impl.forefooting_predpazovanie import ForefootingPredpazovanie
from _exercises_impl.drepy import Drepy
from _exercises_impl.upazovanie import Upazovanie
from _exercises_impl.kruzenie_v_stoji import KruzenieVStoji
from _exercises_impl.kruzenie_v_sede import KruzenieVSede
from _exercises_impl.obchadzanie_stolicky import ObchadzanieOkoloStolicky

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import config_robot

import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


# def zdvihni_hlavu():
#     # Zdvihneme hlavu
#     jointName = "HeadPitch"
#     targetAngle = -0.436
#     speed = 0.1
#     motionProxy.setAngles(jointName, targetAngle, speed)

# uz_zdvihol_hlavu = False
# zakladna_pozicia_statia = "Stand"

class RobotTrainer(object):

    HOST = config_robot.IP_SERVER
    PORT = config_robot.PORT_SERVER
    
    zakladne_cviky_bez_queue = ["tpose", "right_leg", "left_leg", "squat", "arm_circling", "arm_sit_circling", "chair_circling"]
    
    score = 0 
    score_size = 2
    use_queue = True

    warningStart = 'ExerciseContinue_'

    def __init__(self):

        print("Init connection...")

        self.naoqi_instance = None

        self.my_socket = socket.socket()

        self.my_socket.bind((self.HOST, self.PORT))
        self.my_socket.listen(5)
        self.conn, self.addr = self.my_socket.accept()
        
        self.curr_exercise = None
        
    def contains_keywords(self, text, keywords):
        return any(keyword in text for keyword in keywords)
    
    def robot_loop(self):
      
        message = "init"
        print("Waiting.....")

        while message:

            message = self.conn.recv(1024)
            
            print('\n')
            print('Received from camera app: ',message)
            print('\n')
            
            if "config" in message:
                config_msg = message.split(';', 1)
                config_input = json.loads(config_msg[1])
                
                if self.naoqi_instance != None:
                    print("Reseting naoqi connection")
                    # Release other service proxies
                    self.naoqi_instance.app = None 
                    self.naoqi_instance = None

                self.naoqi_instance = NaoqiConnection(config_input)
            
            elif "warning" in message:
               
               self.curr_exercise.warning_say(message)
               self.conn.send(self.warningStart + self.curr_exercise.exercise_name + "_warn")
            
            elif "fer" in message:
                print(self.curr_exercise.naoqi.gender)
                if "fer_start"  in message:
                    self.curr_exercise.say_emotion_start(message, self.curr_exercise.starting_sentence)
    
                elif "fer_end"  in message:
                    self.curr_exercise.say_emotion_end(message)
                
                elif "fer_forefooting"  in message:
                    self.curr_exercise.say_forefooting_emotion(message)
                
                elif "fer_lying"  in message:
                    self.curr_exercise.say_lying_emotion(message)
                
                self.conn.send(self.warningStart + self.curr_exercise.exercise_name)
            
            elif not self.contains_keywords(message, self.zakladne_cviky_bez_queue):
                print("Queue")
                self.exercise_in_queue(message)
            else:
                print("No queue")
                self.exercise_not_in_queue(message)
            
            continue
        self.app.stop() 

    def exercise_in_queue(self, message, pending_messages = []):

        if "fullfilled" not in message:
            self.score = message[:self.score_size]
            message = message[self.score_size:]
            score = int(self.score)

            print("Sprava bez fullfilled:")
            print(message)
            
            if "forefooting_on_chair_end," in message:
                message = message.replace("forefooting_on_chair_end,", "forefooting_on_chair_en")
                pending_messages.append((score, message, -2))
            
            elif "sit_stand_raise_arms_end," in message:
                message = message.replace("sit_stand_raise_arms_end,", "sit_stand_raise_arms_en")
                pending_messages.append((score, message, -2))
            
            elif "forefooting_arm_raising_end," in message:
                message = message.replace("forefooting_arm_raising_end,", "forefooting_arm_raising_en")
                pending_messages.append((score, message, -2))

            elif "forefooting_rozpazovanie_end," in message:
                message = message.replace("forefooting_rozpazovanie_end,", "forefooting_rozpazovanie_en")
                pending_messages.append((score, message, -2))
            
            elif "forefooting_predpazovanie_end," in message:
                message = message.replace("forefooting_predpazovanie_end,", "forefooting_predpazovanie_en")
                pending_messages.append((score, message, -2))
            
            elif "forefooting_ruky_nad_hlavu_end," in message:
                message = message.replace("forefooting_ruky_nad_hlavu_end,", "forefooting_ruky_nad_hlavu_en")
                pending_messages.append((score, message, -2))
            
            elif "forefooting_ruky_pri_tele_end," in message:
                message = message.replace("forefooting_ruky_pri_tele_end,", "forefooting_ruky_pri_tele_en")
                pending_messages.append((score, message, -2))

            elif "forefooting_in_lying_end," in message:
                message = message.replace("forefooting_in_lying_end,", "forefooting_in_lying_en")
                pending_messages.append((score, message, -2))
            
            elif "krizny_forefooting_in_lying_end," in message:
                message = message.replace("krizny_forefooting_in_lying_end,", "krizny_forefooting_in_lying_en")
                pending_messages.append((score, message, -2))
            
            elif "sadanie_na_stolicku_end," in message:
                message = message.replace("sadanie_na_stolicku_end,", "sadanie_na_stolicku_en")
                pending_messages.append((score, message, -2))

            elif "predpazovanie_end," in message:
                message = message.replace("predpazovanie_end,", "predpazovanie_en")
                pending_messages.append((score, message, -2))
            
            else:
                pending_messages.append((score, message, -1))
        else:
            print("Sprava S fullfilled:")
            print(message)
            pending_messages = self.curr_exercise.extract_components(message)

        while pending_messages and (self.use_queue is True):

            score, message, phase = pending_messages[0]
            
            if message == 'krizny_forefooting_in_lying_start,':
                self.curr_exercise = KriznyforefootingInLying(self.naoqi_instance)
                self.curr_exercise.stop_tracker()

            if message == 'forefooting_rozpazovanie_start,':
                self.curr_exercise = ForefootingRozpazovanie(self.naoqi_instance)
                self.curr_exercise.stop_tracker()

            if message == 'forefooting_predpazovanie_start,':
                self.curr_exercise = ForefootingPredpazovanie(self.naoqi_instance)
                self.curr_exercise.stop_tracker()

            if message == 'predpazovanie_start,':
                self.curr_exercise = Predpazovanie(self.naoqi_instance)

            self.curr_exercise.run_exercise(score, message, pending_messages, phase, self.conn)
           

    def exercise_not_in_queue(self, message, pending_messages = []):
        self.score = message[:self.score_size]
        message = message[self.score_size:]
        score = int(self.score)

        print(message, score)
        # self.say_score(score)

        if message == 'tpose_start':
            self.curr_exercise = Upazovanie(self.naoqi_instance)

        elif message == 'squat_start':
            self.curr_exercise = Drepy(self.naoqi_instance)
        
        elif message == 'arm_circling_start':
            self.curr_exercise = KruzenieVStoji(self.naoqi_instance)
        
        elif message == 'arm_sit_circling_start':
            self.curr_exercise = KruzenieVSede(self.naoqi_instance)
            self.curr_exercise.stop_tracker()
        
        elif message == 'chair_circling_start':
            self.curr_exercise = ObchadzanieOkoloStolicky(self.naoqi_instance)
            self.curr_exercise.stop_tracker()
        
        self.curr_exercise.run_exercise(score, message, self.conn)
          

robot_app = RobotTrainer()



try:
    robot_app.robot_loop()
except Exception as e:
    print("An error occurred:", e)
finally:
    if robot_app.my_socket:
        try:
            robot_app.my_socket.close()
            print("Socket closed successfully.")
        except Exception as close_error:
            print("Error closing socket:", close_error)