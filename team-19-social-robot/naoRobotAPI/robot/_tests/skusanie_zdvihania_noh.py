# -*- encoding: UTF-8 -*- 

'''Cartesian control: Multiple Effector Trajectories'''

import sys
import motion
import almath
from naoqi import ALProxy
import math
import argparse
import qi
import time

import sitting_position_for_extending_legs as sit_on_chair
import stand_up_from_chair
import put_arms_next_to_body
import lift_right_leg_on_chair2
import lift_right_leg_on_chair3
import lower_arms_from_sitting_position

import lift_left_leg_on_chair1
import vyrovna_ruky_v_lahu_vedla_tela
import poloha_lahu_vymenena_noha
import prava_noha_vyrovnaj_po_zakl_lahu
import prava_noha_zdvihnuta_v_lahu_naspat
import lava_noha_naspat_v_lahu

import robot._tests.rozpaz_ruky as rozpaz_ruky
import vratenie_rozpazenych_ruk_v_sede
import os

FAST_MODE = False # Robot movements will be faster
FAST_MODE_MULTIPLIER = 1

def StiffnessOn(proxy):
    # We use the "Body" name to signify the collection of all joints
    pNames = "Body"
    pStiffnessLists = 1.0
    pTimeLists = 1.0
    proxy.stiffnessInterpolation(pNames, pStiffnessLists, pTimeLists)

physicalIP="172.20.10.7"
virtualIP="127.0.0.1"

robotIp=virtualIP

physical=False

if physical:
    robotIp=physicalIP


module_path = os.path.join(os.getcwd(), 'rozpazovanie')
if module_path not in sys.path:
    sys.path.append(module_path)

module_path = os.path.join(os.getcwd(), 'predpazovanie')
if module_path not in sys.path:
    sys.path.append(module_path)

module_path = os.path.join(os.getcwd(), 'ruky_nad_hlavu')
if module_path not in sys.path:
    sys.path.append(module_path)

module_path = os.path.join(os.getcwd(), 'lah')
if module_path not in sys.path:
    sys.path.append(module_path)

module_path = os.path.join(os.getcwd(), 'iba_zdvihanie_noh')
if module_path not in sys.path:
    sys.path.append(module_path)

# Ruky k sebe v zakladnom sede
import daj_ruky_k_telu_zo_zakladneho_sedu as ruky_k_telu_zo_zakladneho_sedu

# Rozpazovanie simultanne
import vratenie_zdvihnutych_noh_v_sede_bez_ruk
import lift_right_leg_on_chair_no_arms

# Rozpazovanie prava noha
import rozpazovanie_a_zdvihanie_pravej_nohy_sucasne as rozpazovanie_zdvihanie_pravej_nohy_sucasne
import daj_ruky_k_telu_z_rozpazenia as ruky_k_telu_z_rozpazenia

# Rozpazovanie lava noha
import daj_ruky_k_telu_z_rozpazenia_a_zdvihnutej_l_nohy as ruky_k_telu_z_rozpazenia_a_zdvihnutej_l_nohy
import prednozovanie_a_zdvihanie_lavej_nohy_sucasne as rozpazovanie_a_zdvihanie_lavej_nohy_sucasne_l_nohy

# Predpazovanie prava noha
import daj_ruky_k_telu_z_predpazenia_a_zdvihnutej_p_nohy as ruky_k_telu_z_predpazenia_a_zdvihnutej_p_nohy
import predpazovanie_a_zdvihanie_pravej_nohy_sucasne2 as predpazovanie_a_zdvihanie_pravej_nohy_sucasne2

# Predpazovanie lava noha
import daj_ruky_k_telu_z_predpazenia_a_zdvihnutej_l_nohy as ruky_k_telu_z_predpazenia_a_zdvihnutej_l_nohy
import predpazovanie_a_zdvihanie_lavej_nohy_sucasne as predpazovanie_a_zdvihanie_lavej_nohy_sucasne

# Ruky nad hlavou prava noha
import daj_ruky_k_telu_z_nad_hlavou_a_zdvihnutej_p_nohy as ruky_k_telu_z_nad_hlavou_a_zdvihnutej_p_nohy
import ruky_nad_hlavu_a_zdvihanie_pravej_nohy as ruky_nad_hlavu_a_zdvihanie_pravej_nohy

# Ruky nad hlavou prava noha
import daj_ruky_k_telu_z_nad_hlavou_a_zdvihnutej_l_nohy as ruky_k_telu_z_nad_hlavou_a_zdvihnutej_l_nohy
import ruky_nad_hlavu_a_zdvihanie_lavej_nohy as ruky_nad_hlavu_a_zdvihanie_lavej_nohy

# Krizne zdvihanie koncatin v lahu
import daj_ruky_hore_v_lahu
import lava_noha_prava_ruka_hore
import prava_noha_lava_ruka_hore
import prava_noha_lava_ruka_naspat
import lava_noha_prava_ruka_naspat
import daj_ruky_k_telu_v_lahu

import daj_pravu_nohu_naspat
import daj_lavu_nohu_naspat
import iba_zdvihanie_pravej_nohy
import iba_zdvihanie_lavej_nohy

motionProxy = ALProxy("ALMotion", robotIp, 9559)
posture_proxy = ALProxy("ALRobotPosture", robotIp, 9559)
memory_proxy = ALProxy("ALMemory", robotIp, 9559)

