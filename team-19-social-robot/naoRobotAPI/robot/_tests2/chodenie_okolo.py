# interpreter python 2.7 (TimiBakalarka)

import math
import threading
from naoqi import ALProxy
import mutex

import numpy as np
import pandas as pd
import time
from pyzbar.pyzbar import decode

robot_ip = "192.168.86.194"
# robot_ip = "localhost"
robot_port = 9559

RYCHLOST_NATACANIA = 2.5
initial_move_delay = 6

posture = ALProxy("ALRobotPosture", robot_ip, robot_port)
motion = ALProxy("ALMotion", robot_ip, robot_port)
camera = ALProxy("ALVideoDevice", robot_ip, robot_port)
memory_proxy = ALProxy("ALMemory", robot_ip, robot_port)

stop_movement = mutex.mutex()
stop_movement.testandset()
change_movement = mutex.mutex()
change_movement.testandset()
change_theta = mutex.mutex()
print("==== Start ====")
print("Is change_movement mutex locked:", change_movement.test())

theta = 0.0
velx = 1.0
turn_count = 0

current_velocity = 0.0
current_distance = 0.0

def move():
    global turn_count, change_movement, theta
    time.sleep(2)

    print("==== Start Move ====")
    while True:
        if not change_theta.testandset():
            motion.moveToward(velx, 0, theta)
            # motion.stopMove()
        if change_movement.testandset():
            turn_count += 1
            print("Rotating over 90 degrees")
            motion.stopMove()
            if turn_count <= 4:
                motion.moveTo(0, 0, (np.pi/2))
            theta = 0.0
           
            if turn_count >= 5:
                stop_movement.unlock()
                time.sleep(0.5)
                posture.goToPosture("StandInit", 1.0)
                time.sleep(2)
                # motion.moveTo(0, 0, np.pi/2)
                print("==== Stopped after 4 turns ====")
                break
        if stop_movement.test():
            time.sleep(0.1)
            continue
        else:
            break
    motion.stopMove()
    print("==== Stop Move ====")

def find_qr_center(qr_codes, current_target, num_of_targets=4):
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

def capture_image():
    global theta, velx
    time.sleep(0.1)
    print("==== Start Capture Image ====")
    camera_name = "python_camera"
    fps = 24
    color_space = 13
    resolution = 2
    cam_id = camera.subscribeCamera(camera_name, 0, resolution, color_space, fps)
    print("Camera ID:", cam_id)

    if cam_id is None or len(cam_id) == 0:
        print("Nepodarilo sa ziskat obraz z kamery OPS!")
        camera.unsubscribe(cam_id)
        time.sleep(0.1)
        cam_id = camera.subscribeCamera(camera_name, 0, resolution, color_space, fps)
        if cam_id is None or len(cam_id) == 0:
            print("Nenajdena kamera, vypinam program!")
            camera.unsubscribe(cam_id)
            time.sleep(0.1)
            motion.stopWalk()
            stop_movement.unlock()
            print("All stopped")
            exit(0)

    # camera = cv2.VideoCapture(0)

    # cv2.imshow("Camera", np.zeros((640, 480, 3), dtype=np.uint8))

    while stop_movement.test():
        # ret, image = camera.read()
        if cam_id is None:
            cam_id = camera.subscribeCamera(camera_name, 0, resolution, color_space, fps)

        image = camera.getImageRemote(cam_id)
        if image is None:
            print("Nepodarilo sa ziskat obraz z kamery!")
            camera.unsubscribe(cam_id)
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
                qr_center_x, qr_center_y, target, points = find_qr_center(qr_codes, current_target)

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
                    old_theta = theta
                    theta =  -RYCHLOST_NATACANIA * ((delta_x / width) * FOV * (np.pi / 180))/(2*np.pi)
                    #theta = -theta
                    print("Odchylka QR kodu: dx =", delta_x, ", dy =", delta_y, ", theta =", theta, ", old_theta =", old_theta)

                    change_theta.unlock()

                    print("Old theta:", old_theta, "\tNew theta:", theta)
                 
            else:
                print("Nevidim QR kod")
        if not stop_movement.test():
            break
        time.sleep(0.01)

    # camera.release()
    camera.unsubscribe(cam_id)
    #stop_movement.unlock()
    motion.stopMove()
    print("All stopped")
    print("==== Stop Capture Image ====")

def rotate_head():
    print("==== Start Rotate Head ====")
    while stop_movement.test():
        motion.setAngles(["HeadYaw", "HeadPitch"], [0.0, 0.0], 0.1)
        if stop_movement.test():
            time.sleep(0.1)
            continue
        else:
            break
    print("==== Stop Rotate Head ====")

