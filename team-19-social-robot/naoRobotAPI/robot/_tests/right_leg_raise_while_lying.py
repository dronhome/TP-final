# -*- encoding: UTF-8 -*- 

'''Cartesian control: Multiple Effector Trajectories'''

import sys
import motion
import almath
from naoqi import ALProxy

motion_proxy = ALProxy("ALMotion", "127.0.0.1", 9559)
posture_proxy = ALProxy("ALRobotPosture", "127.0.0.1", 9559)

names = list()
times = list()
keys = list()

names.append("RWristYaw")
times.append([0.05, 1.45, 2.2, 2.95, 3.7, 4.45, 7.45])
keys.append([[0.107394, [3, -0.0333333, 0], [3, 0.466667, 0]], [0.107394, [3, -0.466667, 0], [3, 0.25, 0]], [0.0989952, [3, -0.25, 0], [3, 0.25, 0]], [0.107394, [3, -0.25, 0], [3, 0.25, 0]], [0.0989952, [3, -0.25, 0], [3, 0.25, 0]], [0.107394, [3, -0.25, 0], [3, 1, 0]], [0.107394, [3, -1, 0], [3, 0, 0]]])

motion_proxy.angleInterpolationBezier(names, times, keys)