def stand_up_from_sitting_on_chair():

    # Choregraphe bezier export in Python.
    names = list()
    times = list()
    keys = list()

    names.append("LShoulderPitch")
    times.append([1, 1.8])
    keys.append([[0.932006, [3, -0.346667, 0], [3, 0.266667, 0]], [0.932006, [3, -0.266667, 0], [3, 0, 0]]])

    names.append("LShoulderRoll")
    times.append([1.8])
    keys.append([[0.141372, [3, -0.613333, 0], [3, 0, 0]]])

    names.append("RShoulderPitch")
    times.append([1, 1.8])
    keys.append([[0.932006, [3, -0.346667, 0], [3, 0.266667, 0]], [0.932006, [3, -0.266667, 0], [3, 0, 0]]])

    names.append("RShoulderRoll")
    times.append([1.8])
    keys.append([[-0.141372, [3, -0.613333, 0], [3, 0, 0]]])

    motionProxy.angleInterpolationBezier(names, times, keys)


    names = list()
    times = list()
    keys = list()

    names.append("HeadPitch")
    times.append([1.16, 1.96, 2.76, 3.56, 4.76, 6.04, 7.36, 8.76])
    keys.append([[-0.169649, [3, -0.4, 0], [3, 0.266667, 0]], [-0.16606, [3, -0.266667, 0], [3, 0.266667, 0]], [-0.16606, [3, -0.266667, 0], [3, 0.266667, 0]], [-0.16606, [3, -0.266667, 0], [3, 0.4, 0]], [-0.16606, [3, -0.4, 0], [3, 0.426667, 0]], [-0.166005, [3, -0.426667, -6.45615e-08], [3, 0.44, 6.6579e-08]], [-0.166005, [3, -0.44, 0], [3, 0.466667, 0]], [-0.166005, [3, -0.466667, 0], [3, 0, 0]]])

    names.append("HeadYaw")
    times.append([1.16, 1.96, 2.76, 3.56, 4.76, 6.04, 7.36, 8.76])
    keys.append([[0, [3, -0.4, 0], [3, 0.266667, 0]], [0, [3, -0.266667, 0], [3, 0.266667, 0]], [0, [3, -0.266667, 0], [3, 0.266667, 0]], [0, [3, -0.266667, 0], [3, 0.4, 0]], [0, [3, -0.4, 0], [3, 0.426667, 0]], [0.00269869, [3, -0.426667, -7.81799e-09], [3, 0.44, 8.0623e-09]], [0.0026987, [3, -0.44, 0], [3, 0.466667, 0]], [0.00269869, [3, -0.466667, 0], [3, 0, 0]]])

    names.append("LAnklePitch")
    times.append([1.16, 1.96, 2.76, 3.56, 4.76, 6.04, 7.36, 8.76])
    keys.append([[0.339913, [3, -0.4, 0], [3, 0.266667, 0]], [0.349066, [3, -0.266667, 0], [3, 0.266667, 0]], [0.349066, [3, -0.266667, 0], [3, 0.266667, 0]], [0.349066, [3, -0.266667, 0], [3, 0.4, 0]], [0.261799, [3, -0.4, 0.0780552], [3, 0.426667, -0.0832589]], [-0.134877, [3, -0.426667, 0], [3, 0.44, 0]], [-0.134877, [3, -0.44, -5.82566e-08], [3, 0.466667, 6.17874e-08]], [0.0768539, [3, -0.466667, 0], [3, 0, 0]]])

    names.append("LAnkleRoll")
    times.append([1.16, 1.96, 2.76, 3.56, 4.76, 6.04, 7.36, 8.76])
    keys.append([[-0.00625884, [3, -0.4, 0], [3, 0.266667, 0]], [0, [3, -0.266667, 0], [3, 0.266667, 0]], [0, [3, -0.266667, 0], [3, 0.266667, 0]], [0, [3, -0.266667, 0], [3, 0.4, 0]], [0, [3, -0.4, 0], [3, 0.426667, 0]], [0.00043631, [3, -0.426667, 0], [3, 0.44, 0]], [0.00043631, [3, -0.44, 9.75279e-11], [3, 0.466667, -1.03439e-10]], [-0.0981274, [3, -0.466667, 0], [3, 0, 0]]])

    names.append("LElbowRoll")
    times.append([1.16, 1.96, 2.76, 3.56, 4.76, 6.04, 7.36, 8.76])
    keys.append([[-1.35327, [3, -0.4, 0], [3, 0.266667, 0]], [-1.35088, [3, -0.266667, 0], [3, 0.266667, 0]], [-1.35088, [3, -0.266667, 0], [3, 0.266667, 0]], [-1.35088, [3, -0.266667, 0], [3, 0.4, 0]], [-1.35088, [3, -0.4, 0], [3, 0.426667, 0]], [-1.07643, [3, -0.426667, 0], [3, 0.44, 0]], [-1.07643, [3, -0.44, 0], [3, 0.466667, 0]], [-1.07643, [3, -0.466667, 0], [3, 0, 0]]])

    names.append("LElbowYaw")
    times.append([1.16, 1.96, 2.76, 3.56, 4.76, 6.04, 7.36, 8.76])
    keys.append([[-1.38611, [3, -0.4, 0], [3, 0.266667, 0]], [-1.39483, [3, -0.266667, 0], [3, 0.266667, 0]], [-1.39483, [3, -0.266667, 0], [3, 0.266667, 0]], [-1.39483, [3, -0.266667, 0], [3, 0.4, 0]], [-1.39483, [3, -0.4, 0], [3, 0.426667, 0]], [-0.791883, [3, -0.426667, -4.5193e-07], [3, 0.44, 4.66053e-07]], [-0.791882, [3, -0.44, 0], [3, 0.466667, 0]], [-0.791883, [3, -0.466667, 0], [3, 0, 0]]])

    names.append("LHand")
    times.append([1.16, 1.96, 2.76, 3.56, 4.76, 6.04, 7.36, 8.76])
    keys.append([[0.304691, [3, -0.4, 0], [3, 0.266667, 0]], [0.304691, [3, -0.266667, 0], [3, 0.266667, 0]], [0.304691, [3, -0.266667, 0], [3, 0.266667, 0]], [0.304691, [3, -0.266667, 0], [3, 0.4, 0]], [0.304691, [3, -0.4, 0], [3, 0.426667, 0]], [0.299044, [3, -0.426667, 1.15597e-07], [3, 0.44, -1.19209e-07]], [0.299044, [3, -0.44, 0], [3, 0.466667, 0]], [0.299044, [3, -0.466667, 0], [3, 0, 0]]])

    names.append("LHipPitch")
    times.append([1.16, 1.96, 2.76, 3.56, 4.76, 6.04, 7.36, 8.76])
    keys.append([[-1.2303, [3, -0.4, 0], [3, 0.266667, 0]], [-1.32471, [3, -0.266667, 0], [3, 0.266667, 0]], [-1.32471, [3, -0.266667, 0], [3, 0.266667, 0]], [-1.32471, [3, -0.266667, 0], [3, 0.4, 0]], [-1.32471, [3, -0.4, 0], [3, 0.426667, 0]], [-0.634814, [3, -0.426667, 0], [3, 0.44, 0]], [-0.634815, [3, -0.44, 0], [3, 0.466667, 0]], [0.120077, [3, -0.466667, 0], [3, 0, 0]]])

    names.append("LHipRoll")
    times.append([1.16, 1.96, 2.76, 3.56, 4.76, 6.04, 7.36, 8.76])
    keys.append([[-0.0376726, [3, -0.4, 0], [3, 0.266667, 0]], [-0.0349066, [3, -0.266667, 0], [3, 0.266667, 0]], [-0.0523599, [3, -0.266667, 0.0116355], [3, 0.266667, -0.0116355]], [-0.10472, [3, -0.266667, 0], [3, 0.4, 0]], [-0.0872665, [3, -0.4, -0.0158846], [3, 0.426667, 0.0169436]], [-0.00623519, [3, -0.426667, -1.00877e-09], [3, 0.44, 1.0403e-09]], [-0.00623519, [3, -0.44, -1.0403e-09], [3, 0.466667, 1.10335e-09]], [0.104047, [3, -0.466667, 0], [3, 0, 0]]])

    names.append("LHipYawPitch")
    times.append([1.16, 1.96, 2.76, 3.56, 4.76, 6.04, 7.36, 8.76])
    keys.append([[-0.486947, [3, -0.4, 0], [3, 0.266667, 0]], [-0.523599, [3, -0.266667, 0.0206531], [3, 0.266667, -0.0206531]], [-0.610865, [3, -0.266667, 0.0290888], [3, 0.266667, -0.0290888]], [-0.698132, [3, -0.266667, 0], [3, 0.4, 0]], [-0.610865, [3, -0.4, 0], [3, 0.426667, 0]], [-0.750492, [3, -0.426667, 0.0612924], [3, 0.44, -0.0632078]], [-0.984366, [3, -0.44, 0], [3, 0.466667, 0]], [-0.175861, [3, -0.466667, 0], [3, 0, 0]]])

    names.append("LKneePitch")
    times.append([1.16, 1.96, 2.76, 3.56, 4.76, 6.04, 7.36, 8.76])
    keys.append([[1.04742, [3, -0.4, 0], [3, 0.266667, 0]], [1.11701, [3, -0.266667, 0], [3, 0.266667, 0]], [1.11701, [3, -0.266667, 0], [3, 0.266667, 0]], [1.11701, [3, -0.266667, 0], [3, 0.4, 0]], [1.0472, [3, -0.4, 0], [3, 0.426667, 0]], [1.053, [3, -0.426667, 0], [3, 0.44, 0]], [1.04545, [3, -0.44, 0.00754926], [3, 0.466667, -0.00800679]], [-0.0767842, [3, -0.466667, 0], [3, 0, 0]]])

    names.append("LShoulderPitch")
    times.append([1.16, 1.96, 2.76, 3.56, 4.76, 6.04, 7.36, 8.76])
    keys.append([[0.45115, [3, -0.4, 0], [3, 0.266667, 0]], [0.441568, [3, -0.266667, 0], [3, 0.266667, 0]], [0.441568, [3, -0.266667, 0], [3, 0.266667, 0]], [0.441568, [3, -0.266667, 0], [3, 0.4, 0]], [0.441568, [3, -0.4, 0], [3, 0.426667, 0]], [1.39654, [3, -0.426667, 0], [3, 0.44, 0]], [1.39654, [3, -0.44, 7.98948e-07], [3, 0.466667, -8.47369e-07]], [1.38519, [3, -0.466667, 0], [3, 0, 0]]])

    names.append("LShoulderRoll")
    times.append([1.16, 1.96, 2.76, 3.56, 4.76, 6.04, 7.36, 8.76])
    keys.append([[0.293906, [3, -0.4, 0], [3, 0.266667, 0]], [0.302179, [3, -0.266667, 0], [3, 0.266667, 0]], [0.302179, [3, -0.266667, 0], [3, 0.266667, 0]], [0.302179, [3, -0.266667, 0], [3, 0.4, 0]], [0.302179, [3, -0.4, 0], [3, 0.426667, 0]], [0.166304, [3, -0.426667, 3.22807e-08], [3, 0.44, -3.32895e-08]], [0.166304, [3, -0.44, 0], [3, 0.466667, 0]], [0.166304, [3, -0.466667, 0], [3, 0, 0]]])

    names.append("LWristYaw")
    times.append([1.16, 1.96, 2.76, 3.56, 4.76, 6.04, 7.36, 8.76])
    keys.append([[0.145701, [3, -0.4, 0], [3, 0.266667, 0]], [0.146244, [3, -0.266667, 0], [3, 0.266667, 0]], [0.146244, [3, -0.266667, 0], [3, 0.266667, 0]], [0.146244, [3, -0.266667, 0], [3, 0.4, 0]], [0.146244, [3, -0.4, 0], [3, 0.426667, 0]], [0.145482, [3, -0.426667, 0], [3, 0.44, 0]], [0.145482, [3, -0.44, 0], [3, 0.466667, 0]], [0.145482, [3, -0.466667, 0], [3, 0, 0]]])

    names.append("RAnklePitch")
    times.append([1.16, 1.96, 2.76, 3.56, 4.76, 6.04, 7.36, 8.76])
    keys.append([[0.339913, [3, -0.4, 0], [3, 0.266667, 0]], [0.349066, [3, -0.266667, 0], [3, 0.266667, 0]], [0.349066, [3, -0.266667, 0], [3, 0.266667, 0]], [0.349066, [3, -0.266667, 0], [3, 0.4, 0]], [0.261799, [3, -0.4, 0.0780552], [3, 0.426667, -0.0832589]], [-0.134877, [3, -0.426667, 0], [3, 0.44, 0]], [-0.134877, [3, -0.44, -5.82566e-08], [3, 0.466667, 6.17874e-08]], [0.0775809, [3, -0.466667, 0], [3, 0, 0]]])

    names.append("RAnkleRoll")
    times.append([1.16, 1.96, 2.76, 3.56, 4.76, 6.04, 7.36, 8.76])
    keys.append([[0.00632195, [3, -0.4, 0], [3, 0.266667, 0]], [0, [3, -0.266667, 0], [3, 0.266667, 0]], [0, [3, -0.266667, 0], [3, 0.266667, 0]], [0, [3, -0.266667, 0], [3, 0.4, 0]], [0, [3, -0.4, 0], [3, 0.426667, 0]], [-0.00043631, [3, -0.426667, 0], [3, 0.44, 0]], [-0.00043631, [3, -0.44, -9.75279e-11], [3, 0.466667, 1.03439e-10]], [0.0991166, [3, -0.466667, 0], [3, 0, 0]]])

    names.append("RElbowRoll")
    times.append([1.16, 1.96, 2.76, 3.56, 4.76, 6.04, 7.36, 8.76])
    keys.append([[1.35327, [3, -0.4, 0], [3, 0.266667, 0]], [1.35088, [3, -0.266667, 0], [3, 0.266667, 0]], [1.35088, [3, -0.266667, 0], [3, 0.266667, 0]], [1.35088, [3, -0.266667, 0], [3, 0.4, 0]], [1.35088, [3, -0.4, 0], [3, 0.426667, 0]], [1.07643, [3, -0.426667, 0], [3, 0.44, 0]], [1.07643, [3, -0.44, 0], [3, 0.466667, 0]], [1.07643, [3, -0.466667, 0], [3, 0, 0]]])

    names.append("RElbowYaw")
    times.append([1.16, 1.96, 2.76, 3.56, 4.76, 6.04, 7.36, 8.76])
    keys.append([[1.38625, [3, -0.4, 0], [3, 0.266667, 0]], [1.39483, [3, -0.266667, 0], [3, 0.266667, 0]], [1.39483, [3, -0.266667, 0], [3, 0.266667, 0]], [1.39483, [3, -0.266667, 0], [3, 0.4, 0]], [1.39483, [3, -0.4, 0], [3, 0.426667, 0]], [0.791883, [3, -0.426667, 4.5193e-07], [3, 0.44, -4.66053e-07]], [0.791882, [3, -0.44, 0], [3, 0.466667, 0]], [0.791883, [3, -0.466667, 0], [3, 0, 0]]])

    names.append("RHand")
    times.append([1.16, 1.96, 2.76, 3.56, 4.76, 6.04, 7.36, 8.76])
    keys.append([[0.293013, [3, -0.4, 0], [3, 0.266667, 0]], [0.29357, [3, -0.266667, 0], [3, 0.266667, 0]], [0.29357, [3, -0.266667, 0], [3, 0.266667, 0]], [0.29357, [3, -0.266667, 0], [3, 0.4, 0]], [0.29357, [3, -0.4, 0], [3, 0.426667, 0]], [0.288129, [3, -0.426667, 2.60093e-07], [3, 0.44, -2.68221e-07]], [0.288129, [3, -0.44, 0], [3, 0.466667, 0]], [0.288129, [3, -0.466667, 0], [3, 0, 0]]])

    names.append("RHipPitch")
    times.append([1.16, 1.96, 2.76, 3.56, 4.76, 6.04, 7.36, 8.76])
    keys.append([[-1.24064, [3, -0.4, 0], [3, 0.266667, 0]], [-1.34216, [3, -0.266667, 0], [3, 0.266667, 0]], [-1.34216, [3, -0.266667, 0], [3, 0.266667, 0]], [-1.32471, [3, -0.266667, 0], [3, 0.4, 0]], [-1.32471, [3, -0.4, 0], [3, 0.426667, 0]], [-0.634814, [3, -0.426667, 0], [3, 0.44, 0]], [-0.634815, [3, -0.44, 0], [3, 0.466667, 0]], [0.120252, [3, -0.466667, 0], [3, 0, 0]]])

    names.append("RHipRoll")
    times.append([1.16, 1.96, 2.76, 3.56, 4.76, 6.04, 7.36, 8.76])
    keys.append([[0.0376726, [3, -0.4, 0], [3, 0.266667, 0]], [0.0349066, [3, -0.266667, 0], [3, 0.266667, 0]], [0.0523599, [3, -0.266667, -0.0116355], [3, 0.266667, 0.0116355]], [0.10472, [3, -0.266667, 0], [3, 0.4, 0]], [0.0872665, [3, -0.4, 0.0158846], [3, 0.426667, -0.0169436]], [0.00623519, [3, -0.426667, 1.00877e-09], [3, 0.44, -1.0403e-09]], [0.00623519, [3, -0.44, 1.0403e-09], [3, 0.466667, -1.10335e-09]], [-0.106957, [3, -0.466667, 0], [3, 0, 0]]])

    names.append("RHipYawPitch")
    times.append([1.16, 1.96, 2.76, 3.56, 4.76, 6.04, 7.36, 8.76])
    keys.append([[-0.486947, [3, -0.4, 0], [3, 0.266667, 0]], [-0.523599, [3, -0.266667, 0.0206531], [3, 0.266667, -0.0206531]], [-0.610865, [3, -0.266667, 0.0290888], [3, 0.266667, -0.0290888]], [-0.698132, [3, -0.266667, 0], [3, 0.4, 0]], [-0.610865, [3, -0.4, 0], [3, 0.426667, 0]], [-0.750492, [3, -0.426667, 0.0612924], [3, 0.44, -0.0632078]], [-0.984366, [3, -0.44, 0], [3, 0.466667, 0]], [-0.175861, [3, -0.466667, 0], [3, 0, 0]]])

    names.append("RKneePitch")
    times.append([1.16, 1.96, 2.76, 3.56, 4.76, 6.04, 7.36, 8.76])
    keys.append([[1.04742, [3, -0.4, 0], [3, 0.266667, 0]], [1.11701, [3, -0.266667, 0], [3, 0.266667, 0]], [1.11701, [3, -0.266667, 0], [3, 0.266667, 0]], [1.11701, [3, -0.266667, 0], [3, 0.4, 0]], [1.0472, [3, -0.4, 0], [3, 0.426667, 0]], [1.053, [3, -0.426667, 0], [3, 0.44, 0]], [1.04545, [3, -0.44, 0.00754926], [3, 0.466667, -0.00800679]], [-0.0780461, [3, -0.466667, 0], [3, 0, 0]]])

    names.append("RShoulderPitch")
    times.append([1.16, 1.96, 2.76, 3.56, 4.76, 6.04, 7.36, 8.76])
    keys.append([[0.451164, [3, -0.4, 0], [3, 0.266667, 0]], [0.441568, [3, -0.266667, 0], [3, 0.266667, 0]], [0.441568, [3, -0.266667, 0], [3, 0.266667, 0]], [0.441568, [3, -0.266667, 0], [3, 0.4, 0]], [0.441568, [3, -0.4, 0], [3, 0.426667, 0]], [1.39654, [3, -0.426667, 0], [3, 0.44, 0]], [1.39654, [3, -0.44, 7.98948e-07], [3, 0.466667, -8.47369e-07]], [1.38519, [3, -0.466667, 0], [3, 0, 0]]])

    names.append("RShoulderRoll")
    times.append([1.16, 1.96, 2.76, 3.56, 4.76, 6.04, 7.36, 8.76])
    keys.append([[-0.294041, [3, -0.4, 0], [3, 0.266667, 0]], [-0.302179, [3, -0.266667, 0], [3, 0.266667, 0]], [-0.302179, [3, -0.266667, 0], [3, 0.266667, 0]], [-0.302179, [3, -0.266667, 0], [3, 0.4, 0]], [-0.302179, [3, -0.4, 0], [3, 0.426667, 0]], [-0.166304, [3, -0.426667, -3.22807e-08], [3, 0.44, 3.32895e-08]], [-0.166304, [3, -0.44, 0], [3, 0.466667, 0]], [-0.166304, [3, -0.466667, 0], [3, 0, 0]]])

    names.append("RWristYaw")
    times.append([1.16, 1.96, 2.76, 3.56, 4.76, 6.04, 7.36, 8.76])
    keys.append([[-0.13878, [3, -0.4, 0], [3, 0.266667, 0]], [-0.143533, [3, -0.266667, 0], [3, 0.266667, 0]], [-0.143533, [3, -0.266667, 0], [3, 0.266667, 0]], [-0.143533, [3, -0.266667, 0], [3, 0.4, 0]], [-0.143533, [3, -0.4, 0], [3, 0.426667, 0]], [-0.148822, [3, -0.426667, 0], [3, 0.44, 0]], [-0.148822, [3, -0.44, 0], [3, 0.466667, 0]], [-0.148822, [3, -0.466667, 0], [3, 0, 0]]])

    motionProxy.angleInterpolationBezier(names, times, keys)

