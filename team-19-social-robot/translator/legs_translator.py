import numpy as np


REQUIRED_LANDMARKS = [
    "Left shoulder",
    "Right shoulder",
    "Left hip",
    "Right hip",
    "Left knee",
    "Right knee",
    "Left ankle",
    "Right ankle",
]


STANDING_POSE = [
    0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.1130, 0.1217,
    -0.0844, 0.0786, -0.1017, -0.1130, 0.1217, -0.0844, 0.0786, 0.1017, 0.0, 0.0,
]

SQUAT_POSE = [
    0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.1, -0.795,
    1.275, -0.33, -0.13, -0.1, -0.795, 1.275, -0.33, 0.13, 0.0, 0.0,
]

SIT_POSE = [
    0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, -1.10, 1.15,
    -0.02, 0.0, 0.0, -1.10, 1.15, -0.02, 0.0, 0.0, 0.0,
]

RIGHT_LEG_SHIFT = [
    1.40689, 0.300092, -1.00483, -1.38659, -0.00498221, 1.39967, -0.306888,
    1.00634, 1.39279, 0.00395609, -0.331613, -0.453016, 0.707806, -0.350534,
    0.331613, -0.331613, -0.455269, 0.703364, -0.351562, 0.331613, -0.00362528, 0.00196421,
]

RIGHT_LEG_UP = [
    1.40689, 1.3264502315, 1.3264502315, -1.38659, -0.00498221, 1.39967,
    -0.306888, 1.00634, 1.39279, 0.00395609, -0.331613, -0.453016, 0.707806,
    -0.350534, 0.331613, -0.331613, -0.8, 1.4, -0.65, 0.331613, -0.00362528, 0.00196421,
]

LEFT_LEG_SHIFT = [
    1.43965, 0.217452, -0.423197, -1.20175, 0.109774, 1.45207, -0.22412,
    0.42319, 1.20175, 0.0989953, 0.331613, 0.123171, -0.0872552, 0.0866826,
    -0.331613, 0.331613, 0.123172, -0.0872552, 0.0866825, -0.331613, 0.0, -0.160616,
]

LEFT_LEG_UP = [
    1.43965, 0.217452, -0.423197, -1.20175, 0.109774, 1.45207,
    -1.3264502315, -1.3264502315, 1.20175, 0.0989953, 0.331613, -0.8,
    1.4, -0.65, -0.331613, 0.331613, 0.123172, -0.0872552, 0.0866825,
    -0.331613, 0.0, -0.160616,
]


POSE_OUTPUTS = {
    "standing": {
        "pose": "STANDING_POSE",
        "angles": STANDING_POSE,
        "arm_mode": "merge_from_arms_translator",
    },
    "squatting": {
        "pose": "SQUAT_POSE",
        "angles": SQUAT_POSE,
        "arm_mode": "merge_from_arms_translator",
    },
    "sitting": {
        "pose": "SIT_POSE",
        "angles": SIT_POSE,
        "arm_mode": "merge_from_arms_translator",
    },
    "lifted_right_leg": {
        "pose": "RIGHT_LEG_UP",
        "angles": RIGHT_LEG_UP,
        "arm_mode": "use_fixed_pose_arms",
    },
    "lifted_left_leg": {
        "pose": "LEFT_LEG_UP",
        "angles": LEFT_LEG_UP,
        "arm_mode": "use_fixed_pose_arms",
    },
}

POSE_TRANSITIONS = {
    "RIGHT_LEG_UP": RIGHT_LEG_SHIFT,
    "LEFT_LEG_UP": LEFT_LEG_SHIFT,
}

SHIFT_POSE_NAMES = {
    "RIGHT_LEG_UP": "RIGHT_LEG_SHIFT",
    "LEFT_LEG_UP": "LEFT_LEG_SHIFT",
}


