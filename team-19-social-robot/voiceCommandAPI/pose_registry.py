# Predefined NAO pose registry for voice commands.
#
# Joint order matches setting_pose.py in naoRobotAPI:
#   0  LShoulderPitch   1  LShoulderRoll   2  LElbowRoll    3  LElbowYaw    4  LWristYaw
#   5  RShoulderPitch   6  RShoulderRoll   7  RElbowRoll    8  RElbowYaw    9  RWristYaw
#  10  LHipRoll        11  LHipPitch       12 LKneePitch    13 LAnklePitch  14 LAnkleRoll
#  15  RHipRoll        16 RHipPitch        17 RKneePitch    18 RAnklePitch  19 RAnkleRoll
#  20  HeadYaw         21 HeadPitch
#
# All angles are in radians.

POSES = {
    # ------------------------------------------------------------------ #
    # STAND – neutral upright position, arms relaxed at sides             #
    # ------------------------------------------------------------------ #
    "stand": {
        "description": "Stand upright with arms at sides",
        "angles": [
            1.57,  0.10, -0.05, -1.50,  0.00,   # L arm
            1.57, -0.10,  0.05,  1.50,  0.00,   # R arm
            0.00, -0.01,  0.00,  0.00,  0.00,   # L leg
            0.00, -0.01,  0.00,  0.00,  0.00,   # R leg
            0.00,  0.00,                          # head
        ],
    },

    # ------------------------------------------------------------------ #
    # T-POSE – arms stretched straight out to the sides                  #
    # ------------------------------------------------------------------ #
    "t_pose": {
        "description": "T-pose: arms spread straight out to the sides",
        "angles": [
            0.00,  1.30, -0.05, -1.50,  0.00,   # L arm (roll out)
            0.00, -1.30,  0.05,  1.50,  0.00,   # R arm (roll out)
            0.00, -0.01,  0.00,  0.00,  0.00,   # L leg
            0.00, -0.01,  0.00,  0.00,  0.00,   # R leg
            0.00,  0.00,                          # head
        ],
    },

    # ------------------------------------------------------------------ #
    # HANDS UP – both arms raised above the head                         #
    # ------------------------------------------------------------------ #
    "hands_up": {
        "description": "Raise both arms above the head",
        "angles": [
           -1.57,  0.20, -0.05, -1.50,  0.00,   # L arm (pitch back = up)
           -1.57, -0.20,  0.05,  1.50,  0.00,   # R arm
            0.00, -0.01,  0.00,  0.00,  0.00,   # L leg
            0.00, -0.01,  0.00,  0.00,  0.00,   # R leg
            0.00,  0.00,                          # head
        ],
    },

    # ------------------------------------------------------------------ #
    # SIT – sitting position                                              #
    # ------------------------------------------------------------------ #
    "sit": {
        "description": "Sit down with arms resting on knees",
        "angles": [
            1.20,  0.10, -0.05, -1.50,  0.00,   # L arm
            1.20, -0.10,  0.05,  1.50,  0.00,   # R arm
            0.00, -1.40,  2.10, -0.70,  0.00,   # L leg (hip+knee bent)
            0.00, -1.40,  2.10, -0.70,  0.00,   # R leg
            0.00,  0.00,                          # head
        ],
    },

    # ------------------------------------------------------------------ #
    # WAVE – right arm waving                                             #
    # ------------------------------------------------------------------ #
    "wave": {
        "description": "Wave with the right arm",
        "angles": [
            1.57,  0.10, -0.05, -1.50,  0.00,   # L arm (relaxed)
           -0.50, -0.30,  0.80,  1.50,  0.00,   # R arm raised + elbow bent
            0.00, -0.01,  0.00,  0.00,  0.00,   # L leg
            0.00, -0.01,  0.00,  0.00,  0.00,   # R leg
            0.00,  0.00,                          # head
        ],
    },

    # ------------------------------------------------------------------ #
    # BOW – head tilted down as a greeting bow                           #
    # ------------------------------------------------------------------ #
    "bow": {
        "description": "Bow by lowering the head",
        "angles": [
            1.57,  0.10, -0.05, -1.50,  0.00,   # L arm
            1.57, -0.10,  0.05,  1.50,  0.00,   # R arm
            0.00, -0.01,  0.00,  0.00,  0.00,   # L leg
            0.00, -0.01,  0.00,  0.00,  0.00,   # R leg
            0.00,  0.50,                          # head tilted down
        ],
    },

    # ------------------------------------------------------------------ #
    # CROUCH – slight squat                                               #
    # ------------------------------------------------------------------ #
    "crouch": {
        "description": "Crouch / partial squat",
        "angles": [
            1.40,  0.10, -0.05, -1.50,  0.00,   # L arm
            1.40, -0.10,  0.05,  1.50,  0.00,   # R arm
            0.00, -0.70,  1.50, -0.80,  0.00,   # L leg
            0.00, -0.70,  1.50, -0.80,  0.00,   # R leg
            0.00,  0.00,                          # head
        ],
    },

    # ------------------------------------------------------------------ #
    # POINT_RIGHT – right arm pointing to the right                      #
    # ------------------------------------------------------------------ #
    "point_right": {
        "description": "Point to the right with the right arm",
        "angles": [
            1.57,  0.10, -0.05, -1.50,  0.00,   # L arm relaxed
            0.00, -1.30,  0.05,  1.50,  0.00,   # R arm extended right
            0.00, -0.01,  0.00,  0.00,  0.00,   # L leg
            0.00, -0.01,  0.00,  0.00,  0.00,   # R leg
            0.00,  0.00,                          # head
        ],
    },

    # ------------------------------------------------------------------ #
    # POINT_LEFT – left arm pointing to the left                         #
    # ------------------------------------------------------------------ #
    "point_left": {
        "description": "Point to the left with the left arm",
        "angles": [
            0.00,  1.30, -0.05, -1.50,  0.00,   # L arm extended left
            1.57, -0.10,  0.05,  1.50,  0.00,   # R arm relaxed
            0.00, -0.01,  0.00,  0.00,  0.00,   # L leg
            0.00, -0.01,  0.00,  0.00,  0.00,   # R leg
            0.00,  0.00,                          # head
        ],
    },
}

# Aliases so the frontend can send natural language variants
ALIASES = {
    "arms_up":      "hands_up",
    "raise_hands":  "hands_up",
    "tpose":        "t_pose",
    "t-pose":       "t_pose",
    "sit_down":     "sit",
    "hello":        "wave",
    "greeting":     "bow",
    "squat":        "crouch",
}


def resolve(command: str):
    """Return (pose_name, pose_dict) for the given command string, or raise KeyError."""
    key = command.strip().lower().replace(" ", "_")
    key = ALIASES.get(key, key)
    if key not in POSES:
        raise KeyError(key)
    return key, POSES[key]


def list_commands():
    """Return a sorted list of all accepted command strings."""
    direct = sorted(POSES.keys())
    aliased = sorted(ALIASES.keys())
    return {"commands": direct, "aliases": aliased}