def ruky_nad_hlavu_v_sede():
    shoulder_pitch = -1.4
    shoulder_roll = 0.0
    elbow_yaw = 0.0
    elbow_roll = 0.0
    wrist_yaw = 0.0

    left_arm_angles = [shoulder_pitch, shoulder_roll, elbow_yaw, elbow_roll, wrist_yaw]
    right_arm_angles = [shoulder_pitch, -shoulder_roll, -elbow_yaw, -elbow_roll, -wrist_yaw]

    motionProxy.setAngles(["LShoulderPitch", "LShoulderRoll", "LElbowYaw", "LElbowRoll", "LWristYaw"] + 
                            ["RShoulderPitch", "RShoulderRoll", "RElbowYaw", "RElbowRoll", "RWristYaw"],
                            left_arm_angles + right_arm_angles, 
                            0.1)  # 0.1 is the fraction of max speed

def raise_arm():
    # motion_proxy.wakeUp()
    # pass
    # Set stiffness to allow movement
    # motion_proxy.setStiffnesses("Body", 1.0)
    # # Define the target joint angles (in radians)
    shoulder_pitch = -1.4  # Negative value to raise the arms
    shoulder_roll = 0.0    # Zero to keep arms straight
    elbow_yaw = 0.0
    elbow_roll = 0.0
    wrist_yaw = 0.0

    # Combine the angles for both arms
    left_arm_angles = [shoulder_pitch, shoulder_roll, elbow_yaw, elbow_roll, wrist_yaw]
    right_arm_angles = [shoulder_pitch, -shoulder_roll, -elbow_yaw, -elbow_roll, -wrist_yaw]

    # print("Ahoj")
    # # Apply the joint angles
    motionProxy.setAngles(["LShoulderPitch", "LShoulderRoll", "LElbowYaw", "LElbowRoll", "LWristYaw"] + 
                            ["RShoulderPitch", "RShoulderRoll", "RElbowYaw", "RElbowRoll", "RWristYaw"],
                            left_arm_angles + right_arm_angles, 
                            0.1)  # 0.1 is the fraction of max speed
    
