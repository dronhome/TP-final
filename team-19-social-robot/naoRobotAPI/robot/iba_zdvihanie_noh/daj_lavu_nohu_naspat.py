# Choregraphe bezier export in Python.
from naoqi import ALProxy
names = list()
times = list()
keys = list()

names.append("HeadPitch")
times.append([0.36, 1.40])
keys.append([[-0.169649, [3, -0.133333, 0], [3, 0.573333, 0]], [-0.160616, [3, -0.573333, 0], [3, 0, 0]]])

names.append("HeadYaw")
times.append([0.36, 1.40])
keys.append([[0, [3, -0.133333, 0], [3, 0.573333, 0]], [0, [3, -0.573333, 0], [3, 0, 0]]])

names.append("LAnklePitch")
times.append([0.36, 1.40])
keys.append([[0.268069, [3, -0.133333, 0], [3, 0.573333, 0]], [0.267287, [3, -0.573333, 0], [3, 0, 0]]])

names.append("LAnkleRoll")
times.append([0.36, 1.40])
keys.append([[-0.0069162, [3, -0.133333, 0], [3, 0.573333, 0]], [-0.00225767, [3, -0.573333, 0], [3, 0, 0]]])

names.append("LElbowRoll")
times.append([2.08])
keys.append([[-0.662977, [3, -0.706667, 0], [3, 0, 0]]])

names.append("LElbowYaw")
times.append([2.08])
keys.append([[-1.85089, [3, -0.706667, 0], [3, 0, 0]]])

names.append("LHand")
times.append([2.08])
keys.append([[0.3, [3, -0.706667, 0], [3, 0, 0]]])

names.append("LHipPitch")
times.append([0.36, 1.40])
keys.append([[-1.31, [3, -0.133333, 0], [3, 0.573333, 0]], [-1.23553, [3, -0.573333, 0], [3, 0, 0]]])

names.append("LHipRoll")
times.append([0.36, 1.40])
keys.append([[0.0294207, [3, -0.133333, 0], [3, 0.573333, 0]], [0.0294207, [3, -0.573333, 0], [3, 0, 0]]])

names.append("LHipYawPitch")
times.append([0.36, 1.40])
keys.append([[-0.495288, [3, -0.133333, 0], [3, 0.573333, 0]], [-0.483303, [3, -0.573333, 0], [3, 0, 0]]])

names.append("LKneePitch")
times.append([0.36, 1.40])
keys.append([[1.2126, [3, -0.133333, 0], [3, 0.573333, 0]], [1.2126, [3, -0.573333, 0], [3, 0, 0]]])

names.append("LShoulderPitch")
times.append([2.08])
keys.append([[1.2525, [3, -0.706667, 0], [3, 0, 0]]])

names.append("LShoulderRoll")
times.append([2.08])
keys.append([[0.4622, [3, -0.706667, 0], [3, 0, 0]]])

names.append("LWristYaw")
times.append([2.08])
keys.append([[0.147051, [3, -0.706667, 0], [3, 0, 0]]])

names.append("RAnklePitch")
times.append([0.36, 1.40])
keys.append([[0.268095, [3, -0.133333, 0], [3, 0.573333, 0]], [0.267287, [3, -0.573333, 0], [3, 0, 0]]])

names.append("RAnkleRoll")
times.append([0.36, 1.40])
keys.append([[0.0124357, [3, -0.133333, 0], [3, 0.573333, 0]], [0.00800858, [3, -0.573333, 0], [3, 0, 0]]])

names.append("RElbowRoll")
times.append([2.08])
keys.append([[0.662978, [3, -0.706667, 0], [3, 0, 0]]])

names.append("RElbowYaw")
times.append([2.08])
keys.append([[1.84227, [3, -0.706667, 0], [3, 0, 0]]])

names.append("RHand")
times.append([2.08])
keys.append([[0.3, [3, -0.706667, 0], [3, 0, 0]]])

names.append("RHipPitch")
times.append([0.36, 1.40])
keys.append([[-1.19802, [3, -0.133333, 0], [3, 0.573333, 0]], [-1.25053, [3, -0.573333, 0], [3, 0, 0]]])

names.append("RHipRoll")
times.append([0.36, 1.40])
keys.append([[0.00192084, [3, -0.133333, 0], [3, 0.573333, 0]], [0.00748169, [3, -0.573333, 0], [3, 0, 0]]])

names.append("RHipYawPitch")
times.append([0.36, 1.40])
keys.append([[-0.495288, [3, -0.133333, 0], [3, 0.573333, 0]], [-0.483303, [3, -0.573333, 0], [3, 0, 0]]])

names.append("RKneePitch")
times.append([0.36, 1.40])
keys.append([[1.27458, [3, -0.133333, 0], [3, 0.573333, 0]], [1.20677, [3, -0.573333, 0], [3, 0, 0]]])

names.append("RShoulderPitch")
times.append([2.08])
keys.append([[1.25363, [3, -0.706667, 0], [3, 0, 0]]])

names.append("RShoulderRoll")
times.append([2.08])
keys.append([[-0.462217, [3, -0.706667, 0], [3, 0, 0]]])

names.append("RWristYaw")
times.append([2.08])
keys.append([[-0.147051, [3, -0.706667, 0], [3, 0, 0]]])