# -*- coding: utf-8 -*-
import time
import math
import random
import sys
import os
from naoqi import ALProxy


sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

module_path = os.path.join(os.getcwd(), 'sadanie')
if module_path not in sys.path:
    sys.path.append(module_path)


module_path = os.path.join(os.getcwd(), 'rozpazovanie_nohy_ruky')
if module_path not in sys.path:
    sys.path.append(module_path)

module_path = os.path.join(os.getcwd(), 'predpazovanie_nohy_ruky')
if module_path not in sys.path:
    sys.path.append(module_path)


import stand_up_from_chair
import sitting_position_for_extending_legs as sit_on_chair
import daj_ruky_k_telu_zo_zakladneho_sedu as ruky_k_telu_zo_zakladneho_sedu

# Predpazovanie prava noha
import daj_ruky_k_telu_z_predpazenia_a_zdvihnutej_p_nohy as ruky_k_telu_z_predpazenia_a_zdvihnutej_p_nohy
import predpazovanie_a_zdvihanie_pravej_nohy_sucasne2 as predpazovanie_a_zdvihanie_pravej_nohy_sucasne2

# Predpazovanie lava noha
import daj_ruky_k_telu_z_predpazenia_a_zdvihnutej_l_nohy as ruky_k_telu_z_predpazenia_a_zdvihnutej_l_nohy
import predpazovanie_a_zdvihanie_lavej_nohy_sucasne as predpazovanie_a_zdvihanie_lavej_nohy_sucasne

FAST_MODE = True # Robot movements will be faster
FAST_MODE_MULTIPLIER = 1
"192.168.220.194"
motion = ALProxy("ALMotion", "192.168.86.194", 9559)
posture_proxy = ALProxy("ALRobotPosture",  "192.168.86.194", 9559)
speechProxy = ALProxy("ALTextToSpeech",  "192.168.86.194", 9559)

stand_up_from_chair_times = [[time / FAST_MODE_MULTIPLIER for time in times] for times in stand_up_from_chair.times] if FAST_MODE else sit_on_chair.times
motion.angleInterpolationBezier(stand_up_from_chair.names, stand_up_from_chair_times, stand_up_from_chair.keys)
    