def prednozovanie_rozpazene_ruky():
    sit_on_chair_times = [[time / FAST_MODE_MULTIPLIER for time in times] for times in sit_on_chair.times] if FAST_MODE else sit_on_chair.times
    motionProxy.angleInterpolationBezier(sit_on_chair.names, sit_on_chair_times, sit_on_chair.keys)

    motionProxy.angleInterpolationBezier(rozpaz_ruky.names, rozpaz_ruky.times, rozpaz_ruky.keys)
                
    lift_right_leg_on_chair_no_arms_times = [[time / FAST_MODE_MULTIPLIER for time in times] for times in lift_right_leg_on_chair_no_arms.times] if FAST_MODE else lift_right_leg_on_chair_no_arms.times
    motionProxy.angleInterpolationBezier(lift_right_leg_on_chair_no_arms.names, lift_right_leg_on_chair_no_arms_times, lift_right_leg_on_chair_no_arms.keys)

    # Noha dole
    motionProxy.angleInterpolationBezier(vratenie_zdvihnutych_noh_v_sede_bez_ruk.names, vratenie_zdvihnutych_noh_v_sede_bez_ruk.times, vratenie_zdvihnutych_noh_v_sede_bez_ruk.keys)
    
    # Ruky naspat
    motionProxy.angleInterpolationBezier(vratenie_rozpazenych_ruk_v_sede.names, vratenie_rozpazenych_ruk_v_sede.times, vratenie_rozpazenych_ruk_v_sede.keys)
    
    #Vstan
    stand_up_from_sitting_on_chair()

