from naoqi import ALProxy
import right_leg_exercise

# Replace this with your NAO robot's IP address
NAO_IP = "127.0.0.1"
# NAO_IP = "172.20.10.7"
NAO_PORT = 9559

motionProxy = ALProxy("ALMotion", NAO_IP, NAO_PORT)
postureProxy = ALProxy("ALRobotPosture", NAO_IP, NAO_PORT)

def go_back_to_stable_position_for_lifting_right_leg_in_standing():
    from naoqi import ALProxy
    names = list()
    times = list()
    keys = list()

    stabilize_time = 2.0

    names.append("HeadPitch")
    times.append([stabilize_time])
    keys.append([[0.00196421, [3, -0.306667, 0], [3, 0, 0]]])

    names.append("HeadYaw")
    times.append([stabilize_time])
    keys.append([[-0.00362528, [3, -0.306667, 0], [3, 0, 0]]])

    names.append("LAnklePitch")
    times.append([stabilize_time])
    keys.append([[-0.350534, [3, -0.306667, 0], [3, 0, 0]]])

    names.append("LAnkleRoll")
    times.append([stabilize_time])
    keys.append([[0.330616, [3, -0.306667, 0], [3, 0, 0]]])

    names.append("LElbowRoll")
    times.append([stabilize_time])
    keys.append([[-1.00483, [3, -0.306667, 0], [3, 0, 0]]])

    names.append("LElbowYaw")
    times.append([stabilize_time])
    keys.append([[-1.38659, [3, -0.306667, 0], [3, 0, 0]]])

    names.append("LHand")
    times.append([stabilize_time])
    keys.append([[0.254252, [3, -0.306667, 0], [3, 0, 0]]])

    names.append("LHipPitch")
    times.append([stabilize_time])
    keys.append([[-0.453016, [3, -0.306667, 0], [3, 0, 0]]])

    names.append("LHipRoll")
    times.append([stabilize_time])
    keys.append([[-0.330616, [3, -0.306667, 0], [3, 0, 0]]])

    names.append("LHipYawPitch")
    times.append([stabilize_time])
    keys.append([[-0.00257, [3, -0.306667, 0], [3, 0, 0]]])

    names.append("LKneePitch")
    times.append([stabilize_time])
    keys.append([[0.707806, [3, -0.306667, 0], [3, 0, 0]]])

    names.append("LShoulderPitch")
    times.append([stabilize_time])
    keys.append([[1.40689, [3, -0.306667, 0], [3, 0, 0]]])

    names.append("LShoulderRoll")
    times.append([stabilize_time])
    keys.append([[0.300092, [3, -0.306667, 0], [3, 0, 0]]])

    names.append("LWristYaw")
    times.append([stabilize_time])
    keys.append([[-0.00498221, [3, -0.306667, 0], [3, 0, 0]]])

    names.append("RAnklePitch")
    times.append([stabilize_time])
    keys.append([[-0.351562, [3, -0.306667, 0], [3, 0, 0]]])

    names.append("RAnkleRoll")
    times.append([stabilize_time])
    keys.append([[0.330616, [3, -0.306667, 0], [3, 0, 0]]])

    names.append("RElbowRoll")
    times.append([stabilize_time])
    keys.append([[1.00634, [3, -0.306667, 0], [3, 0, 0]]])

    names.append("RElbowYaw")
    times.append([stabilize_time])
    keys.append([[1.39279, [3, -0.306667, 0], [3, 0, 0]]])

    names.append("RHand")
    times.append([stabilize_time])
    keys.append([[0.253553, [3, -0.306667, 0], [3, 0, 0]]])

    names.append("RHipPitch")
    times.append([stabilize_time])
    keys.append([[-0.455269, [3, -0.306667, 0], [3, 0, 0]]])

    names.append("RHipRoll")
    times.append([stabilize_time])
    keys.append([[-0.330616, [3, -0.306667, 0], [3, 0, 0]]])

    names.append("RHipYawPitch")
    times.append([stabilize_time])
    keys.append([[-0.00257, [3, -0.306667, 0], [3, 0, 0]]])

    names.append("RKneePitch")
    times.append([stabilize_time])
    keys.append([[0.703364, [3, -0.306667, 0], [3, 0, 0]]])

    names.append("RShoulderPitch")
    times.append([stabilize_time])
    keys.append([[1.39967, [3, -0.306667, 0], [3, 0, 0]]])

    names.append("RShoulderRoll")
    times.append([stabilize_time])
    keys.append([[-0.306888, [3, -0.306667, 0], [3, 0, 0]]])

    names.append("RWristYaw")
    times.append([stabilize_time])
    keys.append([[0.00395609, [3, -0.306667, 0], [3, 0, 0]]])

    motionProxy.angleInterpolationBezier(names, times, keys)


# Wake up the robot
motionProxy.wakeUp()

names = list()
times = list()
keys = list()

# set center of gravity to one leg
motionProxy.angleInterpolation(right_leg_exercise.names, right_leg_exercise.keys, right_leg_exercise.times, True)

# motionProxy.setAngles(["RKneePitch"], 1.745329252, 0.06)  # 100 deg
# motionProxy.setAngles(["RAnklePitch"], -0.872664626,0.06)  # -50 deg
# motionProxy.setAngles(["RHipPitch"],  -1.0471975512, 0.06)  # -60 deg
# # lift opposite arm for stability
# motionProxy.setAngles(["LShoulderRoll"], 1.3264502315, 0.075)
# motionProxy.setAngles(["LElbowRoll"], 1.3264502315, 0.075)

# motionProxy.angleInterpolationBezier(names, times, keys)

jointNames = ["RKneePitch", "RAnklePitch", "RHipPitch", "LShoulderRoll", "LElbowRoll"]
targetAngles = [
    [1.4],  # RKneePitch, adjusted to approximately 57.3 degrees
    [-0.65],  # RAnklePitch, adjusted to approximately -34.38 degrees
    [-0.8],  # RHipPitch, adjusted to approximately -40.15 degrees
    
    [1.3264502315],  # LShoulderRoll, adjusted to approximately 57.3 degrees
    [1.3264502315]   # LElbowRoll, adjusted to approximately 57.3 degrees
]
# targetAngles = [
#     [0.5],  # RKneePitch, reduced to approximately 28.65 degrees
#     [-0.4],  # RAnklePitch, reduced to approximately -22.92 degrees
#     [-0.5],  # RHipPitch, reduced to approximately -28.65 degrees
#     [0.75],  # LShoulderRoll, reduced to approximately 42.97 degrees
#     [0.75]   # LElbowRoll, reduced to approximately 42.97 degrees
# ]

times = [[3], [3], [3], [3], [3]]

motionProxy.angleInterpolation(jointNames, targetAngles, times, False)

go_back_to_stable_position_for_lifting_right_leg_in_standing()

postureProxy.goToPosture("StandInit", 0.5)