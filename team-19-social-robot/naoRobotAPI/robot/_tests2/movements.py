# -*- encoding: UTF-8 -*- 


from naoqi import ALProxy
import time
em = "anger"
motion = ALProxy("ALMotion", "192.168.86.194", 9559)
posture_proxy = ALProxy("ALRobotPosture", "192.168.86.194", 9559)
speechProxy = ALProxy("ALTextToSpeech", "192.168.86.194", 9559)

if em == "Happy":
    names = ["LAnklePitch", "LAnkleRoll", "LElbowRoll", "LElbowYaw", "LHand", "LHipPitch", "LHipRoll", "LHipYawPitch", "LKneePitch", "LShoulderPitch", "LShoulderRoll", "LWristYaw", "RAnklePitch", "RAnkleRoll", "RElbowRoll", "RElbowYaw", "RHand", "RHipPitch", "RHipRoll", "RHipYawPitch", "RKneePitch", "RShoulderPitch", "RShoulderRoll", "RWristYaw"]
            
    keys1 = [0.0950661, -0.116542, -0.374254, -1.62301, 0.2884, 0.122762, 0.121228, -0.05058, -0.098218, 0.621228, 0.478566, 0.121144, 0.090548, 0.112024, 0.377406, 1.62753, 0.2864, 0.122678, -0.11961, -0.05058, -0.0919981, 0.622846, -0.481718, 0.0720561]
    keys2 = [0.0950661, -0.102736, -0.424876, -1.17662, 0.292, 0.121228, 0.112024, -0.171766, -0.098218, 1.45266, 0.202446, 0.121144, 0.092082, 0.11049, 0.411154, 1.18267, 0.29, 0.122678, -0.116542, -0.171766, -0.102736, 1.44814, -0.200996, 0.05825]

    motion.setAngles(names, keys1, 0.1)
    exit()
    speechProxy.say("Skvele, vidím, že máš dobru náladu ")
    motion.setAngles(names, keys2, 0.1)
    speechProxy.say("Dajme sa teda do toho!")


# ******************************************************************************
if em == "suprise":
    names1 = ["LElbowRoll", "LElbowYaw", "LHand", "LShoulderPitch", "LShoulderRoll", "LWristYaw",
                        "RElbowRoll", "RElbowYaw", "RHand", "RShoulderPitch", "RShoulderRoll", "RWristYaw"]
    angles1 = [-0.391128, -1.18736, 0.2908, -0.5937, 0.256136, 0.11194,
                0.414222, 1.18574, 0.29, 1.47728, -0.234744, 0.05825]
    speed1 = 0.2  # Fraction of max speed

    motion.setAngles(names1, angles1, speed1)
    exit()

    speechProxy.say("Len vydrž, hneď sa dozvieš čo ťa čaka.")
    names2 = ["LElbowRoll", "LElbowYaw", "LHand", "LShoulderPitch", "LShoulderRoll", "LWristYaw",
                        "RElbowRoll", "RElbowYaw", "RHand", "RShoulderPitch", "RShoulderRoll", "RWristYaw"]
    angles2 = [-0.429478, -1.17815, 0.2864, 1.45572, 0.210116, 0.11194,
                0.405018, 1.18267, 0.2868, 1.45121, -0.2102, 0.0597839]
    speed2 = 0.2  # Fraction of max speed

    motion.setAngles(names2, angles2, speed2)

    speechProxy.say("O malú chvíľu sa do spoločného cvičenia pustíme! ")
# # ******************************************************************************

if em == "anger":

    names_head_arms = [
                "HeadPitch", "HeadYaw",
                "LElbowRoll", "LElbowYaw", "LHand",
                "LShoulderPitch", "LShoulderRoll", "LWristYaw",
                "RElbowRoll", "RElbowYaw", "RHand",
                "RShoulderPitch", "RShoulderRoll", "RWristYaw"
            ]

    angles_head_arms = [
        -0.168614, 0,
        -1.51841, -0.496355, 0.294948,
        1.80576, 0.772792, 0.106233,
        1.51841, 0.496355, 0.294948,
        1.80576, -0.772792, 0.0935145
    ]

    speed_head_arms = 0.2  # Fraction of max speed (adjustable)

    motion.setAngles(names_head_arms, angles_head_arms, speed_head_arms)
    exit()

    speechProxy.say("Zdá sa, že ťa dnes niečo rozladilo. Než začneme cvičiť, urobíme si dychové cvičenie. Nadýchni sa cez nos na 4 doby a pomaly vydýchni cez ústa na 6 dôb. Sústreď sa na svoj dych. Zopakuj 6-krát.")

    names_head_arms = [
        "HeadPitch", "HeadYaw",
        "LElbowRoll", "LElbowYaw", "LHand",
        "LShoulderPitch", "LShoulderRoll", "LWristYaw",
        "RElbowRoll", "RElbowYaw", "RHand",
        "RShoulderPitch", "RShoulderRoll", "RWristYaw"
    ]

    angles_head_arms = [
        -0.166224, 0,
        -0.406468, -1.18736, 0.2908,
        1.45419, 0.228524, 0.11194,
        0.421892, 1.19341, 0.29,
        1.46194, -0.231676, 0.05825
    ]

    speed_head_arms = 0.2  # Fraction of max speed (adjustable)

    motion.setAngles(names_head_arms, angles_head_arms, speed_head_arms)
    time.sleep(0.5)


speechProxy.say("Jeden")
time.sleep(0.4)
speechProxy.say("Dva")
time.sleep(0.4)
speechProxy.say("Tri")