def _rozpazovanie_zdvihanie_pravej_nohy_sucasne():
        
    sit_on_chair_times = [[time / FAST_MODE_MULTIPLIER for time in times] for times in sit_on_chair.times] if FAST_MODE else sit_on_chair.times
    motionProxy.angleInterpolationBezier(sit_on_chair.names, sit_on_chair_times, sit_on_chair.keys)
    motionProxy.angleInterpolationBezier(ruky_k_telu_zo_zakladneho_sedu.names, ruky_k_telu_zo_zakladneho_sedu.times, ruky_k_telu_zo_zakladneho_sedu.keys)

    motionProxy.angleInterpolationBezier(rozpazovanie_zdvihanie_pravej_nohy_sucasne.names, rozpazovanie_zdvihanie_pravej_nohy_sucasne.times, rozpazovanie_zdvihanie_pravej_nohy_sucasne.keys)
    motionProxy.angleInterpolationBezier(ruky_k_telu_z_rozpazenia.names, ruky_k_telu_z_rozpazenia.times, ruky_k_telu_z_rozpazenia.keys)

    # stand_up_from_sitting_on_chair()

def _rozpazovanie_zdvihanie_lavej_nohy_sucasne():
        
    sit_on_chair_times = [[time / FAST_MODE_MULTIPLIER for time in times] for times in sit_on_chair.times] if FAST_MODE else sit_on_chair.times
    # motionProxy.angleInterpolationBezier(sit_on_chair.names, sit_on_chair_times, sit_on_chair.keys)
    # motionProxy.angleInterpolationBezier(ruky_k_telu_zo_zakladneho_sedu.names, ruky_k_telu_zo_zakladneho_sedu.times, ruky_k_telu_zo_zakladneho_sedu.keys)

    motionProxy.angleInterpolationBezier(rozpazovanie_a_zdvihanie_lavej_nohy_sucasne_l_nohy.names, rozpazovanie_a_zdvihanie_lavej_nohy_sucasne_l_nohy.times, rozpazovanie_a_zdvihanie_lavej_nohy_sucasne_l_nohy.keys)
    
    motionProxy.angleInterpolationBezier(ruky_k_telu_z_rozpazenia_a_zdvihnutej_l_nohy.names, ruky_k_telu_z_rozpazenia_a_zdvihnutej_l_nohy.times, ruky_k_telu_z_rozpazenia_a_zdvihnutej_l_nohy.keys)

    # stand_up_from_sitting_on_chair()

