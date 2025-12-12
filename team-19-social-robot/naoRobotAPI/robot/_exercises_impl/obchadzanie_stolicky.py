# -*- coding: utf-8 -*-


import sys
import os

import math
import threading

import mutex

import numpy as np
import pandas as pd
import time
from pyzbar.pyzbar import decode

from robot_exercise_utils import RobotExerciseUtils
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import sit_exercise

module_path = os.path.join(os.getcwd(), 'sadanie')
if module_path not in sys.path:
    sys.path.append(module_path)

import sitting_position_for_extending_legs as sit_on_chair
import daj_ruky_k_telu_zo_zakladneho_sedu as ruky_k_telu_zo_zakladneho_sedu


class ObchadzanieOkoloStolicky(RobotExerciseUtils):
    starting_sentence = ""

    RYCHLOST_NATACANIA = 2.5
    initial_move_delay = 6

        
    stop_movement = mutex.mutex()
    stop_movement.testandset()
    change_movement = mutex.mutex()
    change_movement.testandset()
    change_theta = mutex.mutex()

    theta = 0.0
    velx = 1.0
    turn_count = 0

    current_velocity = 0.0
    current_distance = 0.0
      
    def __init__(self, naoqi_instance):
         
        self.exercise_name = 'chairExercise'
      
        self.chair = True

        super(ObchadzanieOkoloStolicky, self).__init__(naoqi_instance)
        self.naoqi.init_walking_around_chair()

        self.exercise_name = 'chairExercise'

        self.thread1 = threading.Thread(target=self.move)
        self.thread2 = threading.Thread(target=self.capture_image)
        self.thread3 = threading.Thread(target=self.rotate_head)
        self.thread4 = threading.Thread(target=self.log_data)
    
    def warning_say(self, message):
        
        if  "Clovek_nesedi" in message:
            self.naoqi.speak_or_message("Prosím sadni si na te stoličku.")
            
        elif "Clovek_sa_ma_postavit" in message:
            self.naoqi.speak_or_message("Prosím postav sa a obíťe stoličku.")

        elif "Clovek_musi_ist_dolava" in  message :
            self.naoqi.speak_or_message("Prosím choď pár krokov doľava od stoličky.")

        elif "Clovek_musi_ist_dozadu" in  message:
            self.naoqi.speak_or_message("Prosím obráťte sa a kračajt pár krokov dozadu za stoličku.")

        elif "Clovek_musi_ist_doprava" in  message:
            self.naoqi.speak_or_message("Prosím choď za pravú stranu stoličky")

        elif "Clovek_musi_ist_dopredu" in  message:
            self.naoqi.speak_or_message("Prosím vráť sa dopredu a posaď sa na stoličku.")
        
    def run_exercise(self, score, message, conn):

        
        if message == 'chair_circling_up':
            self.say_score(score + 1, conn)
            if score + 1 < 5:
                s2 =  'Prejdi znova okolo stoličky'
                self.naoqi.speak_or_message(s2)
            conn.send("ExerciseContinue".encode())
        
        if message == 'chair_circling_end':

            if self.naoqi.er:
                 time.sleep(0.5)
                 conn.send("getEmotion_end".encode())
            else:
                self.naoqi.speak_or_message("Super. Zvládľi sme to na jednotku.")

        elif message == 'chair_circling_start':
            
            if self.naoqi.er:
                conn.send("getEmotion_start".encode())
                message = conn.recv(1024)
                self.say_emotion_start(message, "")


            s1 = 'Začíname obchádzaňie okolo stoličky zo sedu, postav sa pred stolicku.'
            self.naoqi.speak_or_message(s1)
            time.sleep(0.5)
            s2 =  ' Najprv ti ukážem priebeh cvičenia, potom to po mňe zopakuješ päť krát.'
            self.naoqi.speak_or_message(s2)
           
            self.naoqi.motionProxy.wakeUp()
            time.sleep(1.5)
            if self.naoqi.is_physical:
                try:
                    def rotation_timer():
                    
                        print(self.turn_count)
                        if self.turn_count == 0:
                            rotation_time = 10
                        elif self.turn_count == 1:
                            rotation_time = 13
                        elif self.turn_count == 2:
                            rotation_time = 13
                        elif self.turn_count == 3:
                            rotation_time = 10
                        elif self.turn_count == 4:
                            rotation_time = 3
                        elif self.turn_count == 5:
                            rotation_time = 3          
                        if not self.stop_movement.test():
                            print("Stopping robot movement...")
                            return
                        threading.Timer(rotation_time, rotation_timer).start()
                        print("Timer has run out")
                        self.change_movement.unlock()

                    self.thread1.start()
                    self.thread2.start()
                    self.thread3.start()
                    self.thread4.start()
                    print("***********Sleeping")
                    time.sleep(self.initial_move_delay)
                    print("***********Waking up")
                    rotation_timer()

                    self.thread1.join()
                    self.thread2.join()
                    self.thread3.join()
                    self.thread4.join()
                except KeyboardInterrupt:
                    print("Threads stop")
                    self.stop_movement.testandset()
                    self.naoqi.motionProxy.stopMove()
                    self.naoqi.camera.unsubscribe("python_camera")
            else:
               
                self.perform_chair_circling()
            
            s1 = 'Teraz prišiel čas na ťeba'
            self.naoqi.speak_or_message(s1)
            time.sleep(0.5)
            s2 =  'Sadni si a po napomenuťí chodťe okolo stoličky miernim tempom'
            self.naoqi.speak_or_message(s2)
            conn.send("ExerciseContinue".encode())
            time.sleep(0.5)
           
            conn.send("ExerciseContinue".encode())
           

    def move(self):
      
        time.sleep(2)

        print("==== Start Move ====")
        while True:
            if not self.change_theta.testandset():
                self.naoqi.motionProxy.moveToward(self.velx, 0, self.theta)
                # motion.stopMove()
            if self.change_movement.testandset():
                self.turn_count += 1
                print("Rotating over 90 degrees")
                self.naoqi.motionProxy.stopMove()
                if self.turn_count <= 4:
                    self.naoqi.motionProxy.moveTo(0, 0, (np.pi/2))
                self.theta = 0.0
            
                if self.turn_count >= 5:
                    self.stop_movement.unlock()
                    time.sleep(0.5)
                    self.naoqi.motionProxy.moveTo(0, 0, -(np.pi/2))
                   
                    time.sleep(2)
                    # motion.moveTo(0, 0, np.pi/2)
                    print("==== Stopped after 4 turns ====")
                    break
            if self.stop_movement.test():
                time.sleep(0.1)
                continue
            else:
                break
        self.naoqi.postureProxy.stopMove()
        print("==== Stop Move ====")
    
    def find_qr_center(self, qr_codes, current_target, num_of_targets=4):
        for qr in qr_codes:
            data = qr.data.decode('utf-8')
            if "Ciel" in data:
                    target = int(data.split("Ciel")[1])%num_of_targets
            else:
                print("QR code doesn't contain expected 'Ciel' format:", data)
                target = None
            # if target != current_target and target != ((current_target - 1)%num_of_targets):
            #     return None, None, None, None

            print("\nNajdeny QR kod:", data)

            points = qr.polygon
            print("Suradnice rohov QR kodu:", points)

            if len(points) == 4:
                x_coords = [point.x for point in points]
                y_coords = [point.y for point in points]

                qr_center_x = sum(x_coords) / len(x_coords)
                qr_center_y = sum(y_coords) / len(y_coords)

                print("Stred QR kodu: {}, {}".format(qr_center_x, qr_center_y))
        return qr_center_x, qr_center_y, target, points
    

    def capture_image(self):
      
        time.sleep(0.1)
        print("==== Start Capture Image ====")
        camera_name = "python_camera"
        fps = 24
        color_space = 13
        resolution = 2
        cam_id = self.naoqi.camera.subscribeCamera(camera_name, 0, resolution, color_space, fps)
        print("Camera ID:", cam_id)

        if cam_id is None or len(cam_id) == 0:
            print("Nepodarilo sa ziskat obraz z kamery OPS!")
            self.naoqi.camera.unsubscribe(cam_id)
            time.sleep(0.1)
            cam_id = self.naoqi.camera.subscribeCamera(camera_name, 0, resolution, color_space, fps)
            if cam_id is None or len(cam_id) == 0:
                print("Nenajdena kamera, vypinam program!")
                self.naoqi.camera.unsubscribe(cam_id)
                time.sleep(0.1)
                self.naoqi.motionProxy.stopWalk()
                self.stop_movement.unlock()
                print("All stopped")
                exit(0)

        # camera = cv2.VideoCapture(0)

        # cv2.imshow("Camera", np.zeros((640, 480, 3), dtype=np.uint8))

        while self.stop_movement.test():
            # ret, image = camera.read()
            if cam_id is None:
                cam_id = self.naoqi.camera.subscribeCamera(camera_name, 0, resolution, color_space, fps)

            image = self.naoqi.camera.getImageRemote(cam_id)
            if image is None:
                print("Nepodarilo sa ziskat obraz z kamery!")
                self.naoqi.camera.unsubscribe(cam_id)
                cam_id = None
                time.sleep(0.01)
                continue
            else:
                # imageorg = image
                width = image[0]
                height = image[1]
                image_data = image[6]

                #width, height = image.shape[1], image.shape[0] # Pouzivat iba ked sa snima z webkamery
                imageorg = np.frombuffer(image_data, dtype=np.uint8).reshape((height, width, 3))


                # tu zavolaj ten vypocet a nastav theta novu
                qr_codes = decode(imageorg)
                print("QR CODES LEN:", len(qr_codes))
                current_target = 1
                if len(qr_codes) != 0:
                    qr_center_x, qr_center_y, target, points = self.find_qr_center(qr_codes, current_target)

                    # Vypocet odchylky QR kodu od stredu kamery
                    if qr_center_x is not None and qr_center_y is not None:
                        # Ziskanie rozlisenia kamery
                        width, height = imageorg.shape[1], imageorg.shape[0]
                        print("Rozlisenie kamery: width =", width, ", height =", height)
                        x_c, y_c = width / 2, height / 2

                        # Vypocet odchylky QR kodu od stredu kamery
                        delta_x = float(qr_center_x - x_c)
                        delta_y = float(qr_center_y - y_c)

                        FOV = 60.0
                        old_theta = self.theta
                        self.theta =  -self.RYCHLOST_NATACANIA * ((delta_x / width) * FOV * (np.pi / 180))/(2*np.pi)
                        #theta = -theta
                        print("Odchylka QR kodu: dx =", delta_x, ", dy =", delta_y, ", theta =", self.theta, ", old_theta =", old_theta)

                        self.change_theta.unlock()

                        print("Old theta:", old_theta, "\tNew theta:",  self.theta)
                       
                else:
                   
                    print("Nevidim QR kod")
            if not self.stop_movement.test():
                break
            time.sleep(0.01)

        # camera.release()
        self.naoqi.camera.unsubscribe(cam_id)
        #stop_movement.unlock()
        self.naoqi.motionProxy.stopMove()
        print("All stopped")
        print("==== Stop Capture Image ====")
    

    def rotate_head(self):
        print("==== Start Rotate Head ====")
        while self.stop_movement.test():
            self.motionProxy.setAngles(["HeadYaw", "HeadPitch"], [0.0, 0.0], 0.1)
            if self.stop_movement.test():
                time.sleep(0.1)
                continue
            else:
                break
        print("==== Stop Rotate Head ====")

    def log_data(self):
        global current_distance, current_velocity
        dt = pd.DataFrame(columns=["Time", "AccelX", "AccelY", "AccelZ", "AngleX", "AngleY", "AngleZ", "RightFootPressure",
                                "LeftFootPressure", "CenterPressureRFootX", "CenterPressureRFootY",
                                "CenterPressureLFootX", "CenterPressureLFootY", "GyroX", "GyroY", "GyroZ",
                                "GyroXZeroOffset", "GyroYZeroOffset", "GyroZZeroOffset", "GyrX", "GyrY", "GyrZ", "RefVx", "RefTheta",
                                "Velocity","Distance"])
        Tvz = 0.05
        try:
            print("==== Data start ====")
            while self.stop_movement.test():
                accel_x = self.naoqi.memory_proxy.getData("Device/SubDeviceList/InertialSensor/AccX/Sensor/Value")
                accel_y = self.naoqi.memory_proxy.getData("Device/SubDeviceList/InertialSensor/AccY/Sensor/Value")
                accel_z = self.naoqi.memory_proxy.getData("Device/SubDeviceList/InertialSensor/AccZ/Sensor/Value")
                angle_x = self.naoqi.memory_proxy.getData("Device/SubDeviceList/InertialSensor/AngleX/Sensor/Value")
                angle_y = self.naoqi.memory_proxy.getData("Device/SubDeviceList/InertialSensor/AngleY/Sensor/Value")
                angle_z = self.naoqi.memory_proxy.getData("Device/SubDeviceList/InertialSensor/AngleZ/Sensor/Value")
                pressure_r_foot = self.naoqi.memory_proxy.getData("Device/SubDeviceList/RFoot/FSR/TotalWeight/Sensor/Value")
                pressure_l_foot = self.naoqi.memory_proxy.getData("Device/SubDeviceList/LFoot/FSR/TotalWeight/Sensor/Value")
                center_pressure_r_foot_x = self.naoqi.memory_proxy.getData(
                    "Device/SubDeviceList/RFoot/FSR/CenterOfPressure/X/Sensor/Value")
                center_pressure_r_foot_y = self.naoqi.memory_proxy.getData(
                    "Device/SubDeviceList/RFoot/FSR/CenterOfPressure/Y/Sensor/Value")
                center_pressure_l_foot_x = self.naoqi.memory_proxy.getData(
                    "Device/SubDeviceList/LFoot/FSR/CenterOfPressure/X/Sensor/Value")
                center_pressure_l_foot_y = self.naoqi.memory_proxy.getData(
                    "Device/SubDeviceList/LFoot/FSR/CenterOfPressure/Y/Sensor/Value")
                # pressure_r_foot = memory_proxy.getData("Motion/Sensor/Velocity/WheelFR")
                # pressure_l_foot = memory_proxy.getData("Motion/Sensor/Velocity/WheelFL")
                gyro_x = self.naoqi.memory_proxy.getData("Device/SubDeviceList/InertialSensor/GyroscopeX/Sensor/Value")
                gyro_y = self.naoqi.memory_proxy.getData("Device/SubDeviceList/InertialSensor/GyroscopeY/Sensor/Value")
                gyro_z = self.naoqi.memory_proxy.getData("Device/SubDeviceList/InertialSensor/GyroscopeZ/Sensor/Value")
                gyro_zero_offset_x = self.naoqi.memory_proxy.getData(
                    "Device/SubDeviceList/InertialSensor/GyroscopeXZeroOffset/Sensor/Value")
                gyro_zero_offset_y = self.naoqi.memory_proxy.getData(
                    "Device/SubDeviceList/InertialSensor/GyroscopeYZeroOffset/Sensor/Value")
                gyro_zero_offset_z = self.naoqi.memory_proxy.getData(
                    "Device/SubDeviceList/InertialSensor/GyroscopeZZeroOffset/Sensor/Value")
                gyrx = self.naoqi.memory_proxy.getData("Device/SubDeviceList/InertialSensor/GyrX/Sensor/Value")
                gyry = self.naoqi.memory_proxy.getData("Device/SubDeviceList/InertialSensor/GyrY/Sensor/Value")
                gyrz = self.naoqi.memory_proxy.getData("Device/SubDeviceList/InertialSensor/GyrZ/Sensor/Value")

                current_velocity += accel_x * Tvz
                current_distance += current_velocity * Tvz

                dt.loc[len(dt)] = [time.time(), accel_x, accel_y, accel_z, angle_x, angle_y, angle_z, pressure_r_foot,
                                pressure_l_foot, center_pressure_r_foot_x, center_pressure_r_foot_y,
                                center_pressure_l_foot_x, center_pressure_l_foot_y, gyro_x, gyro_y, gyro_z,
                                gyro_zero_offset_x, gyro_zero_offset_y, gyro_zero_offset_z, gyrx, gyry, gyrz,
                                self.velx,  self.theta, current_velocity, current_distance]

                # Nefunguje, zatial sa to bude riesit casovacom.
                # if current_distance >= 1.0:
                #     print("Distance is:", current_distance)
                #     change_movement.unlock()
                #     motion.stopMove()
                #     current_distance = 0.0
                #     print("==== Stopped after 1.0m ====")
                time.sleep(Tvz)
                if not self.naoqi.stop_movement.test():
                    break
            print("==== Data stop ====")
        except KeyboardInterrupt:
            print("Data stop")
        finally:
            dt.to_csv("vpred_data.csv")
            exit(0)
        
    def perform_chair_circling(self):
        
        step_distances = [0.1, 0.2, 0.3, 0.4, 0.4,]
        
        print("Starting chair circling simulation.")
        
        for i, distance in enumerate(step_distances):
           
            self.naoqi.motionProxy.moveTo(distance, 0.0, 0.0)  # Move forward

          
            self.naoqi.motionProxy.moveTo(0.0, 0.0, (np.pi/2))  # Turn left
        
        self.naoqi.motionProxy.moveTo(0.2, 0.0, 0.0)  # Move forward

          
        self.naoqi.motionProxy.moveTo(0.0, 0.0, -(np.pi/2))  # Turn left
        print("Finished chair circling.")