CLASS_PROTOTYPES = {
    "standing": {
        "knee_angle": 138.0,
        "hip_angle": 143.0,
        "ankle_angle": 50.0,
        "hip_above_knee": 0.74,
        "knee_z_offset": -0.18,
        "body_span": 2.47,
        "shin_tilt": 90.0,
        "hip_to_ankle_y": 1.47,
        "knee_depth_vs_hip": -0.05,
        "hip_over_foot_x": 0.03,
        "knee_over_foot_x": 0.06,
        "torso_vertical_offset": 2.0,
    },
    "squatting": {
        "knee_angle": 70.0,
        "hip_angle": 78.0,
        "ankle_angle": 38.0,
        "hip_above_knee": 0.26,
        "knee_z_offset": -0.16,
        "body_span": 2.12,
        "shin_tilt": 92.0,
        "hip_to_ankle_y": 1.08,
        "knee_depth_vs_hip": -0.24,
        "hip_over_foot_x": 0.06,
        "knee_over_foot_x": 0.11,
        "torso_vertical_offset": 8.0,
    },
    "sitting": {
        "knee_angle": 92.0,
        "hip_angle": 103.0,
        "ankle_angle": 20.0,
        "hip_above_knee": 0.31,
        "knee_z_offset": -0.07,
        "body_span": 2.36,
        "shin_tilt": 93.0,
        "hip_to_ankle_y": 1.38,
        "knee_depth_vs_hip": -0.16,
        "hip_over_foot_x": 0.11,
        "knee_over_foot_x": 0.07,
        "torso_vertical_offset": 2.0,
    },
}


FEATURE_SCALES = {
    "knee_angle": 30.0,
    "hip_angle": 28.0,
    "ankle_angle": 16.0,
    "hip_above_knee": 0.16,
    "knee_z_offset": 0.06,
    "body_span": 0.20,
    "shin_tilt": 8.0,
    "hip_to_ankle_y": 0.18,
    "knee_depth_vs_hip": 0.10,
    "hip_over_foot_x": 0.06,
    "knee_over_foot_x": 0.05,
    "torso_vertical_offset": 5.0,
}


FEATURE_WEIGHTS = {
    "knee_angle": 1.8,
    "hip_angle": 1.8,
    "ankle_angle": 1.2,
    "hip_above_knee": 2.2,
    "knee_z_offset": 1.6,
    "body_span": 1.0,
    "shin_tilt": 1.0,
    "hip_to_ankle_y": 1.0,
    "knee_depth_vs_hip": 1.3,
    "hip_over_foot_x": 1.2,
    "knee_over_foot_x": 1.0,
    "torso_vertical_offset": 1.0,
}


def _has_leg_landmarks(landmarks):
    return all(k in landmarks for k in REQUIRED_LANDMARKS)


def validate_landmarks(landmarks):
    if not isinstance(landmarks, dict):
        raise ValueError("Landmarks must be a dictionary.")
    missing = [name for name in REQUIRED_LANDMARKS if name not in landmarks]
    if missing:
        raise ValueError(f"Missing required landmarks: {', '.join(missing)}")


def point_average(left_point, right_point):
    return {
        axis: (left_point[axis] + right_point[axis]) / 2.0
        for axis in ("x", "y", "z")
    }


def vertical_reference(point):
    return {"x": point["x"], "y": point["y"] - 1.0, "z": point["z"]}


def angle_at_joint(a, joint, b):
    v1 = np.array([a["x"] - joint["x"], a["y"] - joint["y"], a["z"] - joint["z"]])
    v2 = np.array([b["x"] - joint["x"], b["y"] - joint["y"], b["z"] - joint["z"]])
    denom = np.linalg.norm(v1) * np.linalg.norm(v2)
    if denom < 1e-9:
        return 180.0
    cos_angle = np.dot(v1, v2) / denom
    return float(np.degrees(np.arccos(np.clip(cos_angle, -1.0, 1.0))))


def segment_tilt_deg(start, end):
    return float(np.degrees(np.arctan2(end["y"] - start["y"], end["x"] - start["x"])))