def prednozovanie_ruky_nad_hlavou():
    sit_on_chair_times = [[time / FAST_MODE_MULTIPLIER for time in times] for times in sit_on_chair.times] if FAST_MODE else sit_on_chair.times
    motionProxy.angleInterpolationBezier(sit_on_chair.names, sit_on_chair_times, sit_on_chair.keys)
        
    ruky_nad_hlavu_v_sede()
    import time
    time.sleep(5)

    lift_right_leg_on_chair_no_arms_times = [[time / FAST_MODE_MULTIPLIER for time in times] for times in lift_right_leg_on_chair_no_arms.times] if FAST_MODE else lift_right_leg_on_chair_no_arms.times
    motionProxy.angleInterpolationBezier(lift_right_leg_on_chair_no_arms.names, lift_right_leg_on_chair_no_arms_times, lift_right_leg_on_chair_no_arms.keys)

    motionProxy.angleInterpolationBezier(vratenie_zdvihnutych_noh_v_sede_bez_ruk.names, vratenie_zdvihnutych_noh_v_sede_bez_ruk.times, vratenie_zdvihnutych_noh_v_sede_bez_ruk.keys)
    motionProxy.angleInterpolationBezier(lower_arms_from_sitting_position.names, lower_arms_from_sitting_position.times, lower_arms_from_sitting_position.keys)

