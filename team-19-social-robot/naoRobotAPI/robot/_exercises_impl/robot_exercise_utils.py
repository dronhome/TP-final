# -*- coding: utf-8 -*-

import json
import sys
import os
import naoqi
from naoqi import ALProxy, qi
import almath
import time
import random
import codecs
from gtts import gTTS

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

class NaoqiConnection(object):

    app = None
   

    def __init__(self, config):
        # future = qi.Future()

        self.er = config['enable_emotions']
        self.limit = int(config["exercise_duration"])
        self.is_physical = config['is_physical']
        self.gender = config['target_gender']
    
        if self.is_physical:
            self.ip_nao = config['physical_robot_ip']

        else:
            self.ip_nao = config['virtual_robot_ip']
        try:
            self.port_nao = 9559
            self.app = qi.Session()
            self.app.connect("tcp://{}:{}".format(self.ip_nao, self.port_nao))
            
            self.speechProxy = self.app.service("ALTextToSpeech")
            self.postureProxy = self.app.service("ALRobotPosture")
            self.motionProxy = self.app.service("ALMotion")
            self.trackerService = self.app.service("ALTracker")

            self.soundDetection = self.app.service("ALSoundDetection")
            self.memory = self.app.service("ALMemory")

            # if self.is_physical:
            #     self.motionProxy.setFallManagerEnabled(False)
            
        except:
            return None


        # Add target face to track.
        self.targetName = "Face"
        faceWidth = 0.1
        self.trackerService.registerTarget(self.targetName, faceWidth)
        self.trackerService.track(self.targetName)
    
    def init_walking_around_chair(self):
        self.camera = self.app.service("ALVideoDevice")

    def speak_or_message(self, sentence):
        print("Speech:", self.is_physical, sentence)
        
        if self.is_physical:
            self.speechProxy.say(sentence)
        else:
            if sentence != '':
                if isinstance(sentence, str):
                    sentence = sentence.decode('utf-8')
                tts = gTTS(text=u"{0}".format(sentence), lang='cs', slow=False)
                tts.save("output.mp3")
                os.system("mpg123 output.mp3 > /dev/null 2>&1")