def get_features(landmarks):
    validate_landmarks(landmarks)

    left_knee_angle = angle_at_joint(landmarks["Left hip"], landmarks["Left knee"], landmarks["Left ankle"])
    right_knee_angle = angle_at_joint(landmarks["Right hip"], landmarks["Right knee"], landmarks["Right ankle"])
    knee_angle = (left_knee_angle + right_knee_angle) / 2
    knee_angle_delta = abs(left_knee_angle - right_knee_angle)
    max_knee_angle = max(left_knee_angle, right_knee_angle)

    left_hip_angle = angle_at_joint(landmarks["Left shoulder"], landmarks["Left hip"], landmarks["Left knee"])
    right_hip_angle = angle_at_joint(landmarks["Right shoulder"], landmarks["Right hip"], landmarks["Right knee"])
    hip_angle = (left_hip_angle + right_hip_angle) / 2
    hip_angle_delta = abs(left_hip_angle - right_hip_angle)
    max_hip_angle = max(left_hip_angle, right_hip_angle)

    left_ankle_angle = angle_at_joint(landmarks["Left knee"], landmarks["Left ankle"], vertical_reference(landmarks["Left ankle"]))
    right_ankle_angle = angle_at_joint(landmarks["Right knee"], landmarks["Right ankle"], vertical_reference(landmarks["Right ankle"]))
    ankle_angle = (left_ankle_angle + right_ankle_angle) / 2

    left_shoulder_hip_dist = landmarks["Left hip"]["y"] - landmarks["Left shoulder"]["y"]
    right_shoulder_hip_dist = landmarks["Right hip"]["y"] - landmarks["Right shoulder"]["y"]
    torso_len = ((left_shoulder_hip_dist + right_shoulder_hip_dist) / 2.0) + 1e-6

    hip_above_knee = (
        (landmarks["Left knee"]["y"] - landmarks["Left hip"]["y"]) / torso_len
        + (landmarks["Right knee"]["y"] - landmarks["Right hip"]["y"]) / torso_len
    ) / 2.0

    knee_z_offset = (
        landmarks["Left knee"]["z"] - landmarks["Left ankle"]["z"]
        + landmarks["Right knee"]["z"] - landmarks["Right ankle"]["z"]
    ) / 2.0

    body_span = (
        (landmarks["Left ankle"]["y"] - landmarks["Left shoulder"]["y"]) / torso_len
        + (landmarks["Right ankle"]["y"] - landmarks["Right shoulder"]["y"]) / torso_len
    ) / 2.0

    left_shin_tilt = segment_tilt_deg(landmarks["Left knee"], landmarks["Left ankle"])
    right_shin_tilt = segment_tilt_deg(landmarks["Right knee"], landmarks["Right ankle"])
    shin_tilt = (left_shin_tilt + right_shin_tilt) / 2.0

    left_torso_tilt = segment_tilt_deg(landmarks["Left hip"], landmarks["Left shoulder"])
    right_torso_tilt = segment_tilt_deg(landmarks["Right hip"], landmarks["Right shoulder"])
    torso_tilt = (left_torso_tilt + right_torso_tilt) / 2.0

    hip_center = point_average(landmarks["Left hip"], landmarks["Right hip"])
    knee_center = point_average(landmarks["Left knee"], landmarks["Right knee"])
    ankle_center = point_average(landmarks["Left ankle"], landmarks["Right ankle"])
    shoulder_center = point_average(landmarks["Left shoulder"], landmarks["Right shoulder"])

    hip_to_ankle_y = abs(ankle_center["y"] - hip_center["y"]) / torso_len
    torso_lean_x = abs(shoulder_center["x"] - hip_center["x"]) / torso_len
    knee_depth_vs_hip = knee_center["z"] - hip_center["z"]
    knee_over_foot_x = abs(knee_center["x"] - ankle_center["x"]) / torso_len
    hip_over_foot_x = abs(hip_center["x"] - ankle_center["x"]) / torso_len
    torso_vertical_offset = abs(90.0 - abs(torso_tilt))
    ankle_height_delta = (landmarks["Right ankle"]["y"] - landmarks["Left ankle"]["y"]) / torso_len

    return {
        "knee_angle": knee_angle,
        "knee_angle_delta": knee_angle_delta,
        "max_knee_angle": max_knee_angle,
        "hip_angle": hip_angle,
        "hip_angle_delta": hip_angle_delta,
        "max_hip_angle": max_hip_angle,
        "ankle_angle": ankle_angle,
        "hip_above_knee": hip_above_knee,
        "knee_z_offset": knee_z_offset,
        "body_span": body_span,
        "shin_tilt": shin_tilt,
        "torso_tilt": torso_tilt,
        "hip_to_ankle_y": hip_to_ankle_y,
        "torso_lean_x": torso_lean_x,
        "knee_depth_vs_hip": knee_depth_vs_hip,
        "knee_over_foot_x": knee_over_foot_x,
        "hip_over_foot_x": hip_over_foot_x,
        "torso_vertical_offset": torso_vertical_offset,
        "ankle_height_delta": ankle_height_delta,
    }


def prototype_distance(features, class_name):
    prototype = CLASS_PROTOTYPES[class_name]
    distance = 0.0
    for key, center in prototype.items():
        scale = FEATURE_SCALES[key]
        weight = FEATURE_WEIGHTS[key]
        distance += weight * ((features[key] - center) / scale) ** 2
    return distance