def _predpazovanie_zdvihanie_pravej_nohy_sucasne():
    sit_on_chair_times = [[time / FAST_MODE_MULTIPLIER for time in times] for times in sit_on_chair.times] if FAST_MODE else sit_on_chair.times
    motionProxy.angleInterpolationBezier(sit_on_chair.names, sit_on_chair_times, sit_on_chair.keys)
    motionProxy.angleInterpolationBezier(ruky_k_telu_zo_zakladneho_sedu.names, ruky_k_telu_zo_zakladneho_sedu.times, ruky_k_telu_zo_zakladneho_sedu.keys)

    motionProxy.angleInterpolationBezier(predpazovanie_a_zdvihanie_pravej_nohy_sucasne2.names, predpazovanie_a_zdvihanie_pravej_nohy_sucasne2.times, predpazovanie_a_zdvihanie_pravej_nohy_sucasne2.keys)
    motionProxy.angleInterpolationBezier(ruky_k_telu_z_predpazenia_a_zdvihnutej_p_nohy.names, ruky_k_telu_z_predpazenia_a_zdvihnutej_p_nohy.times, ruky_k_telu_z_predpazenia_a_zdvihnutej_p_nohy.keys)
    
    stand_up_from_sitting_on_chair()

def _predpazovanie_zdvihanie_lavej_nohy_sucasne():
    sit_on_chair_times = [[time / FAST_MODE_MULTIPLIER for time in times] for times in sit_on_chair.times] if FAST_MODE else sit_on_chair.times
    motionProxy.angleInterpolationBezier(sit_on_chair.names, sit_on_chair_times, sit_on_chair.keys)
    motionProxy.angleInterpolationBezier(ruky_k_telu_zo_zakladneho_sedu.names, ruky_k_telu_zo_zakladneho_sedu.times, ruky_k_telu_zo_zakladneho_sedu.keys)

    motionProxy.angleInterpolationBezier(predpazovanie_a_zdvihanie_lavej_nohy_sucasne.names, predpazovanie_a_zdvihanie_lavej_nohy_sucasne.times, predpazovanie_a_zdvihanie_lavej_nohy_sucasne.keys)
    
    motionProxy.angleInterpolationBezier(ruky_k_telu_z_predpazenia_a_zdvihnutej_l_nohy.names, ruky_k_telu_z_predpazenia_a_zdvihnutej_l_nohy.times, ruky_k_telu_z_predpazenia_a_zdvihnutej_l_nohy.keys)
    stand_up_from_sitting_on_chair()

def _ruky_nad_hlavu_zdvihanie_pravej_nohy_sucasne():
    sit_on_chair_times = [[time / FAST_MODE_MULTIPLIER for time in times] for times in sit_on_chair.times] if FAST_MODE else sit_on_chair.times
    motionProxy.angleInterpolationBezier(sit_on_chair.names, sit_on_chair_times, sit_on_chair.keys)
    motionProxy.angleInterpolationBezier(ruky_k_telu_zo_zakladneho_sedu.names, ruky_k_telu_zo_zakladneho_sedu.times, ruky_k_telu_zo_zakladneho_sedu.keys)

    motionProxy.angleInterpolationBezier(ruky_nad_hlavu_a_zdvihanie_pravej_nohy.names, ruky_nad_hlavu_a_zdvihanie_pravej_nohy.times, ruky_nad_hlavu_a_zdvihanie_pravej_nohy.keys)
    
    motionProxy.angleInterpolationBezier(ruky_k_telu_z_nad_hlavou_a_zdvihnutej_p_nohy.names, ruky_k_telu_z_nad_hlavou_a_zdvihnutej_p_nohy.times, ruky_k_telu_z_nad_hlavou_a_zdvihnutej_p_nohy.keys)
    stand_up_from_sitting_on_chair()

def _ruky_nad_hlavu_zdvihanie_pravej_nohy_sucasne():
    sit_on_chair_times = [[time / FAST_MODE_MULTIPLIER for time in times] for times in sit_on_chair.times] if FAST_MODE else sit_on_chair.times
    motionProxy.angleInterpolationBezier(sit_on_chair.names, sit_on_chair_times, sit_on_chair.keys)
    motionProxy.angleInterpolationBezier(ruky_k_telu_zo_zakladneho_sedu.names, ruky_k_telu_zo_zakladneho_sedu.times, ruky_k_telu_zo_zakladneho_sedu.keys)

    motionProxy.angleInterpolationBezier(ruky_nad_hlavu_a_zdvihanie_pravej_nohy.names, ruky_nad_hlavu_a_zdvihanie_pravej_nohy.times, ruky_nad_hlavu_a_zdvihanie_pravej_nohy.keys)
    
    motionProxy.angleInterpolationBezier(ruky_k_telu_z_nad_hlavou_a_zdvihnutej_p_nohy.names, ruky_k_telu_z_nad_hlavou_a_zdvihnutej_p_nohy.times, ruky_k_telu_z_nad_hlavou_a_zdvihnutej_p_nohy.keys)
    stand_up_from_sitting_on_chair()

