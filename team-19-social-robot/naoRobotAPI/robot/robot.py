# -*- coding: utf-8 -*-
import os
import sys

print("HEllo world")
import naoqi
import socket
from naoqi import ALProxy
import time
import sadanie.sit_exercise as sit_exercise
from iba_zdvihanie_noh import left_leg_exercise, right_leg_exercise
import random
# ip_nao = 'laptop-gedo4ip1.local.'


print("Loaded")
HOST = os.environ.get("HOST_IP", '127.0.0.1')
PORT = int(os.environ.get("HOST_PORT", 1234))
ip_nao = os.environ.get("NAO_IP", '172.20.10.7')
port_nao = int(os.environ.get("NAO_PORT", 9559))

score_size = 2
print(ip_nao)
socket = socket.socket()

socket.bind((HOST, PORT))
socket.listen(5)

conn, addr = socket.accept()

print("Connected by", addr)


speechProxy = ALProxy("ALTextToSpeech", ip_nao, port_nao)
postureProxy = ALProxy("ALRobotPosture", ip_nao, port_nao)
motionProxy = ALProxy("ALMotion", ip_nao, port_nao)

# Setting wakeup mode
motionProxy.wakeUp()

postureProxy.goToPosture("StandInit", 0.5)

while True:
    print("Wheel")
    message = conn.recv(1024)
    score = message[:score_size]
    message = message[score_size:]
    score = int(score)
    # print(message)
    # robot will be one step ahead of the user
    if message == 'tpose_down':
        if score == 0:
            speechProxy.say(str("Nezabudňiťe plynule dýchať."))
        elif score == 1:
            speechProxy.say(str("Jeden"))
        elif score == 2:
            speechProxy.say(str("Dva"))
        elif score == 3:
            speechProxy.say(str("Tri, iďe vám to dobre."))
        elif score == 4:
            speechProxy.say(str("Štyri."))
        elif score == 5:
            speechProxy.say(str("Päť, už sme v polovici."))
        elif score == 6:
            speechProxy.say(str("Šesť."))
        elif score == 7:
            speechProxy.say(str("Sedem, už len tri."))
        elif score == 8:
            speechProxy.say(str("Osem, už len dva."))
        elif score == 9:
            speechProxy.say(str("Ďeveť, ešťe jeden a máme to."))
        elif score == 10:
            speechProxy.say(str("Desať, super!"))
        else:
            speechProxy.say(str(score))
        time.sleep(1)
        random.randint(0, 10)
        if score == 9:
            speechProxy.post.say(str("Posledný krát upažťe"))
        elif score < 3:
            speechProxy.post.say(str("Upažťe ruky"))
        else:
            speechProxy.post.say(str("Upažťe"))
        print(score)
        # Adjustment of arms position (Up)
        motionProxy.setAngles(["LShoulderRoll"], 1.3264502315, 0.3)
        motionProxy.setAngles(["LElbowRoll"], 1.3264502315, 0.3)

        motionProxy.setAngles(["RShoulderRoll"], -1.3264502315, 0.3)
        motionProxy.setAngles(["RElbowRoll"], -1.3264502315, 0.3)
    elif message == 'tpose_up':
        time.sleep(1)
        if score < 3:
            speechProxy.post.say(str("Pripažťe ruky"))
        else:
            speechProxy.post.say(str("Pripažťe"))
        # Adjustment of arms position (Down)
        motionProxy.setAngles(["LShoulderRoll"], 0.0, 0.3)
        motionProxy.setAngles(["LElbowRoll"], 0.0, 0.3)

        motionProxy.setAngles(["RShoulderRoll"], 0.0, 0.3)
        motionProxy.setAngles(["RElbowRoll"], 0.0, 0.3)

    elif message == 'squat_up':
        postureProxy.goToPosture("StandInit", 0.5)
        if score == 0:
            speechProxy.say(str("Pri cvičení nezabudnite plynule dýchať."))
        elif score == 1:
            speechProxy.say(str("Jeden"))
        elif score == 2:
            speechProxy.say(str("Dva"))
        elif score == 3:
            speechProxy.say(str("Tri, iďe vám to dobre."))
        elif score == 4:
            speechProxy.say(str("Štyri."))
        elif score == 5:
            speechProxy.say(str("Päť, už sme v polovici."))
        elif score == 6:
            speechProxy.say(str("Šesť."))
        elif score == 7:
            speechProxy.say(str("Sedem, už len tri."))
        elif score == 8:
            speechProxy.say(str("Osem, už len dva."))
        elif score == 9:
            speechProxy.say(str("Ďeveť, ešťe jeden a máme to."))
        elif score == 10:
            speechProxy.say(str("Ďesať, super!"))
        else:
            speechProxy.say(str(score))
        time.sleep(0.5)
        if score == 0:
            speechProxy.post.say(str("Sadňiťe si a predpažťe"))
        elif (score > 0 and score < 4) or (score == 7):
            speechProxy.post.say(
                str("Sadňiťe si s nádychom"))
        else:
            speechProxy.post.say(str("Sadnite si"))
        motionProxy.angleInterpolation(sit_exercise.names, sit_exercise.keys, sit_exercise.times, True)

    elif message == 'squat_down':
        time.sleep(0.5)
        if (score < 4 and score != 0) or (score == 7):
            speechProxy.post.say(str("Postavte sa s výdychom"))
        else:
            speechProxy.post.say(str("Postavte sa"))
        postureProxy.goToPosture("StandInit", 0.5)

    elif message == 'left_leg_down':
        # set center of gravity to one leg
        motionProxy.post.angleInterpolation(
            right_leg_exercise.names, right_leg_exercise.keys, right_leg_exercise.times, True)
        if score == 0:
            speechProxy.say(str("Pri cvičení nezabudnite plynule dýchať."))
        elif score == 1:
            speechProxy.say(str("Jeden"))
        elif score == 2:
            speechProxy.say(str("Dva"))
        elif score == 3:
            speechProxy.say(str("Tri, iďe vám to dobre."))
        elif score == 4:
            speechProxy.say(str("Štyri."))
        elif score == 5:
            speechProxy.say(str("Päť, už sme v polovici."))
        elif score == 6:
            speechProxy.say(str("Šesť."))
        elif score == 7:
            speechProxy.say(str("Sedem."))
        elif score == 8:
            speechProxy.say(str("Osem, už len dva."))
        elif score == 9:
            speechProxy.say(str("Ďeveť, ešťe jeden a máme to."))
        elif score == 10:
            speechProxy.say(str("Ďesať, super!"))
        else:
            speechProxy.say(str(score))
        time.sleep(0.5)
        if score < 4:
            speechProxy.post.say(str("Zdvihňite ľavé koleno a pravú ruku upažťe"))
        else:
            speechProxy.post.say(str("Zopakujeme znovu"))

        motionProxy.setAngles(["RKneePitch"], 1.745329252, 0.12)  # 100 deg
        motionProxy.setAngles(["RAnklePitch"], -0.872664626,0.12)  # -50 deg
        motionProxy.setAngles(["RHipPitch"],  -1.0471975512, 0.12)  # -60 deg
        # lift opposite arm for stability
        motionProxy.setAngles(["LShoulderRoll"], 1.3264502315, 0.15)
        motionProxy.setAngles(["LElbowRoll"], 1.3264502315, 0.15)

    elif message == 'left_leg_up':
        time.sleep(0.5)
        if score < 4:
            speechProxy.post.say(str("Poľožťe nohu na zem a pravú ruku pripažťe"))
        motionProxy.setAngles(["RAnklePitch"], -0.1745329252, 0.3)  # back to -10 deg
        postureProxy.goToPosture("StandInit", 0.5)

    elif message == 'right_leg_down':
        # set center of gravity to one leg
        motionProxy.post.angleInterpolation(
            left_leg_exercise.names, left_leg_exercise.keys, left_leg_exercise.times, True)
        if score == 0:
            speechProxy.say(str("Poďme na to!"))
        elif score == 1:
            speechProxy.say(str("Jeden"))
        elif score == 2:
            speechProxy.say(str("Dva"))
        elif score == 3:
            speechProxy.say(str("Tri, iďe vám to dobre."))
        elif score == 4:
            speechProxy.say(str("Štyri."))
        elif score == 5:
            speechProxy.say(str("Päť, už sme v polovici."))
        elif score == 6:
            speechProxy.say(str("Šesť."))
        elif score == 7:
            speechProxy.say(str("Sedem."))
        elif score == 8:
            speechProxy.say(str("Osem, už len dva."))
        elif score == 9:
            speechProxy.say(str("Ďeveť, ešťe jeden a máme to."))
        elif score == 10:
            speechProxy.say(str("Ďesať, super!"))
        else:
            speechProxy.say(str(score))
        time.sleep(0.5)
        if score < 4:
            speechProxy.post.say(str("Zdvihňite pravé koleno a ľavú ruku upažťe"))
        else:
            speechProxy.post.say(str("Zopakujeme znovu"))
        motionProxy.setAngles(["LKneePitch"], 1.745329252, 0.12)  # 100 degrees
        motionProxy.setAngles(["LAnklePitch"], -0.872664626, 0.12)  # -60 degrees
        motionProxy.setAngles(["LHipPitch"], -1.0471975512, 0.12)  # -60 deg

        # lift opposite arm for stability
        motionProxy.setAngles(["RShoulderRoll"], -1.3264502315, 0.15)
        motionProxy.setAngles(["RElbowRoll"], -1.3264502315, 0.15)

    elif message == 'right_leg_up':
        time.sleep(0.5)
        if score < 4:
            speechProxy.post.say(str("Poľožťe nohu na zem a ľavú ruku pripažťe"))
        motionProxy.setAngles(["LAnklePitch"], -0.1745329252, 0.3)
        postureProxy.goToPosture("StandInit", 0.5)

    elif message == 'tpose_start':
        speechProxy.say(str("Začiatok cviku tri, upažovanie rúk"))
        postureProxy.goToPosture("StandInit", 0.5)

    elif message == 'tpose_end':
        speechProxy.say(str("Super, koniec cvičenia. Zvládli sťe to na jednotku."))

    elif message == 'squat_start':
        speechProxy.say(str(
            "Začíname cvičiť, prvý cvik sadanie a vstávanie zo stoličky"))
        postureProxy.goToPosture("StandInit", 0.5)
    
    elif message == 'squat_end':
        speechProxy.say(str("Výborňe, sadaňie a vstávaňie zo stoličky máme za sebou."))

    elif message == 'left_leg_start':
        speechProxy.say(str("Prejdiťe na cvik dva, dvíhaňie kolien."))
        postureProxy.goToPosture("StandInit", 0.5)
    
    elif message == 'left_leg_end':
        speechProxy.say(str(
            "Koniec dvíhaňia kolien na ľavej nohe. Teraz si dáme petnásťsekundovú prestávku."))
        postureProxy.goToPosture("StandInit", 0.5)

    elif message == 'right_leg_start':
        speechProxy.say(str("Teraz vymeňťe strany."))
        postureProxy.goToPosture("StandInit", 0.5)

    elif message == 'right_leg_end':
        speechProxy.say(
            str("Koniec dvíhaňia kolien. Dáme si petnásťsekundovú prestávku."))