names = list()
times = list()
keys = list()

names.append("HeadPitch")
times.append([0, 4])
keys.append([-0.0351029, -0.0351029])

names.append("HeadYaw")
times.append([0, 4])
keys.append([0.0224334, 0.0224334])

names.append("LAnklePitch")
times.append([0, 4])
keys.append([0.00114572, 0.00114572])

names.append("LAnkleRoll")
times.append([0, 4])
keys.append([-0.0925132, -0.0925133])

names.append("LElbowRoll")
times.append([0, 4])
keys.append([-0.988633, -0.988633])

names.append("LElbowYaw")
times.append([0, 4])
keys.append([-1.52658, -1.52658])

names.append("LHand")
times.append([0, 4])
keys.append([0.6988, 0.6988])

names.append("LHipPitch")
times.append([0, 4])
keys.append([0.308083, 0.308084])

names.append("LHipRoll")
times.append([0, 4])
keys.append([0.0797669, 0.079767])

names.append("LHipYawPitch")
times.append([0, 4])
keys.append([-0.153456, -0.153456])

names.append("LKneePitch")
times.append([0, 4])
keys.append([-0.0839433, -0.0839434])

names.append("LShoulderPitch")
times.append([0, 4])
keys.append([1.46624, 1.46624])

names.append("LShoulderRoll")
times.append([0, 4])
keys.append([0.109958, 0.109958])

names.append("LWristYaw")
times.append([0, 4])
keys.append([-0.725513, -0.725512])

names.append("RAnklePitch")
times.append([0, 4])
keys.append([0.0216098, 0.0216098])

names.append("RAnkleRoll")
times.append([0, 4])
keys.append([0.14867, 0.14867])

names.append("RElbowRoll")
times.append([0, 1.93333, 4])
keys.append([1.1081, 0.34383, 1.1081])

names.append("RElbowYaw")
times.append([0, 1.93333, 4])
keys.append([1.47652, 0, 1.47652])

names.append("RHand")
times.append([0, 1.93333, 4])
keys.append([0.564323, 0.69, 0.564323])

names.append("RHipPitch")
times.append([0, 4])
keys.append([0.301379, 0.30138])

names.append("RHipRoll")
times.append([0, 4])
keys.append([-0.155334, -0.155334])

names.append("RHipYawPitch")
times.append([0, 4])
keys.append([-0.153456, -0.153456])

names.append("RKneePitch")
times.append([0, 4])
keys.append([-0.0823275, -0.0823275])

names.append("RShoulderPitch")
times.append([0, 1.93333, 4])
keys.append([1.50757, -0.457276, 1.50757])

names.append("RShoulderRoll")
times.append([0, 1.93333, 4])
keys.append([-0.133735, 0.0191986, -0.133735])

names.append("RWristYaw")
times.append([0, 1.93333, 4])
keys.append([0.883993, 0.162316, 0.883992])

# try:
#   # uncomment the following line and modify the IP if you use this script outside Choregraphe.
#   # motion = ALProxy("ALMotion", IP, 9559)
#   motion = ALProxy("ALMotion")
#   motion.angleInterpolation(names, keys, times, True)
# except Exception:
#   print ("chyba")
#   pass