def get_biased_distances(features):
    knee_angle = features["knee_angle"]
    knee_angle_delta = features["knee_angle_delta"]
    max_knee_angle = features["max_knee_angle"]
    hip_angle = features["hip_angle"]
    hip_angle_delta = features["hip_angle_delta"]
    max_hip_angle = features["max_hip_angle"]
    ankle_angle = features["ankle_angle"]
    hip_ratio = features["hip_above_knee"]
    knee_z = features["knee_z_offset"]
    body_span = features["body_span"]
    shin_tilt = features["shin_tilt"]
    hip_to_ankle_y = features["hip_to_ankle_y"]
    knee_depth_vs_hip = features["knee_depth_vs_hip"]
    knee_over_foot_x = features["knee_over_foot_x"]
    hip_over_foot_x = features["hip_over_foot_x"]
    torso_lean_x = features["torso_lean_x"]
    torso_vertical_offset = features["torso_vertical_offset"]
    ankle_height_delta = features["ankle_height_delta"]

    distances = {label: prototype_distance(features, label) for label in CLASS_PROTOTYPES}

    if hip_ratio >= 0.68 and body_span >= 2.30 and knee_angle >= 105:
        distances["standing"] *= 0.75

    if (
        knee_angle_delta >= 35.0
        and hip_angle_delta >= 30.0
        and abs(ankle_height_delta) >= 0.35
        and (max_knee_angle >= 120.0 or max_hip_angle >= 145.0)
    ):
        distances["standing"] *= 0.55
        distances["squatting"] *= 1.35
        distances["sitting"] *= 1.35

    if hip_ratio <= 0.42 and (knee_z <= -0.10 or ankle_angle >= 30 or knee_depth_vs_hip <= -0.22):
        distances["squatting"] *= 0.75

    if (
        hip_ratio <= 0.38
        and hip_to_ankle_y >= 1.18
        and ankle_angle <= 30
        and knee_z >= -0.10
        and knee_over_foot_x <= 0.08
        and torso_vertical_offset <= 5.0
    ):
        distances["sitting"] *= 0.75

    if hip_over_foot_x <= 0.08 and knee_over_foot_x >= 0.10 and (torso_lean_x >= 0.14 or torso_vertical_offset >= 8.0):
        distances["squatting"] *= 0.80

    return distances