class RobotExerciseUtils(object):

    starting_sentence = '' # Sentence to say during starting phase
    say_emotion_after_start = True # if emotion should be said after or before senctence
    ending_sentence = "Môžeme sa pripraviť na ďalší cvik."
    say_emotion_after_end = True

    is_sitting = False
    is_lying = False
    chair = False

    finished_phases = {str(i): False for i in range(10)}
        
    FAST_MODE = True # Robot movements will be faster
    FAST_MODE_MULTIPLIER = 1
    MIRRORING = True

    warning_said = True
    
    zakladna_pozicia_statia = "Stand"

    hlasky_pool = {
        'sit_stand_raise_arms': [
            '',
            '',
            'Vstaňťe',
            'Zdvihňiťe ruky',
            'Dajťe ruky späť k ťelu',
            'Sadňite si na stoličku',
        ],
        'forefooting_on_chair': [
            'Sadňite si na stoličku',
            'Zdvihňiťe pravé koleno',
            'Položťe nohu na zem',
            'Zdvihňiťe ľavé koleno',
            'Položťe nohu na zem',
        ],
        'forefooting_arm_raising': [
            'Sadňi si na stoličku',
            'Zdvihňi pravé koleno',
            'Polož nohu na zem',
            'Zdvihňi ruky nad hlavu',
            'Vráť ruky naspäť',
            'Zdvihňi ľavé koleno',
            'Polož nohu na zem',
            'Zdvihňi ruky nad hlavu',
            'Vráť ruky naspäť',
        ],
        'forefooting_in_lying': [
            'Ľahňi si na chrbát',
            'Vystri pravú nohu',
            'Polož nohu naspäť na zem',
            'Vystri ľavú nohu',
            'Polož nohu naspäť na zem',
        ],
        'krizny_forefooting_in_lying': [
            '',
            'Zdvihňi a vystri pravú nohu a ľavú ruku',
            'Polož nohu a ruku naspäť na zem',
            'Zdvihňi a vystri ľavú nohu a pravú ruku',
            'Polož nohu a ruku naspäť na zem',
        ],
        'forefooting_rozpazovanie': [
            '',
            'Zdvihňi pravé koleno a upaž ruky',
            'Polož nohu na zem a pripaž ruky',
            'Zdvihňi ľavé koleno a upaž ruky',
            'Polož nohu na zem a pripaž ruky',
        ],
        'forefooting_predpazovanie': [
            '',
            'Zdvihňi pravé koleno a predpaž ruky',
            'Polož nohu na zem a pripaž ruky',
            'Zdvihňi ľavé koleno a predpaž ruky',
            'Polož nohu na zem a pripaž ruky',
        ],
        'forefooting_ruky_nad_hlavu': [
            '',
            'Zdvihňiťe pravé koleno a dajťe ruky nad hlavu',
            'Položťe nohu na zem a pripažťe',
            'Zdvihňiťe ľavé koleno a dajťe ruky nad hlavu',
            'Položťe nohu na zem a pripažťe',
        ],
        'forefooting_ruky_pri_tele': [
            '',
            'Zdvihňiťe pravé koleno',
            'Položťe nohu na zem',
            'Zdvihňiťe ľavé koleno',
            'Položťe nohu na zem',
        ],
        'sadanie_na_stolicku': [
            'Sadňite si na stoličku',
            'Vstaňťe',
        ],
        'predpazovanie': [
            'Predpaž ruky',
            'Pripaž ruky',
        ],
    }


    def __init__(self, naoqi_instance):

        self.naoqi = naoqi_instance
        self.emHelper = EmotionHelper(self.naoqi, self.is_sitting, self.is_lying, self.chair)

        if self.naoqi.is_physical is False:
            self.FAST_MODE_MULTIPLIER = 1.5
    
    def get_random_reaction(self, records):
        return random.randrange(0, len(records))
    

    def say_emotion_start(self, sentence, start_sentence):
        for emotion in self.emHelper.emotions_start:
            
            if emotion in sentence:
                index = self.get_random_reaction(self.emHelper.emotions_start[emotion])
                voiceline = self.emHelper.emotions_start[emotion][index]

                if voiceline["non_verbal"]:
                    getattr(self.emHelper, voiceline["func"])()
                    
                else:
                    if voiceline[self.naoqi.gender]:
                        self.naoqi.speak_or_message(voiceline[self.naoqi.gender])
                    else:
                        self.naoqi.speak_or_message(voiceline["neutral"])
                break
        
        # index = self.get_random_reaction(self.emHelper.emotions_start["Neutral"])
        # em = self.emHelper.emotions_start["Neutral"][index]
        
        # if em["non_verbal"]:
        #     getattr(self.emHelper, em["func"])()
                    
        # else:
        #     voiceline = em
        #     if voiceline[self.naoqi.gender]:
        #         self.naoqi.speak_or_message(voiceline[self.naoqi.gender])
        #     else:
        #         self.naoqi.speak_or_message(voiceline["neutral"])
                
        time.sleep(0.5)
        self.naoqi.speak_or_message(start_sentence)
    
    def say_emotion_exercise(self, sentence):
        print("exercise:", sentence)
        
        for emotion in self.emHelper.emotion_exercise:
            
            if emotion in sentence:
                index = self.get_random_reaction(self.emHelper.emotion_exercise[emotion])
                voiceline = self.emHelper.emotion_exercise[emotion][index]

                if voiceline[self.naoqi.gender]:
                    self.naoqi.speak_or_message(voiceline[self.naoqi.gender])
                else:
                    self.naoqi.speak_or_message(voiceline["neutral"])
                return
            
        index = self.get_random_reaction(self.emHelper.emotion_exercise["Neutral"])    
        voiceline = self.emHelper.emotion_exercise["Neutral"][index]
        
        if voiceline[self.naoqi.gender]:
            self.naoqi.speak_or_message(voiceline[self.naoqi.gender])
        else:
            self.naoqi.speak_or_message(voiceline["neutral"])
        

    def say_emotion_end(self, sentence):
        for emotion in self.emHelper.emotion_end:
            
            if emotion in sentence:
                index = self.get_random_reaction(self.emHelper.emotion_end[emotion])
                voiceline = self.emHelper.emotion_end[emotion][index]
                
                if voiceline["non_verbal"]:
                    getattr(self.emHelper, voiceline["func"])()
                
                else:
                    if voiceline[self.naoqi.gender]:
                        self.naoqi.speak_or_message(voiceline[self.naoqi.gender])
                    else:
                        self.naoqi.speak_or_message(voiceline["neutral"])
                return

        index = self.get_random_reaction(self.emHelper.emotion_end["Neutral"])
        voiceline = self.emHelper.emotion_exercise["Neutral"][index]
        
        if voiceline[self.naoqi.gender]:
            self.naoqi.speak_or_message(voiceline[self.naoqi.gender])
        else:
            self.naoqi.speak_or_message(voiceline["neutral"])

    def say_score(self, score, conn):
        if self.naoqi.er and score != self.naoqi.limit and (score == 2 or score == 4 ):
           conn.send("getEmotion_exercise".encode())
           res = conn.recv(1024)
           self.say_emotion_exercise(res)
           time.sleep(0.75)

        if score == 0:
            self.naoqi.speak_or_message("Pri cvičení nezabudňi plynule dýchať.")
        elif score == 1:
            self.naoqi.speak_or_message("Jeden")
        elif score == 2:
            self.naoqi.speak_or_message("Dva")
        elif score == 3:
            self.naoqi.speak_or_message("Tri, iďe ťi to dobre.")
        elif score == 4:
            self.naoqi.speak_or_message("Štyri.")
        elif score == 5:
            self.naoqi.speak_or_message("Päť.")
        elif score == 6:
            self.naoqi.speak_or_message("Šesť.")
        elif score == 7:
            self.naoqi.speak_or_message("Sedem, už len tri.")
        elif score == 8:
            self.naoqi.speak_or_message("Osem, už len dva.")
        elif score == 9:
            self.naoqi.speak_or_message("Ďeveť, ešťe jeden a máme to.")
        elif score == 10:
            self.naoqi.speak_or_message("Ďesať, super!")
        else:
            self.naoqi.speak_or_message(score)


    def extract_components(self, input_string):
  
        messages = input_string.split(',')   # Split the string by commas into an array of messages
    
        messages = [message for message in messages if message]   # Remove any empty strings that may result from trailing commas

        extracted_components = [] # Initialize an empty list to store the components of each message

        for message in messages:  # Iterate over each message and extract components
        
            initial_number_str = ''  # 1. Extract the initial number as an integer
            
            for char in message:
                if char.isdigit():
                    initial_number_str += char
                else:
                    if initial_number_str:  # Stop at the first non-digit character after digits are found
                        break

        
            score_before = int(initial_number_str) if initial_number_str else 0   # Convert the initial number string to an integer

            # 2. Extract the string between the initial number and the word "_fullfilled"
            # Ensuring that this string does not include digits or the final comma
            start_index = message.find(initial_number_str) + len(initial_number_str)
            fullfilled_index = message.find("_fullfilled")
            message_between = message[start_index:fullfilled_index].lstrip('_').rstrip('_')
            
            # 3. Extract the number after "fullfilled_" as an integer
            # Find the last "_" after "fullfilled_" to get the number in between
            underscore_index = message.find("_", fullfilled_index + 1)
            phase_str = message[underscore_index + 1:]
            phase = int(phase_str) if phase_str.isdigit() else 0

            # Check if 'message_between' ends with '_en' and set phase to -2 if true
            if message_between.endswith("_en"):
                phase = -2

            print("EXTRACTION LOG")
            print(score_before, message_between, phase)
            print("ENDEXTRACTION LOG")
            
            # Append the extracted components to the list
            extracted_components.append((score_before, message_between, phase))

        return extracted_components
    

    def robot_povedz(self, exercise, phase):
        if "_start," in exercise:
            exercise = exercise.replace("_start,", "").strip()
        
        if exercise in self.hlasky_pool:
            messages = self.hlasky_pool[exercise]
            
            if "_start," in exercise:
                message = messages[0]
            else:
                phase_index = phase + 1
                if 0 <= phase_index < len(messages):
                    message = messages[phase_index]
                else:
                    print("Phase index out of bounds for exercise: " + exercise + ", phase: " + str(phase + 1))
                    return
            print("message", message)
            self.naoqi.speak_or_message(message)
        else:
            print("No exercise found with the name: " + exercise)


    def remove_items_by_value(self, messages, score, value, finished_phases, robot_say = True):

        i = len(messages) - 1
        while i >= 0:
            import time
            message_score, _, phase = messages[i]
            # Only remove if the phase and score match and the corresponding phase is actually finished
            if phase == value and message_score == score and (phase == -1 or phase == -2 or finished_phases.get(str(phase), False)):
                messages.pop(i)

                if robot_say:
                    if self.naoqi.is_physical is True:
                        time.sleep(1.5)
                    self.robot_povedz(_, phase)
            i -= 1

        print("REMAINING MESSAGES: ")
        print(messages)
        print("FINISHED PHASES: ")
        print(finished_phases)


    def reset_finished_phases_if_needed(self, finished_phases, pending_messages):
        """
        Resets finished_phases to False if all phases are completed and no pending messages
        are left for the current cycle.
        """
        if all(finished_phases.values()) and not any(msg[2] != 5 for msg in pending_messages):
            for key in finished_phases:
                finished_phases[key] = False
            return True
        return False
    
    
    def stop_tracker(self):
        try:
            self.naoqi.trackerService.stopTracker()
            self.naoqi.trackerService.unregisterAllTargets()
            print("Tracker stopped and all targets unregistered")
        except Exception as e:
            print("Error stopping tracker:")
    
    def run_exercise(self):
        pass




