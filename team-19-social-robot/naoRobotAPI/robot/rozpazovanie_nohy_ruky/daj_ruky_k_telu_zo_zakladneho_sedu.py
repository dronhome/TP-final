# Choregraphe bezier export in Python.
from naoqi import ALProxy
names = list()
times = list()
keys = list()

names.append("HeadPitch")
times.append([0.24, 1.68])
keys.append([[-0.17, [3, -0.0933333, 0], [3, 0.48, 0]], [-0.160616, [3, -0.48, 0], [3, 0, 0]]])

names.append("HeadYaw")
times.append([0.24, 1.68])
keys.append([[0, [3, -0.0933333, 0], [3, 0.48, 0]], [0, [3, -0.48, 0], [3, 0, 0]]])

names.append("LAnklePitch")
times.append([0.24, 1.68])
keys.append([[0.268913, [3, -0.0933333, 0], [3, 0.48, 0]], [0.267287, [3, -0.48, 0], [3, 0, 0]]])

names.append("LAnkleRoll")
times.append([0.24, 1.68])
keys.append([[-0.00213803, [3, -0.0933333, 0], [3, 0.48, 0]], [-0.00225767, [3, -0.48, 0], [3, 0, 0]]])

names.append("LElbowRoll")
times.append([0.24, 1.68])
keys.append([[-1.36043, [3, -0.0933333, 0], [3, 0.48, 0]], [-0.66497, [3, -0.48, 0], [3, 0, 0]]])

names.append("LElbowYaw")
times.append([0.24, 1.68])
keys.append([[-1.39397, [3, -0.0933333, 0], [3, 0.48, 0]], [-1.84656, [3, -0.48, 0], [3, 0, 0]]])

names.append("LHand")
times.append([0.24, 1.68])
keys.append([[0.3, [3, -0.0933333, 0], [3, 0.48, 0]], [0.302373, [3, -0.48, 0], [3, 0, 0]]])

names.append("LHipPitch")
times.append([0.24, 1.68])
keys.append([[-1.23046, [3, -0.0933333, 0], [3, 0.48, 0]], [-1.23553, [3, -0.48, 0], [3, 0, 0]]])

names.append("LHipRoll")
times.append([0.24, 1.68])
keys.append([[0.0306377, [3, -0.0933333, 0], [3, 0.48, 0]], [0.0294207, [3, -0.48, 0], [3, 0, 0]]])

names.append("LHipYawPitch")
times.append([0.24, 1.68])
keys.append([[-0.476438, [3, -0.0933333, 0], [3, 0.48, 0]], [-0.483303, [3, -0.48, 0], [3, 0, 0]]])

names.append("LKneePitch")
times.append([0.24, 1.68])
keys.append([[1.2156, [3, -0.0933333, 0], [3, 0.48, 0]], [1.2126, [3, -0.48, 0], [3, 0, 0]]])

names.append("LShoulderPitch")
times.append([0.24, 1.68])
keys.append([[0.45115, [3, -0.0933333, 0], [3, 0.48, 0]], [1.25664, [3, -0.48, 0], [3, 0, 0]]])

names.append("LShoulderRoll")
times.append([0.24, 1.68])
keys.append([[0.295332, [3, -0.0933333, 0], [3, 0.48, 0]], [0.462512, [3, -0.48, 0], [3, 0, 0]]])

names.append("LWristYaw")
times.append([0.24, 1.68])
keys.append([[0.144133, [3, -0.0933333, 0], [3, 0.48, 0]], [0.148732, [3, -0.48, 0], [3, 0, 0]]])

names.append("RAnklePitch")
times.append([0.24, 1.68])
keys.append([[0.268913, [3, -0.0933333, 0], [3, 0.48, 0]], [0.267287, [3, -0.48, 0], [3, 0, 0]]])

names.append("RAnkleRoll")
times.append([0.24, 1.68])
keys.append([[0.0021596, [3, -0.0933333, 0], [3, 0.48, 0]], [0.00800858, [3, -0.48, 0], [3, 0, 0]]])

names.append("RElbowRoll")
times.append([0.24, 1.68])
keys.append([[1.36043, [3, -0.0933333, 0], [3, 0.48, 0]], [0.66497, [3, -0.48, 0], [3, 0, 0]]])

names.append("RElbowYaw")
times.append([0.24, 1.68])
keys.append([[1.39398, [3, -0.0933333, 0], [3, 0.48, 0]], [1.84656, [3, -0.48, 0], [3, 0, 0]]])

names.append("RHand")
times.append([0.24, 1.68])
keys.append([[0.3, [3, -0.0933333, 0], [3, 0.48, 0]], [0.293065, [3, -0.48, 0], [3, 0, 0]]])

names.append("RHipPitch")
times.append([0.24, 1.68])
keys.append([[-1.24461, [3, -0.0933333, 0], [3, 0.48, 0]], [-1.25053, [3, -0.48, 0], [3, 0, 0]]])

names.append("RHipRoll")
times.append([0.24, 1.68])
keys.append([[0.00453492, [3, -0.0933333, 0], [3, 0.48, 0]], [0.00748169, [3, -0.48, 0], [3, 0, 0]]])

names.append("RHipYawPitch")
times.append([0.24, 1.68])
keys.append([[-0.476438, [3, -0.0933333, 0], [3, 0.48, 0]], [-0.483303, [3, -0.48, 0], [3, 0, 0]]])

names.append("RKneePitch")
times.append([0.24, 1.68])
keys.append([[1.20262, [3, -0.0933333, 0], [3, 0.48, 0]], [1.20677, [3, -0.48, 0], [3, 0, 0]]])

names.append("RShoulderPitch")
times.append([0.24, 1.68])
keys.append([[0.451164, [3, -0.0933333, 0], [3, 0.48, 0]], [1.25664, [3, -0.48, 0], [3, 0, 0]]])

names.append("RShoulderRoll")
times.append([0.24, 1.68])
keys.append([[-0.299704, [3, -0.0933333, 0], [3, 0.48, 0]], [-0.462512, [3, -0.48, 0], [3, 0, 0]]])

names.append("RWristYaw")
times.append([0.24, 1.68])
keys.append([[-0.133726, [3, -0.0933333, 0], [3, 0.48, 0]], [-0.149648, [3, -0.48, 0], [3, 0, 0]]])