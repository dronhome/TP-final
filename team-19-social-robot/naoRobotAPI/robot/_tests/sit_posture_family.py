from naoqi import ALProxy

# Replace with your NAO's IP address and port number
NAO_IP = "127.0.0.7"
NAO_PORT = 9559

# Create a proxy to ALRobotPosture
postureProxy = ALProxy("ALRobotPosture", NAO_IP, NAO_PORT)

# Use goToPosture method to go to SittingOnChair posture
posture = "LyingLeft"
speed = 0.5  # Speed of the posture transition where 1 is the maximum speed

try:
    success = postureProxy.goToPosture(posture, speed)
    if success:
        print("NAO robot has successfully moved to posture.")
    else:
        print("Failed to move NAO robot to posture.")
except Exception as e:
    print("ERROR")
    print(e)