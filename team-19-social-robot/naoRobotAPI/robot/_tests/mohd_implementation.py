from naoqi import ALProxy
import math

motion_proxy = ALProxy("ALMotion", "127.0.0.1", 9559)
posture_proxy = ALProxy("ALRobotPosture", "127.0.0.1", 9559)

def set_joint_angles(joint_names, angles, fraction_of_max_speed):
    """
    Set the angles of specified joints on the NAO robot.
    
    Parameters:
    joint_names (list): The names of the joints to control.
    angles (list): The target angles in radians.
    fraction_of_max_speed (float): The fraction of the maximum speed to use.
    """
    # Convert angles from degrees to radians
    angles_radians = [math.radians(angle) for angle in angles]

    # Set the joint angles using the NAOqi SDK
    for i, joint_name in enumerate(joint_names):
        motion_proxy.setAngles(joint_name, angles_radians[i], fraction_of_max_speed)



def sit_on_small_chair():
    leg_joints = ['LHipPitch', 'RHipPitch', 'LKneePitch', 'RKneePitch', 'LAnklePitch', 'RAnklePitch']

    # Convert angles from degrees to radians
    hip_pitch_angle_degrees = -25  # Adjust to match the sitting posture
    knee_pitch_angle_degrees = 90  # Adjust to match the sitting posture
    ankle_pitch_angle_degrees = -20  # Adjust to match the sitting posture

    hip_pitch_angle_radians = math.radians(hip_pitch_angle_degrees)
    knee_pitch_angle_radians = math.radians(knee_pitch_angle_degrees)
    ankle_pitch_angle_radians = math.radians(ankle_pitch_angle_degrees)

    # Ensure angles are within the range by checking against the joint limits
    if not (-1.535889 <= hip_pitch_angle_radians <= 0.484090):
        raise ValueError("Hip pitch angle out of range")
    if not (-0.103083 <= knee_pitch_angle_radians <= 2.120198):
        raise ValueError("Knee pitch angle out of range")
    if not (-1.186448 <= ankle_pitch_angle_radians <= 0.932056):
        raise ValueError("Ankle pitch angle out of range")

    # Apply the joint angles
    angles = [hip_pitch_angle_radians, hip_pitch_angle_radians, 
              knee_pitch_angle_radians, knee_pitch_angle_radians,
              ankle_pitch_angle_radians, ankle_pitch_angle_radians]
    motion_proxy.setAngles(leg_joints, angles, 0.1)

def straighten_up():
    # Define the adjustment needed to straighten the robot
    hip_pitch_straighten_adjustment_degrees = 5  # This is an example, adjust based on actual need
    hip_pitch_straighten_adjustment_radians = math.radians(hip_pitch_straighten_adjustment_degrees)

    # Get the current angles for the hip joints
    current_hip_pitch_angles = motion_proxy.getAngles(['LHipPitch', 'RHipPitch'], True)
    
    # Calculate the new hip pitch angles and apply them if within the safe range
    new_hip_pitch_angles = [
        max(-1.535889, min(0.484090, current_hip_pitch_angles[0] + hip_pitch_straighten_adjustment_radians)),
        max(-1.535889, min(0.484090, current_hip_pitch_angles[1] + hip_pitch_straighten_adjustment_radians))
    ]

    motion_proxy.setAngles(['LHipPitch', 'RHipPitch'], new_hip_pitch_angles, 0.1)

def sit_on_chair(chair_height_cm):
    """
    Make the NAO robot sit on a chair of a given height.
    
    Parameters:
    chair_height_cm (float): The height of the chair in centimeters.
    """
    # Assuming that the NAO SDK has been properly initialized and proxies set up

    # Wake up robot
    motion_proxy.wakeUp()

    # Ensure the robot is standing
    posture_proxy.goToPosture("Stand", 0.5)

    # Calculate the angles needed for sitting based on the chair height
    # These calculations are placeholders; you would need to calculate the appropriate angles
    # based on the kinematics of the NAO robot and the chair height
    thigh_length_cm = 15  # Placeholder value, you should use the actual thigh length of NAO
    shin_length_cm = 15  # Placeholder value, you should use the actual shin length of NAO
    sitting_knee_angle_degrees = math.degrees(math.acos((thigh_length_cm + shin_length_cm - chair_height_cm) / (2 * thigh_length_cm)))
    
    # Hip needs to move back a certain amount, so we need to calculate this
    hip_pitch_angle_degrees = -sitting_knee_angle_degrees / 2
    # Ankle needs to adjust to keep the foot flat on the ground
    ankle_pitch_angle_degrees = -hip_pitch_angle_degrees

    # Example: setting the angles for hip, knee, and ankle joints to sit down
    motion_proxy.setAngles(["LHipPitch", "RHipPitch"], [math.radians(hip_pitch_angle_degrees)]*2, 0.1)
    motion_proxy.setAngles(["LKneePitch", "RKneePitch"], [math.radians(sitting_knee_angle_degrees)]*2, 0.1)
    motion_proxy.setAngles(["LAnklePitch", "RAnklePitch"], [math.radians(ankle_pitch_angle_degrees)]*2, 0.1)
    

def sit_down_from_standing():
    """
    Transition the NAO robot from a standing position to sitting on an object.
    """
    # Example: setting the angles for hip and knee joints to simulate sitting down
    # Note that each joint name is paired with its angle in separate calls
    set_joint_angles(["LHipRoll", "RHipRoll"], [-25, -25], 0.1)
    set_joint_angles(["LHipPitch", "RHipPitch"], [-25, -25], 0.1)
    set_joint_angles(["LKneePitch", "RKneePitch"], [50, 50], 0.1)
    set_joint_angles(["LAnklePitch", "RAnklePitch"], [25, 25], 0.1)
    set_joint_angles(["LAnkleRoll", "RAnkleRoll"], [25, 25], 0.1)

if __name__ == "__main__":
    robot_ip = "127.0.0.1"
    robot_port = 9559

    motion_proxy = ALProxy("ALMotion", robot_ip, robot_port)
    posture_proxy = ALProxy("ALRobotPosture", robot_ip, robot_port)
    # sit_on_chair(chair_height_cm=12)
    posture_proxy.goToPosture("Stand", 1.0)

    sit_on_small_chair()
    straighten_up()

    # sit_down_from_standing()
    # sit_down()
