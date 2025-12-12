# -*- encoding: UTF-8 -*- 

import qi
import argparse
import sys
import time
import math
import almath

import signal

def signal_handler(signal, frame):
    print('You pressed Ctrl+C!')
    sys.exit(0)

signal.signal(signal.SIGINT, signal_handler)

class LandmarkDetector(object):
    def __init__(self, app):
        super(LandmarkDetector, self).__init__()
        app.start()
        session = app.session

        # Initialize services
        self.memory = session.service("ALMemory")
        self.motion_service = session.service("ALMotion")
        self.posture_service = session.service("ALRobotPosture")
        self.tts = session.service("ALTextToSpeech")
        self.landmark_detection = session.service("ALLandMarkDetection")
        self.tracker = session.service("ALTracker")

        self.tracker = session.service("ALVisualCompass")

        # Assume an instance of ALVisualCompassProxy is initialized here if you're planning to use it
        # self.visual_compass = session.service("ALVisualCompass")

        # Subscribe to the ALLandMarkDetection extractor
        self.landmark_detection.subscribe("LandmarkDetector", 500, 0.0)
        self.got_landmark = False
        self.landmarkTheoreticalSize = 0.10  # Size of the landmark in meters
        self.currentCamera = "CameraTop"

        # Connect the event callback
        self.subscriber = self.memory.subscriber("LandmarkDetected")
        self.subscriber.signal.connect(self.on_landmark_detected)

    def cleanup(self):
        # Unsubscribe and cleanup actions
        try:
            self.landmark_detection.unsubscribe("LandmarkDetector")
            print("Successfully unsubscribed and cleaned up.")
        except Exception as e:
            print("Cleanup failed:", e)
        finally:
            sys.exit(0)  # Exit after cleanup

    def set_head_position(self, pitch):
        # Example method to move the robot's head to scan for landmarks
        try:
            self.motion_service.setAngles("HeadPitch", pitch, 0.1)
        except Exception as e:
            print("Error setting head position:", e)

    def scan_for_landmarks(self):
        # Scan for landmarks by adjusting the head pitch
        pitch_angles = [0, 0.15, 0.3]  # Example pitch angles: straight ahead, slightly down, more down
        for pitch in pitch_angles:
            self.set_head_position(pitch)
            time.sleep(1)  # Wait for the head movement to complete and for landmark detection

    def on_landmark_detected(self, value):
        if value == []:  # No landmark is detected
            self.got_landmark = False
        else:
            if not self.got_landmark:  # Act only the first time a landmark is detected
                self.got_landmark = True
                self.tts.say("našiel som značku")

                # Process landmark detection data
                markData = value[1][0]  # Assuming one landmark detected
                wzCamera = markData[0][1]
                wyCamera = markData[0][2]
                angularSize = markData[0][3]
                distanceFromCameraToLandmark = self.landmarkTheoreticalSize / (2 * math.tan(angularSize / 2))

                # Compute the robot to landmark transform
                transform = self.motion_service.getTransform(self.currentCamera, 2, True)
                robotToCamera = almath.Transform(almath.vectorFloat(transform))
                cameraToLandmarkRotationTransform = almath.Transform_from3DRotation(0, wyCamera, wzCamera)
                cameraToLandmarkTranslationTransform = almath.Transform(distanceFromCameraToLandmark, 0, 0)
                robotToLandmark = robotToCamera * cameraToLandmarkRotationTransform * cameraToLandmarkTranslationTransform

                # Extract x, y positions for movement and angle for the robot to face the landmark
                x = robotToLandmark.r1_c4
                y = robotToLandmark.r2_c4
                theta = math.atan2(y, x)

                # Move the robot towards the landmark
                try:
                    self.motion_service.moveTo(x - 0, y, theta)  # Adjust distance as needed
                    self.tts.say("Došiel som ku značke!")
                except Exception as e:
                    print("Error in moving to landmark:", e)

    def run(self):
        try:
            self.posture_service.goToPosture("StandInit", 0.5)
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            print("Interrupted by user, stopping LandmarkDetector")
        finally:
            self.cleanup()  # Ensure cleanup is called regardless of how the script exits.
            sys.exit(0)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--ip", type=str, default="172.20.10.7",
                        help="Robot IP address. On robot or Local Naoqi: use '172.20.10.7'.")
    parser.add_argument("--port", type=int, default=9559,
                        help="Naoqi port number")

    args = parser.parse_args()
    connection_url = "tcp://" + args.ip + ":" + str(args.port)
    app = qi.Application(["LandmarkDetector", "--qi-url=" + connection_url])
    landmark_detector = LandmarkDetector(app)

    try:
        landmark_detector.run()
    finally:
        landmark_detector.cleanup()