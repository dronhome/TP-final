# -*- coding: utf-8 -*-

import sys
import os

from robot_exercise_utils import RobotExerciseUtils

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

module_path = os.path.join(os.getcwd(), 'lah')
if module_path not in sys.path:
    sys.path.append(module_path)

import prava_noha_vyrovnaj_po_zakl_lahu
import vyrovna_ruky_v_lahu_vedla_tela

import daj_ruky_hore_v_lahu
import lava_noha_prava_ruka_hore
import prava_noha_lava_ruka_hore
import prava_noha_lava_ruka_naspat
import lava_noha_prava_ruka_naspat
import daj_ruky_k_telu_v_lahu


class KriznyforefootingInLying(RobotExerciseUtils):
    starting_sentence = 'Ľahňi si na chrbát a vystri ruky nad hlavu.'

      
    def __init__(self, naoqi_instance):
        self.is_lying = True
        super(KriznyforefootingInLying, self).__init__(naoqi_instance)
        self.exercise_name = ''
        

    def go_down(self):
        self.naoqi.postureProxy.goToPosture("LyingBack", 1.0)
        self.naoqi.motionProxy.angleInterpolationBezier(vyrovna_ruky_v_lahu_vedla_tela.names, vyrovna_ruky_v_lahu_vedla_tela.times, vyrovna_ruky_v_lahu_vedla_tela.keys)
        self.naoqi.motionProxy.angleInterpolationBezier(prava_noha_vyrovnaj_po_zakl_lahu.names, prava_noha_vyrovnaj_po_zakl_lahu.times, prava_noha_vyrovnaj_po_zakl_lahu.keys)
        self.naoqi.motionProxy.angleInterpolationBezier(daj_ruky_hore_v_lahu.names, daj_ruky_hore_v_lahu.times, daj_ruky_hore_v_lahu.keys)
    
    def go_up(self):
        self.naoqi.postureProxy.goToPosture("Crouch", 1.0)
        self.naoqi.speak_or_message("Koniec cvičenia, Pripravíme sa na ďalší cvik.")
    

    def say_lying_emotion(self, message):
        if "start" in message:
            self.say_emotion_start(message, self.starting_sentence)
            self.go_down()
        elif "end" in message:
            self.say_emotion_end(message)
            self.go_up()

  
    def run_exercise(self, score, message, pending_messages, phase, conn):
        
        if message == 'krizny_forefooting_in_lying_start,':
            self.remove_items_by_value(pending_messages, score, -1, self.finished_phases)
            
            if self.naoqi.er:
                conn.send("getEmotion_lyingStart".encode())
            else:
                self.naoqi.speak_or_message(self.starting_sentence)
                self.go_down()
                conn.send("ExerciseContinue_KriznyLying".encode())

        if message == 'krizny_forefooting_in_lying_en':
            self.remove_items_by_value(pending_messages, score, -2, self.finished_phases, False)

            self.naoqi.motionProxy.angleInterpolationBezier(daj_ruky_k_telu_v_lahu.names, daj_ruky_k_telu_v_lahu.times, daj_ruky_k_telu_v_lahu.keys)
            
            if self.naoqi.er:
                conn.send("getEmotion_lyingEnd".encode())
            else:
                self.go_up()
                conn.send("ExerciseContinue_KriznyLying".encode())
         


        if message == 'krizny_forefooting_in_lying':
            if phase == 0 and self.finished_phases["0"] == False: # We put robot to sit first, so we do it in start

                self.finished_phases["0"] = True
                self.remove_items_by_value(pending_messages, score, 0, self.finished_phases)

                self.naoqi.motionProxy.angleInterpolationBezier(prava_noha_lava_ruka_hore.names, prava_noha_lava_ruka_hore.times, prava_noha_lava_ruka_hore.keys)
                
                conn.send(("ExerciseContinue_KriznyLying" + str(phase)).encode())


            elif phase == 1 and self.finished_phases["1"] == False and self.finished_phases["0"] == True:

                self.finished_phases["1"] = True
                self.remove_items_by_value(pending_messages, score, 1, self.finished_phases)

                self.naoqi.motionProxy.angleInterpolationBezier(prava_noha_lava_ruka_naspat.names, prava_noha_lava_ruka_naspat.times, prava_noha_lava_ruka_naspat.keys)
                conn.send(("ExerciseContinue_KriznyLying" + str(phase)).encode())



            elif phase == 2 and self.finished_phases["2"] == False and self.finished_phases["1"] == True:

                self.finished_phases["2"] = True
                self.remove_items_by_value(pending_messages, score, 2, self.finished_phases)

                self.naoqi.motionProxy.angleInterpolationBezier(lava_noha_prava_ruka_hore.names, lava_noha_prava_ruka_hore.times, lava_noha_prava_ruka_hore.keys)
                conn.send(("ExerciseContinue_KriznyLying" + str(phase)).encode())
                

            elif phase == 3 and self.finished_phases["3"] == False and self.finished_phases["2"] == True:


                self.finished_phases["3"] = True
                self.remove_items_by_value(pending_messages, score, 3, self.finished_phases)

                self.naoqi.motionProxy.angleInterpolationBezier(lava_noha_prava_ruka_naspat.names, lava_noha_prava_ruka_naspat.times, lava_noha_prava_ruka_naspat.keys)
                
                conn.send(("ExerciseContinue_KriznyLying" + str(phase)).encode())


            elif phase == 4 and self.finished_phases["4"] == False and self.finished_phases["3"] == True:

                self.finished_phases["4"] = True
                
                self.say_score(score + 1, conn)
                self.remove_items_by_value(pending_messages, score, 4, self.finished_phases, False)

                self.finished_phases = {str(i): False for i in range(6)}
                
                conn.send(("ExerciseContinue_KriznyLying" + str(phase)).encode())
                    
    def warning_say(self, message):
        if "reverse_pose" in message:
            self.naoqi.speak_or_message('Zdvihli ste opačnú ruku a nohu.')
            return
        
        elif "wrong_pose" in message:
            self.naoqi.speak_or_message('Cvičenie vykonávate zle.')
            return
        
        elif "wrong_lift" in message:
            self.naoqi.speak_or_message('Zdvíhate nespravnú ruku a nohu.')
            return
        
        elif "base_pose_1" in message:
            self.naoqi.speak_or_message('Prosím zdvihnite pravú nohu a ľavú ruku')
            return

        elif "base_pose_2" in message:
            self.naoqi.speak_or_message('Prosím zdvihnite ľavú nohu a pravú ruku')
            return
        
        # *************************************
        
        elif "Iba_prava_noha_nizko" in message:
            self.naoqi.speak_or_message('Pravú nohu viacej vystriťe dohora')
            

        elif "Iba_prava_noha_daleko" in message:
            self.naoqi.speak_or_message('Pravú nohu máte príliš naklonenú k vašej hlave, otočťe ju dohora')
            
        
        elif "Iba_lava_ruka_nizko" in message:
            self.naoqi.speak_or_message('Ľavú ruku viacej vystriťe dohora.')
            
        
        elif "Iba_lava_ruka_daleko" in message:
            self.naoqi.speak_or_message('Ľavú ruku máte príliš naklonenú k vašej hlave, otočťe ju dohora')
            
        

        elif "Iba_lava_noha_nizko" in message:
            self.naoqi.speak_or_message('Ľavú nohu viacej vystriťe dohora')
            
        
        elif "Iba_lava_noha_daleko" in message:
            self.naoqi.speak_or_message('Ľavú nohu máte príliš naklonenú k vašej hlave, otočťe ju dohora')
            
        
        elif "Iba_prava_ruka_nizko" in message:
            self.naoqi.speak_or_message('Pravú ruku viacej vystriťe dohora.')
            
        
        elif "Iba_prava_ruka_daleko" in message:
            self.naoqi.speak_or_message('Pravú ruku máte príliš naklonenú k vašej hlave, otočťe ju dohora')
            
        
        
        elif "Ruka_a_noha_nizko" in message:
            self.naoqi.speak_or_message('Vystretú ruku aj nohu otočťe viacej hore.')
            
        
        elif "Ruka_a_noha_daleko" in message:
            self.naoqi.speak_or_message('Vystretá ruka a noha sú príliš posunuté k vašej hlave, dajťe ich viacej dohora.')
            
        
        # *************************************

        elif "Prava_noha_daleko_a_lava_ruka_nizko" in message:
            self.naoqi.speak_or_message('Vystretú nohu aj ruku nemáťe v kolmej pozícií.')
            
        
        elif "Prava_noha_nizko_a_lava_ruka_daleko" in message:
            self.naoqi.speak_or_message('Vystretú nohu aj ruku nemáťe v kolmej pozícií.')
            
        
        elif "Prava_ruka_nizko_a_lava_noha_daleko" in message:
            self.naoqi.speak_or_message('Vystretú nohu aj ruku nemáťe v kolmej pozícií.')
            
        
        elif "Prava_ruka_daleko_a_lava_noha_nizko" in message:
            self.naoqi.speak_or_message('Vystretú nohu aj ruku nemáťe v kolmej pozícií.')
        