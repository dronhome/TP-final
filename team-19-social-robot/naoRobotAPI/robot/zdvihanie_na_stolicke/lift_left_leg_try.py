from naoqi import ALProxy
import left_leg_exercise

# Replace this with your NAO robot's IP address
NAO_IP = "127.0.0.1"
# NAO_IP = "172.20.10.7"
NAO_PORT = 9559

motionProxy = ALProxy("ALMotion", NAO_IP, NAO_PORT)
postureProxy = ALProxy("ALRobotPosture", NAO_IP, NAO_PORT)


def go_back_to_stable_position_for_lifting_left_leg_in_standing():
    names = list()
    times = list()
    keys = list()

    stabilize_time = 2.0

    names.append("HeadPitch")
    times.append([stabilize_time])
    keys.append([[-0.160616, [3, -0.333333, 0], [3, 0, 0]]])

    names.append("HeadYaw")
    times.append([stabilize_time])
    keys.append([[0, [3, -0.333333, 0], [3, 0, 0]]])

    names.append("LAnklePitch")
    times.append([stabilize_time])
    keys.append([[0.0866826, [3, -0.333333, 0], [3, 0, 0]]])

    names.append("LAnkleRoll")
    times.append([stabilize_time])
    keys.append([[-0.322769, [3, -0.333333, 0], [3, 0, 0]]])

    names.append("LElbowRoll")
    times.append([stabilize_time])
    keys.append([[-0.423197, [3, -0.333333, 0], [3, 0, 0]]])

    names.append("LElbowYaw")
    times.append([stabilize_time])
    keys.append([[-1.20175, [3, -0.333333, 0], [3, 0, 0]]])

    names.append("LHand")
    times.append([stabilize_time])
    keys.append([[0.295804, [3, -0.333333, 0], [3, 0, 0]]])

    names.append("LHipPitch")
    times.append([stabilize_time])
    keys.append([[0.123171, [3, -0.333333, 0], [3, 0, 0]]])

    names.append("LHipRoll")
    times.append([stabilize_time])
    keys.append([[0.323102, [3, -0.333333, 0], [3, 0, 0]]])

    names.append("LHipYawPitch")
    times.append([stabilize_time])
    keys.append([[-0.171128, [3, -0.333333, 0], [3, 0, 0]]])

    names.append("LKneePitch")
    times.append([stabilize_time])
    keys.append([[-0.0872552, [3, -0.333333, 0], [3, 0, 0]]])

    names.append("LShoulderPitch")
    times.append([stabilize_time])
    keys.append([[1.43965, [3, -0.333333, 0], [3, 0, 0]]])

    names.append("LShoulderRoll")
    times.append([stabilize_time])
    keys.append([[0.217452, [3, -0.333333, 0], [3, 0, 0]]])

    names.append("LWristYaw")
    times.append([stabilize_time])
    keys.append([[0.109774, [3, -0.333333, 0], [3, 0, 0]]])

    names.append("RAnklePitch")
    times.append([stabilize_time])
    keys.append([[0.0866825, [3, -0.333333, 0], [3, 0, 0]]])

    names.append("RAnkleRoll")
    times.append([stabilize_time])
    keys.append([[-0.330855, [3, -0.333333, 0], [3, 0, 0]]])

    names.append("RElbowRoll")
    times.append([stabilize_time])
    keys.append([[0.42319, [3, -0.333333, 0], [3, 0, 0]]])

    names.append("RElbowYaw")
    times.append([stabilize_time])
    keys.append([[1.20175, [3, -0.333333, 0], [3, 0, 0]]])

    names.append("RHand")
    times.append([stabilize_time])
    keys.append([[0.295804, [3, -0.333333, 0], [3, 0, 0]]])

    names.append("RHipPitch")
    times.append([stabilize_time])
    keys.append([[0.123172, [3, -0.333333, 0], [3, 0, 0]]])

    names.append("RHipRoll")
    times.append([stabilize_time])
    keys.append([[0.33084, [3, -0.333333, 0], [3, 0, 0]]])

    names.append("RHipYawPitch")
    times.append([stabilize_time])
    keys.append([[-0.171128, [3, -0.333333, 0], [3, 0, 0]]])

    names.append("RKneePitch")
    times.append([stabilize_time])
    keys.append([[-0.0872552, [3, -0.333333, 0], [3, 0, 0]]])

    names.append("RShoulderPitch")
    times.append([stabilize_time])
    keys.append([[1.45207, [3, -0.333333, 0], [3, 0, 0]]])

    names.append("RShoulderRoll")
    times.append([stabilize_time])
    keys.append([[-0.22412, [3, -0.333333, 0], [3, 0, 0]]])

    names.append("RWristYaw")
    times.append([stabilize_time])
    keys.append([[0.0989953, [3, -0.333333, 0], [3, 0, 0]]])

    motionProxy.angleInterpolationBezier(names, times, keys)


# motionProxy.wakeUp()
# postureProxy.goToPosture("StandInit", 0.5)
speechProxy = ALProxy("ALTextToSpeech", NAO_IP, NAO_PORT)
speechProxy.say(str("Nezabudnite plynule dychatNezabudnite plynule dychatNezabudnite plynule dychatNezabudnite plynule dychatNezabudnite plynule dychatNezabudnite plynule dychat.Nezabudnite plynule dychatNezabudnite plynule dychatNezabudnite plynule dychatNezabudnite plynule dychatNezabudnite plynule dychatNezabudnite plynule dychat.Nezabudnite plynule dychatNezabudnite plynule dychatNezabudnite plynule dychatNezabudnite plynule dychatNezabudnite plynule dychatNezabudnite plynule dychat.Nezabudnite plynule dychatNezabudnite plynule dychatNezabudnite plynule dychatNezabudnite plynule dychatNezabudnite plynule dychatNezabudnite plynule dychat."))

names = list()
times = list()
keys = list()

# motionProxy.angleInterpolation(left_leg_exercise.names, left_leg_exercise.keys, left_leg_exercise.times, True)

# jointNames = ["LKneePitch", "LAnklePitch", "LHipPitch", "RShoulderRoll", "RElbowRoll"]
# targetAngles = [
#     [1.4],  # LKneePitch, adjusted to approximately 57.3 degrees
#     [-0.65],  # LAnklePitch, adjusted to approximately -34.38 degrees
#     [-0.8],  # LHipPitch, adjusted to approximately -40.15 degrees
    
#     [-1.3264502315],  # RShoulderRoll, adjusted to approximately -57.3 degrees (negated for symmetry)
#     [-1.3264502315]   # RElbowRoll, adjusted to approximately -57.3 degrees (negated for symmetry)
# ]
# times = [[3], [3], [3], [3], [3]]
# motionProxy.angleInterpolationBezier(jointNames, times, targetAngles)

# go_back_to_stable_position_for_lifting_left_leg_in_standing()

# postureProxy.goToPosture("StandInit", 0.5)