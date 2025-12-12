from naoqi import ALProxy

# Connect to the robot
NAO_IP = "192.168.86.194"  # Replace with your NAO's IP address
NAO_PORT = 9559

# Create proxies for the diagnosis and battery services
diagnosisProxy = ALProxy("ALDiagnosis", NAO_IP, NAO_PORT)
batteryProxy = ALProxy("ALBattery", NAO_IP, NAO_PORT)

# Check the battery level
batteryLevel = batteryProxy.getBatteryCharge()
print("Battery Level:", batteryLevel, "%")

# Check for any diagnosed issues
diagnosedIssues = diagnosisProxy.getActiveDiagnosis()
print("Diagnosed Issues (Active):", diagnosedIssues)

diagnosedIssues = diagnosisProxy.getPassiveDiagnosis()
print("Diagnosed Issues (Passive):", diagnosedIssues)