def _krizne_zdvihanie_koncatin_v_lahu():
    posture_proxy.goToPosture("LyingBack", 1.0)
    motionProxy.angleInterpolationBezier(vyrovna_ruky_v_lahu_vedla_tela.names, vyrovna_ruky_v_lahu_vedla_tela.times, vyrovna_ruky_v_lahu_vedla_tela.keys)
    motionProxy.angleInterpolationBezier(prava_noha_vyrovnaj_po_zakl_lahu.names, prava_noha_vyrovnaj_po_zakl_lahu.times, prava_noha_vyrovnaj_po_zakl_lahu.keys)
    motionProxy.angleInterpolationBezier(daj_ruky_hore_v_lahu.names, daj_ruky_hore_v_lahu.times, daj_ruky_hore_v_lahu.keys)

    motionProxy.angleInterpolationBezier(prava_noha_lava_ruka_hore.names, prava_noha_lava_ruka_hore.times, prava_noha_lava_ruka_hore.keys)
    motionProxy.angleInterpolationBezier(prava_noha_lava_ruka_naspat.names, prava_noha_lava_ruka_naspat.times, prava_noha_lava_ruka_naspat.keys)
    motionProxy.angleInterpolationBezier(lava_noha_prava_ruka_hore.names, lava_noha_prava_ruka_hore.times, lava_noha_prava_ruka_hore.keys)
    motionProxy.angleInterpolationBezier(lava_noha_prava_ruka_naspat.names, lava_noha_prava_ruka_naspat.times, lava_noha_prava_ruka_naspat.keys)
    motionProxy.angleInterpolationBezier(daj_ruky_k_telu_v_lahu.names, daj_ruky_k_telu_v_lahu.times, daj_ruky_k_telu_v_lahu.keys)
    posture_proxy.goToPosture("Crouch", 1.0)


def _ruky_nad_hlavu_zdvihanie_lavej_nohy_sucasne():

    # sit_on_chair_times = [[time / FAST_MODE_MULTIPLIER for time in times] for times in sit_on_chair.times] if FAST_MODE else sit_on_chair.times
    # motionProxy.angleInterpolationBezier(sit_on_chair.names, sit_on_chair_times, sit_on_chair.keys)
    # motionProxy.angleInterpolationBezier(ruky_k_telu_zo_zakladneho_sedu.names, ruky_k_telu_zo_zakladneho_sedu.times, ruky_k_telu_zo_zakladneho_sedu.keys)
    # motionProxy.angleInterpolationBezier(ruky_nad_hlavu_a_zdvihanie_lavej_nohy.names, ruky_nad_hlavu_a_zdvihanie_lavej_nohy.times, ruky_nad_hlavu_a_zdvihanie_lavej_nohy.keys)
    
    # motionProxy.angleInterpolationBezier(ruky_k_telu_z_nad_hlavou_a_zdvihnutej_l_nohy.names, ruky_k_telu_z_nad_hlavou_a_zdvihnutej_l_nohy.times, ruky_k_telu_z_nad_hlavou_a_zdvihnutej_l_nohy.keys)
    
    stand_up_from_sitting_on_chair()

def _iba_zdvihanie_pravej_nohy():
    # sit_on_chair_times = [[time / FAST_MODE_MULTIPLIER for time in times] for times in sit_on_chair.times] if FAST_MODE else sit_on_chair.times
    # motionProxy.angleInterpolationBezier(sit_on_chair.names, sit_on_chair_times, sit_on_chair.keys)
    # motionProxy.angleInterpolationBezier(ruky_k_telu_zo_zakladneho_sedu.names, ruky_k_telu_zo_zakladneho_sedu.times, ruky_k_telu_zo_zakladneho_sedu.keys)

    motionProxy.angleInterpolationBezier(iba_zdvihanie_pravej_nohy.names, iba_zdvihanie_pravej_nohy.times, iba_zdvihanie_pravej_nohy.keys)
    # motionProxy.angleInterpolationBezier(daj_pravu_nohu_naspat.names, daj_pravu_nohu_naspat.times, daj_pravu_nohu_naspat.keys)
    
    # stand_up_from_sitting_on_chair()

def _iba_zdvihanie_lavej_nohy():
    sit_on_chair_times = [[time / FAST_MODE_MULTIPLIER for time in times] for times in sit_on_chair.times] if FAST_MODE else sit_on_chair.times
    motionProxy.angleInterpolationBezier(sit_on_chair.names, sit_on_chair_times, sit_on_chair.keys)
    motionProxy.angleInterpolationBezier(ruky_k_telu_zo_zakladneho_sedu.names, ruky_k_telu_zo_zakladneho_sedu.times, ruky_k_telu_zo_zakladneho_sedu.keys)

    motionProxy.angleInterpolationBezier(iba_zdvihanie_lavej_nohy.names, iba_zdvihanie_lavej_nohy.times, iba_zdvihanie_lavej_nohy.keys)
    # motionProxy.angleInterpolationBezier(daj_lavu_nohu_naspat.names, daj_lavu_nohu_naspat.times, daj_lavu_nohu_naspat.keys)
    
    # stand_up_from_sitting_on_chair()

def main():
    _rozpazovanie_zdvihanie_pravej_nohy_sucasne()
    # _rozpazovanie_zdvihanie_lavej_nohy_sucasne()

    # _predpazovanie_zdvihanie_pravej_nohy_sucasne()
    # _predpazovanie_zdvihanie_lavej_nohy_sucasne()

    # _ruky_nad_hlavu_zdvihanie_pravej_nohy_sucasne()
    # _ruky_nad_hlavu_zdvihanie_lavej_nohy_sucasne()

    # _krizne_zdvihanie_koncatin_v_lahu()

    # _iba_zdvihanie_pravej_nohy()
    # _iba_zdvihanie_lavej_nohy()


    # Simultanne, nie sucasne
    # prednozovanie_rozpazene_ruky()
    # prednozovanie_ruky_nad_hlavou()

main()