def classify_pose(landmarks):
    features = get_features(landmarks)

    knee_angle = features["knee_angle"]
    knee_angle_delta = features["knee_angle_delta"]
    max_knee_angle = features["max_knee_angle"]
    hip_angle = features["hip_angle"]
    hip_angle_delta = features["hip_angle_delta"]
    max_hip_angle = features["max_hip_angle"]
    ankle_angle = features["ankle_angle"]
    hip_ratio = features["hip_above_knee"]
    knee_z = features["knee_z_offset"]
    body_span = features["body_span"]
    shin_tilt = features["shin_tilt"]
    hip_to_ankle_y = features["hip_to_ankle_y"]
    knee_depth_vs_hip = features["knee_depth_vs_hip"]
    torso_lean_x = features["torso_lean_x"]
    knee_over_foot_x = features["knee_over_foot_x"]
    hip_over_foot_x = features["hip_over_foot_x"]
    torso_vertical_offset = features["torso_vertical_offset"]
    ankle_height_delta = features["ankle_height_delta"]

    if (
        abs(ankle_height_delta) >= 0.30
        and hip_ratio >= 0.60
        and max_knee_angle >= 165.0
        and hip_to_ankle_y >= 1.12
        and body_span >= 2.10
    ):
        if ankle_height_delta > 0:
            return "lifted_left_leg", features
        return "lifted_right_leg", features

    if (
        knee_angle_delta >= 35.0
        and hip_angle_delta >= 30.0
        and abs(ankle_height_delta) >= 0.35
        and (max_knee_angle >= 120.0 or max_hip_angle >= 145.0)
    ):
        if ankle_height_delta >= 0.35:
            return "lifted_left_leg", features
        return "lifted_right_leg", features

    if hip_ratio >= 0.64 and body_span >= 2.28 and hip_to_ankle_y >= 1.30 and hip_angle >= 100:
        return "standing", features

    if hip_ratio <= 0.38:
        if (
            hip_to_ankle_y < 1.16
            or ankle_angle >= 34
            or (knee_angle <= 62 and hip_angle <= 78)
            or (knee_depth_vs_hip <= -0.22 and torso_vertical_offset >= 6.0)
        ):
            return "squatting", features
        if hip_to_ankle_y >= 1.35 and ankle_angle <= 20 and knee_z >= -0.08:
            return "sitting", features
        if (
            torso_lean_x <= 0.04
            and knee_over_foot_x <= 0.08
            and hip_over_foot_x <= 0.04
            and torso_vertical_offset <= 5.0
            and knee_angle_delta <= 35.0
            and hip_angle_delta <= 30.0
        ):
            return "sitting", features
        return "sitting", features

    if hip_ratio <= 0.52 and hip_to_ankle_y < 1.15:
        return "squatting", features

    if hip_ratio <= 0.45 and knee_depth_vs_hip <= -0.22 and (torso_vertical_offset >= 6.0 or knee_over_foot_x >= 0.10):
        return "squatting", features

    if hip_ratio <= 0.45 and torso_lean_x >= 0.14 and knee_over_foot_x >= 0.10 and hip_over_foot_x <= 0.10:
        return "squatting", features

    if knee_angle <= 82 and (knee_z <= -0.09 or ankle_angle >= 28 or hip_angle <= 95 or knee_depth_vs_hip <= -0.20):
        return "squatting", features

    if (
        hip_ratio <= 0.38
        and hip_to_ankle_y >= 1.24
        and knee_z >= -0.10
        and ankle_angle <= 30
        and hip_angle >= 85
        and knee_angle <= 95
        and 84 <= shin_tilt <= 100
        and torso_lean_x <= 0.10
        and knee_over_foot_x <= 0.08
        and torso_vertical_offset <= 5.0
        and knee_angle_delta <= 35.0
        and hip_angle_delta <= 30.0
    ):
        return "sitting", features

    if hip_ratio >= 0.55 and hip_to_ankle_y >= 1.25 and hip_angle >= 115:
        return "standing", features

    if hip_ratio >= 0.40 and hip_to_ankle_y >= 1.20 and knee_angle >= 95 and hip_angle >= 120 and ankle_angle <= 25:
        return "standing", features

    distances = get_biased_distances(features)
    best_label = min(distances, key=distances.get)
    return best_label, features


def build_pose_output(state):
    if state not in POSE_OUTPUTS:
        raise ValueError(f"Unsupported pose state for output: {state}")
    pose_output = POSE_OUTPUTS[state]
    return {
        "pose": pose_output["pose"],
        "angles": list(pose_output["angles"]),
        "arm_mode": pose_output["arm_mode"],
    }


def normalize_pose_name(pose_name):
    pose_aliases = {
        None: None,
        "standing": "STANDING_POSE",
        "squatting": "SQUAT_POSE",
        "sitting": "SIT_POSE",
        "lifted_right_leg": "RIGHT_LEG_UP",
        "lifted_left_leg": "LEFT_LEG_UP",
        "STANDING_POSE": "STANDING_POSE",
        "SQUAT_POSE": "SQUAT_POSE",
        "SIT_POSE": "SIT_POSE",
        "RIGHT_LEG_UP": "RIGHT_LEG_UP",
        "LEFT_LEG_UP": "LEFT_LEG_UP",
        "RIGHT_LEG_SHIFT": "RIGHT_LEG_SHIFT",
        "LEFT_LEG_SHIFT": "LEFT_LEG_SHIFT",
    }
    if pose_name not in pose_aliases:
        raise ValueError(f"Unsupported previous pose: {pose_name}")
    return pose_aliases[pose_name]


def translate_legs(landmarks):
    state, _features = classify_pose(landmarks)
    return build_pose_output(state)


def translate_legs_with_transition(landmarks, previous_pose=None):
    pose_output = translate_legs(landmarks)
    normalized_previous = normalize_pose_name(previous_pose)
    current_pose = pose_output["pose"]

    if current_pose in POSE_TRANSITIONS and normalized_previous != current_pose:
        shift_output = {
            "pose": SHIFT_POSE_NAMES[current_pose],
            "angles": list(POSE_TRANSITIONS[current_pose]),
            "arm_mode": pose_output["arm_mode"],
        }
        return [shift_output, pose_output]

    return [pose_output]


def merge_with_arm_angles(arm_angles, leg_step):
    merged = list(leg_step["angles"])
    if leg_step["arm_mode"] == "merge_from_arms_translator":
        merged[0:10] = arm_angles[0:10]
    return merged
