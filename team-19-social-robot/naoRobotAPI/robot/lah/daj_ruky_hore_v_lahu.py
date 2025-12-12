# Choregraphe bezier export in Python.
from naoqi import ALProxy
names = list()
times = list()
keys = list()

names.append("HeadPitch")
times.append([0.24, 2.28])
keys.append([[0.153358, [3, -0.0933333, 0], [3, 0.68, 0]], [0.153358, [3, -0.68, 0], [3, 0, 0]]])

names.append("HeadYaw")
times.append([0.24, 2.28])
keys.append([[-0.00106465, [3, -0.0933333, 0], [3, 0.68, 0]], [-0.00106465, [3, -0.68, 0], [3, 0, 0]]])

names.append("LAnklePitch")
times.append([0.24, 2.28])
keys.append([[0.867001, [3, -0.0933333, 0], [3, 0.68, 0]], [0.867001, [3, -0.68, 0], [3, 0, 0]]])

names.append("LAnkleRoll")
times.append([0.24, 2.28])
keys.append([[-0.0307136, [3, -0.0933333, 0], [3, 0.68, 0]], [-0.0307136, [3, -0.68, 0], [3, 0, 0]]])

names.append("LElbowRoll")
times.append([0.24, 2.28])
keys.append([[-0.610329, [3, -0.0933333, 0], [3, 0.68, 0]], [-0.610329, [3, -0.68, 0], [3, 0, 0]]])

names.append("LElbowYaw")
times.append([0.24, 2.28])
keys.append([[-1.26285, [3, -0.0933333, 0], [3, 0.68, 0]], [-1.26285, [3, -0.68, 0], [3, 0, 0]]])

names.append("LHand")
times.append([0.24, 2.28])
keys.append([[0.294819, [3, -0.0933333, 0], [3, 0.68, 0]], [0.294819, [3, -0.68, 0], [3, 0, 0]]])

names.append("LHipPitch")
times.append([0.24, 2.28])
keys.append([[0.366263, [3, -0.0933333, 0], [3, 0.68, 0]], [0.366263, [3, -0.68, 0], [3, 0, 0]]])

names.append("LHipRoll")
times.append([0.24, 2.28])
keys.append([[0.106934, [3, -0.0933333, 0], [3, 0.68, 0]], [0.106934, [3, -0.68, 0], [3, 0, 0]]])

names.append("LHipYawPitch")
times.append([0.24, 2.28])
keys.append([[-0.51131, [3, -0.0933333, 0], [3, 0.68, 0]], [-0.51131, [3, -0.68, 0], [3, 0, 0]]])

names.append("LKneePitch")
times.append([0.24, 2.28])
keys.append([[-0.0836285, [3, -0.0933333, 0], [3, 0.68, 0]], [-0.0836285, [3, -0.68, 0], [3, 0, 0]]])

names.append("LShoulderPitch")
times.append([0.24, 2.28])
keys.append([[1.93004, [3, -0.0933333, 0], [3, 0.68, 0]], [-1.309, [3, -0.68, 0], [3, 0, 0]]])

names.append("LShoulderRoll")
times.append([0.24, 2.28])
keys.append([[0.470864, [3, -0.0933333, 0], [3, 0.68, 0]], [0.256563, [3, -0.68, 0], [3, 0, 0]]])

names.append("LWristYaw")
times.append([0.24, 2.28])
keys.append([[0.383972, [3, -0.0933333, 0], [3, 0.68, 0]], [0.383972, [3, -0.68, 0], [3, 0, 0]]])

names.append("RAnklePitch")
times.append([0.24, 2.28])
keys.append([[0.645601, [3, -0.0933333, 0], [3, 0.68, 0]], [0.645601, [3, -0.68, 0], [3, 0, 0]]])

names.append("RAnkleRoll")
times.append([0.24, 2.28])
keys.append([[-0.281553, [3, -0.0933333, 0], [3, 0.68, 0]], [-0.281553, [3, -0.68, 0], [3, 0, 0]]])

names.append("RElbowRoll")
times.append([0.24, 2.28])
keys.append([[0.599498, [3, -0.0933333, 0], [3, 0.68, 0]], [0.599498, [3, -0.68, 0], [3, 0, 0]]])

names.append("RElbowYaw")
times.append([0.24, 2.28])
keys.append([[1.26337, [3, -0.0933333, 0], [3, 0.68, 0]], [1.26337, [3, -0.68, 0], [3, 0, 0]]])

names.append("RHand")
times.append([0.24, 2.28])
keys.append([[0.360319, [3, -0.0933333, 0], [3, 0.68, 0]], [0.360319, [3, -0.68, 0], [3, 0, 0]]])

names.append("RHipPitch")
times.append([0.24, 2.28])
keys.append([[0.159366, [3, -0.0933333, 0], [3, 0.68, 0]], [0.159366, [3, -0.68, 0], [3, 0, 0]]])

names.append("RHipRoll")
times.append([0.24, 2.28])
keys.append([[-0.129973, [3, -0.0933333, 0], [3, 0.68, 0]], [-0.129973, [3, -0.68, 0], [3, 0, 0]]])

names.append("RHipYawPitch")
times.append([0.24, 2.28])
keys.append([[-0.51131, [3, -0.0933333, 0], [3, 0.68, 0]], [-0.51131, [3, -0.68, 0], [3, 0, 0]]])

names.append("RKneePitch")
times.append([0.24, 2.28])
keys.append([[0.274081, [3, -0.0933333, 0], [3, 0.68, 0]], [0.274081, [3, -0.68, 0], [3, 0, 0]]])

names.append("RShoulderPitch")
times.append([0.24, 2.28])
keys.append([[1.94138, [3, -0.0933333, 0], [3, 0.68, 0]], [-1.309, [3, -0.68, 0], [3, 0, 0]]])

names.append("RShoulderRoll")
times.append([0.24, 2.28])
keys.append([[-0.482844, [3, -0.0933333, 0], [3, 0.68, 0]], [-0.256563, [3, -0.68, 0], [3, 0, 0]]])

names.append("RWristYaw")
times.append([0.24, 2.28])
keys.append([[-0.384116, [3, -0.0933333, 0], [3, 0.68, 0]], [-0.384116, [3, -0.68, 0], [3, 0, 0]]])