class EmotionHelper(object):

    app = None
   

    def __init__(self, naoqi, is_sitting, is_lying, chair):
        self.is_sitting = is_sitting
        self.is_lying = is_lying
        self.chair = chair

        self.naoqi = naoqi

        self.happiness_start1 = ""
        self.happiness_start2 = ""
        self.surprise_start1 = ""
        self.surprise_start2 = ""

       
        with codecs.open('_exercises_impl/hlasky_em.json', 'r', 'utf-8') as f:
            em_reactions = json.load(f)

            self.emotions_start = em_reactions["start"]

            
            self.emotion_exercise =  em_reactions["exercise"]

            
            self.emotion_end =  em_reactions["end"]

    def reaction_neutral_start(self):
        
        self.naoqi.speak_or_message("Ahoj, som rád, že sa opäť vidíme pri cvičení. Ako sa máš?")
        # self.naoqi.soundDetection.setParameter("Sensitivity", 0.7)
        
        self.sound_detected = False
        
        # def on_sound_detected(value):
        #     self.sound_detected = True
        #     print("Sound detected! Value:", value)
        
        # sound_subscriber = self.naoqi.memory.subscriber("SoundDetected")
        # sound_subscriber.signal.connect(on_sound_detected)
        
       
        # print("Starting sound detection for 5 seconds...")
        # self.naoqi.soundDetection.subscribe("NeutralReactionSoundDetection")
        
        # Wait for 5 seconds
        start_time = time.time()
        while time.time() - start_time < 4:
            time.sleep(0.1)  # Small sleep to prevent CPU hogging
        
       
        # self.naoqi.soundDetection.unsubscribe("NeutralReactionSoundDetection")
        print("Sound detection stopped after 5 seconds.")
        
        if self.sound_detected:
            print("Sound was detected during the 5-second period!")
          
            self.naoqi.speak_or_message("Počula som nejaký zvuk!")  # "I heard a sound!" in Slovak
        else:
           
            self.naoqi.speak_or_message("No dobre, poďme na to")

    def motion_happiness_start(self):

        names = ["LAnklePitch", "LAnkleRoll", "LElbowRoll", "LElbowYaw", "LHand", "LHipPitch", "LHipRoll", "LHipYawPitch", "LKneePitch", "LShoulderPitch", "LShoulderRoll", "LWristYaw", "RAnklePitch", "RAnkleRoll", "RElbowRoll", "RElbowYaw", "RHand", "RHipPitch", "RHipRoll", "RHipYawPitch", "RKneePitch", "RShoulderPitch", "RShoulderRoll", "RWristYaw"]
        
        keys1 = [0.0950661, -0.116542, -0.374254, -1.62301, 0.2884, 0.122762, 0.121228, -0.05058, -0.098218, 0.621228, 0.478566, 0.121144, 0.090548, 0.112024, 0.377406, 1.62753, 0.2864, 0.122678, -0.11961, -0.05058, -0.0919981, 0.622846, -0.481718, 0.0720561]
        keys2 = [0.0950661, -0.102736, -0.424876, -1.17662, 0.292, 0.121228, 0.112024, -0.171766, -0.098218, 1.45266, 0.202446, 0.121144, 0.092082, 0.11049, 0.411154, 1.18267, 0.29, 0.122678, -0.116542, -0.171766, -0.102736, 1.44814, -0.200996, 0.05825]
        if self.chair is False:
            self.naoqi.motionProxy.setAngles(names, keys1, 0.1)
        self.naoqi.speak_or_message("Skvele, vidím, že máš dobru náladu ")
        if self.chair is False:
            self.naoqi.motionProxy.setAngles(names, keys2, 0.1)
        self.naoqi.speak_or_message("Dajme sa teda do toho!")
    
    def motion_surprise_start(self):
      
        names1 = ["LElbowRoll", "LElbowYaw", "LHand", "LShoulderPitch", "LShoulderRoll", "LWristYaw",
                    "RElbowRoll", "RElbowYaw", "RHand", "RShoulderPitch", "RShoulderRoll", "RWristYaw"]
        angles1 = [-0.391128, -1.18736, 0.2908, -0.5937, 0.256136, 0.11194,
                    0.414222, 1.18574, 0.29, 1.47728, -0.234744, 0.05825]
        speed1 = 0.2  # Fraction of max speed
        if self.chair is False:
            self.naoqi.motionProxy.setAngles(names1, angles1, speed1)

        self.naoqi.speak_or_message("Len vydrž, hneď sa dozvieš čo ťa čaka.")


        # Second category (index 1)
        names2 = ["LElbowRoll", "LElbowYaw", "LHand", "LShoulderPitch", "LShoulderRoll", "LWristYaw",
                    "RElbowRoll", "RElbowYaw", "RHand", "RShoulderPitch", "RShoulderRoll", "RWristYaw"]
        angles2 = [-0.429478, -1.17815, 0.2864, 1.45572, 0.210116, 0.11194,
                    0.405018, 1.18267, 0.2868, 1.45121, -0.2102, 0.0597839]
        speed2 = 0.2  # Fraction of max speed
        if self.chair is False:
            self.naoqi.motionProxy.setAngles(names2, angles2, speed2)

        self.naoqi.speak_or_message("O malú chvíľu sa do spoločného cvičenia pustíme! ")
    
    def motion_anger_start(self):
        
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
        if self.chair is False:
            self.naoqi.motionProxy.setAngles(names_head_arms, angles_head_arms, speed_head_arms)


        self.naoqi.speak_or_message("Zdá sa, že ťa dnes niečo rozladilo. Než začneme cvičiť, urobíme si dychové cvičenie. Nadýchni sa cez nos na 4 doby a pomaly vydýchni cez ústa na 6 dôb. Sústreď sa na svoj dych. Zopakuj 6-krát.")

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
        if self.chair is False:
            self.naoqi.motionProxy.setAngles(names_head_arms, angles_head_arms, speed_head_arms)
        time.sleep(0.5)
    
    def motion_happiness_end(self):

            
        names = [
            "LElbowRoll", "LElbowYaw", "LHand", "LShoulderPitch", "LShoulderRoll", "LWristYaw",
            "RElbowRoll", "RElbowYaw", "RHand", "RShoulderPitch", "RShoulderRoll", "RWristYaw"
        ]
        if self.is_sitting:
            keys = [
                -0.515235, -1.2027, 0.2948, 1.25427, 0.641406, 0.0904641,
                1.50029, 1.43271, 0.286, -0.153358, -0.75477, 0.724006
            ]

            keys2 = [
                -0.515235, -1.2027, 0.2948, 1.28809, 0.641406, 0.101229,
                0.439696, 1.43271, 0.286, 1.28809, -0.653296, -0.101229
            ]

            self.naoqi.motionProxy.setAngles(names, keys, 0.15)

            self.naoqi.speak_or_message(self.emotion_end["Happiness"][0]["neutral"] )

            self.naoqi.motionProxy.setAngles(names, keys2, 0.12)
            time.sleep(0.5)
        
        elif self.is_lying:
            self.naoqi.speak_or_message(self.emotion_end["Happiness"][0]["neutral"]) # Using the neutral response
        
        else:
          
            keys1 = [
                -0.423342, -1.18429, 0.2936, 1.44959, 0.207048, 0.108872,
                1.52177, 1.44345, 0.2904, -0.200912, -0.77778, 0.751618
            ]

            keys2 = [
                -0.424876, -1.17969, 0.2888, 1.44805, 0.197844, 0.121144,
                0.408086, 1.18421, 0.2864, 1.45121, -0.20253, 0.0643861
            ]

            self.naoqi.motionProxy.setAngles(names, keys1, 0.15) 

            self.naoqi.speak_or_message(self.emotion_end["Happiness"][0]["neutral"]) 

            self.naoqi.motionProxy.setAngles(names, keys2, 0.1)  
            time.sleep(0.5)