# Choregraphe bezier export in Python.
from naoqi import ALProxy
names = list()
times = list()
keys = list()

names.append("HeadPitch")
times.append([0.36, 1.96])
keys.append([[-0.160616, [3, -0.133333, 0], [3, 0.533333, 0]], [-0.161711, [3, -0.533333, 0], [3, 0, 0]]])

names.append("HeadYaw")
times.append([0.36, 1.96])
keys.append([[0, [3, -0.133333, 0], [3, 0.533333, 0]], [0, [3, -0.533333, 0], [3, 0, 0]]])

names.append("LAnklePitch")
times.append([0.36, 1.96])
keys.append([[0.267287, [3, -0.133333, 0], [3, 0.533333, 0]], [0.269901, [3, -0.533333, 0], [3, 0, 0]]])

names.append("LAnkleRoll")
times.append([0.36, 1.96])
keys.append([[-0.00225767, [3, -0.133333, 0], [3, 0.533333, 0]], [-0.00625882, [3, -0.533333, 0], [3, 0, 0]]])

names.append("LElbowRoll")
times.append([0.36])
keys.append([[-0.66497, [3, -0.133333, 0], [3, 0, 0]]])

names.append("LElbowYaw")
times.append([0.36])
keys.append([[-1.84656, [3, -0.133333, 0], [3, 0, 0]]])

names.append("LHand")
times.append([0.36])
keys.append([[0.302373, [3, -0.133333, 0], [3, 0, 0]]])

names.append("LHipPitch")
times.append([0.36, 1.96])
keys.append([[-1.23553, [3, -0.133333, 0], [3, 0.533333, 0]], [-1.23553, [3, -0.533333, 0], [3, 0, 0]]])

names.append("LHipRoll")
times.append([0.36, 1.96])
keys.append([[0.0294207, [3, -0.133333, 0], [3, 0.533333, 0]], [0.02861, [3, -0.533333, 0], [3, 0, 0]]])

names.append("LHipYawPitch")
times.append([0.36, 1.96])
keys.append([[-0.483303, [3, -0.133333, 0], [3, 0.533333, 0]], [-0.483303, [3, -0.533333, 0], [3, 0, 0]]])

names.append("LKneePitch")
times.append([0.36, 1.96])
keys.append([[1.2126, [3, -0.133333, 0], [3, 0.533333, 0]], [1.21061, [3, -0.533333, 0], [3, 0, 0]]])

names.append("LShoulderPitch")
times.append([0.36])
keys.append([[1.25664, [3, -0.133333, 0], [3, 0, 0]]])

names.append("LShoulderRoll")
times.append([0.36])
keys.append([[0.462512, [3, -0.133333, 0], [3, 0, 0]]])

names.append("LWristYaw")
times.append([0.36])
keys.append([[0.139626, [3, -0.133333, 0], [3, 0, 0]]])

names.append("RAnklePitch")
times.append([0.36, 1.96])
keys.append([[0.267287, [3, -0.133333, 0], [3, 0.533333, 0]], [0.269901, [3, -0.533333, 0], [3, 0, 0]]])

names.append("RAnkleRoll")
times.append([0.36, 1.96])
keys.append([[0.00800858, [3, -0.133333, 0], [3, 0.533333, 0]], [0.00332475, [3, -0.533333, 0], [3, 0, 0]]])

names.append("RElbowRoll")
times.append([0.36])
keys.append([[0.66497, [3, -0.133333, 0], [3, 0, 0]]])

names.append("RElbowYaw")
times.append([0.36])
keys.append([[1.84656, [3, -0.133333, 0], [3, 0, 0]]])

names.append("RHand")
times.append([0.36])
keys.append([[0.293065, [3, -0.133333, 0], [3, 0, 0]]])

names.append("RHipPitch")
times.append([0.36, 1.96])
keys.append([[-1.25053, [3, -0.133333, 0], [3, 0.533333, 0]], [-1.48877, [3, -0.533333, 0], [3, 0, 0]]])

names.append("RHipRoll")
times.append([0.36, 1.96])
keys.append([[0.00748169, [3, -0.133333, 0], [3, 0.533333, 0]], [0.00547642, [3, -0.533333, 0], [3, 0, 0]]])

names.append("RHipYawPitch")
times.append([0.36, 1.96])
keys.append([[-0.483303, [3, -0.133333, 0], [3, 0.533333, 0]], [-0.483303, [3, -0.533333, 0], [3, 0, 0]]])

names.append("RKneePitch")
times.append([0.36, 1.96])
keys.append([[1.20677, [3, -0.133333, 0], [3, 0.533333, 0]], [1.20048, [3, -0.533333, 0], [3, 0, 0]]])

names.append("RShoulderPitch")
times.append([0.36])
keys.append([[1.25664, [3, -0.133333, 0], [3, 0, 0]]])

names.append("RShoulderRoll")
times.append([0.36])
keys.append([[-0.462512, [3, -0.133333, 0], [3, 0, 0]]])

names.append("RWristYaw")
times.append([0.36])
keys.append([[-0.139626, [3, -0.133333, 0], [3, 0, 0]]])