def log_data():
    global current_distance, current_velocity
    dt = pd.DataFrame(columns=["Time", "AccelX", "AccelY", "AccelZ", "AngleX", "AngleY", "AngleZ", "RightFootPressure",
                               "LeftFootPressure", "CenterPressureRFootX", "CenterPressureRFootY",
                               "CenterPressureLFootX", "CenterPressureLFootY", "GyroX", "GyroY", "GyroZ",
                               "GyroXZeroOffset", "GyroYZeroOffset", "GyroZZeroOffset", "GyrX", "GyrY", "GyrZ", "RefVx", "RefTheta",
                               "Velocity","Distance"])
    Tvz = 0.05
    try:
        print("==== Data start ====")
        while stop_movement.test():
            accel_x = memory_proxy.getData("Device/SubDeviceList/InertialSensor/AccX/Sensor/Value")
            accel_y = memory_proxy.getData("Device/SubDeviceList/InertialSensor/AccY/Sensor/Value")
            accel_z = memory_proxy.getData("Device/SubDeviceList/InertialSensor/AccZ/Sensor/Value")
            angle_x = memory_proxy.getData("Device/SubDeviceList/InertialSensor/AngleX/Sensor/Value")
            angle_y = memory_proxy.getData("Device/SubDeviceList/InertialSensor/AngleY/Sensor/Value")
            angle_z = memory_proxy.getData("Device/SubDeviceList/InertialSensor/AngleZ/Sensor/Value")
            pressure_r_foot = memory_proxy.getData("Device/SubDeviceList/RFoot/FSR/TotalWeight/Sensor/Value")
            pressure_l_foot = memory_proxy.getData("Device/SubDeviceList/LFoot/FSR/TotalWeight/Sensor/Value")
            center_pressure_r_foot_x = memory_proxy.getData(
                "Device/SubDeviceList/RFoot/FSR/CenterOfPressure/X/Sensor/Value")
            center_pressure_r_foot_y = memory_proxy.getData(
                "Device/SubDeviceList/RFoot/FSR/CenterOfPressure/Y/Sensor/Value")
            center_pressure_l_foot_x = memory_proxy.getData(
                "Device/SubDeviceList/LFoot/FSR/CenterOfPressure/X/Sensor/Value")
            center_pressure_l_foot_y = memory_proxy.getData(
                "Device/SubDeviceList/LFoot/FSR/CenterOfPressure/Y/Sensor/Value")
            # pressure_r_foot = memory_proxy.getData("Motion/Sensor/Velocity/WheelFR")
            # pressure_l_foot = memory_proxy.getData("Motion/Sensor/Velocity/WheelFL")
            gyro_x = memory_proxy.getData("Device/SubDeviceList/InertialSensor/GyroscopeX/Sensor/Value")
            gyro_y = memory_proxy.getData("Device/SubDeviceList/InertialSensor/GyroscopeY/Sensor/Value")
            gyro_z = memory_proxy.getData("Device/SubDeviceList/InertialSensor/GyroscopeZ/Sensor/Value")
            gyro_zero_offset_x = memory_proxy.getData(
                "Device/SubDeviceList/InertialSensor/GyroscopeXZeroOffset/Sensor/Value")
            gyro_zero_offset_y = memory_proxy.getData(
                "Device/SubDeviceList/InertialSensor/GyroscopeYZeroOffset/Sensor/Value")
            gyro_zero_offset_z = memory_proxy.getData(
                "Device/SubDeviceList/InertialSensor/GyroscopeZZeroOffset/Sensor/Value")
            gyrx = memory_proxy.getData("Device/SubDeviceList/InertialSensor/GyrX/Sensor/Value")
            gyry = memory_proxy.getData("Device/SubDeviceList/InertialSensor/GyrY/Sensor/Value")
            gyrz = memory_proxy.getData("Device/SubDeviceList/InertialSensor/GyrZ/Sensor/Value")

            current_velocity += accel_x * Tvz
            current_distance += current_velocity * Tvz

            dt.loc[len(dt)] = [time.time(), accel_x, accel_y, accel_z, angle_x, angle_y, angle_z, pressure_r_foot,
                               pressure_l_foot, center_pressure_r_foot_x, center_pressure_r_foot_y,
                               center_pressure_l_foot_x, center_pressure_l_foot_y, gyro_x, gyro_y, gyro_z,
                               gyro_zero_offset_x, gyro_zero_offset_y, gyro_zero_offset_z, gyrx, gyry, gyrz,
                               velx, theta, current_velocity, current_distance]

            time.sleep(Tvz)
            if not stop_movement.test():
                break
        print("==== Data stop ====")
    except KeyboardInterrupt:
        print("Data stop")
    finally:
        dt.to_csv("vpred_data.csv")
        exit(0)

#sadanie

#najprv ho dat posture ze stoji
motion.wakeUp()
time.sleep(3)

try:
    thread1 = threading.Thread(target=move)
    thread2 = threading.Thread(target=capture_image)
    thread3 = threading.Thread(target=rotate_head)
    thread4 = threading.Thread(target=log_data)

    def rotation_timer():
        global turn_count
        print(turn_count)
        if turn_count == 0:
            rotation_time = 10
        elif turn_count == 1:
            rotation_time = 13
        elif turn_count == 2:
            rotation_time = 13
        elif turn_count == 3:
            rotation_time = 12
        elif turn_count == 4:
            rotation_time = 3
        elif turn_count == 5:
            rotation_time = 0          
        if not stop_movement.test():
            print("Stopping robot movement...")
            return
        threading.Timer(rotation_time, rotation_timer).start()
        print("Timer has run out")
        change_movement.unlock()

    thread1.start()
    thread2.start()
    thread3.start()
    thread4.start()
    print("***********Sleeping")
    time.sleep(initial_move_delay)
    print("***********Waking up")
    rotation_timer()

    thread1.join()
    thread2.join()
    thread3.join()
    thread4.join()
except KeyboardInterrupt:
    print("Threads stop")
    stop_movement.testandset()
    motion.stopMove()
    camera.unsubscribe("python_camera")


#sadne, vstane, obide, padne

#aktual: sadne, vstane, obide, nic nespravi (nepadne ani si nesadne)

#ps: menila som podla gemini tie for loopy (tusim v capture image 1000, rotate_head a log_data --> na while..)
#zakomentovala som tie dve snimky s i (lebo uz nemame i) tusim v image capture