#!/usr/bin/env python3
"""
arms_translator.py

Translator from MediaPipe 3D pose landmarks (x, y, z) to NAO joint angles
for the upper body (shoulders + elbows).

Expected landmarks format (per frame):
    {
        "Left shoulder":  {"x": ..., "y": ..., "z": ...},
        "Right shoulder": {"x": ..., "y": ..., "z": ...},
        "Left elbow":     {"x": ..., "y": ..., "z": ...},
        "Right elbow":    {"x": ..., "y": ..., "z": ...},
        "Left wrist":     {"x": ..., "y": ..., "z": ...},
        "Right wrist":    {"x": ..., "y": ..., "z": ...},
        ...
    }

Public API:
    - build_nao_angles(landmarks) -> dict
        Returns named joints + `angles` list in NAO order.
"""

import math
from typing import Dict, Any, Mapping

# =========================
# CONSTANTS
# =========================

NAO_MAX_SHOULDER_ROLL = 1.2  # radians

PITCH_MIN = -2.0  # arm up
PITCH_MAX = 1.6   # arm down


# =========================
# SHOULDER ROLL (3D)
# =========================

def compute_shoulder_roll(
    shoulder: Mapping[str, float],
    elbow: Mapping[str, float],
    side: str,
    lateral_threshold: float = 0.05,
) -> float:
    """
    Compute NAO ShoulderRoll from MediaPipe 3D landmarks.

    - Uses full 3D vector shoulder->elbow.
    - Base roll from 2D (x,y) deviation from vertical (down).
    - Attenuates roll when arm is mostly forward/back (big z, small x).
    - If lateral component is tiny, roll is 0.

    Args:
        shoulder: mapping with keys 'x', 'y', 'z'
        elbow: mapping with keys 'x', 'y', 'z'
        side: 'L' or 'R'
        lateral_threshold: min lateral component to generate roll

    Returns:
        float: roll angle in radians
                L: 0 .. +1.2
                R: 0 .. -1.2
    """
    dx = elbow["x"] - shoulder["x"]
    dy = elbow["y"] - shoulder["y"]
    dz = elbow["z"] - shoulder["z"]

    len_3d = math.sqrt(dx * dx + dy * dy + dz * dz)
    if len_3d == 0.0:
        return 0.0

    ux = dx / len_3d
    uy = dy / len_3d
    uz = dz / len_3d

    lateral_mag = abs(ux)  # left-right
    if lateral_mag < lateral_threshold:
        return 0.0

    len_xy = math.hypot(dx, dy)
    if len_xy == 0.0:
        return 0.0

    ux_xy = dx / len_xy
    uy_xy = dy / len_xy

    # torso direction: down in image (0, 1)
    tx, ty = 0.0, 1.0

    cos_theta = ux_xy * tx + uy_xy * ty
    cos_theta = max(-1.0, min(1.0, cos_theta))
    theta_2d = math.acos(cos_theta)  # 0 = down, pi/2 = sideways

    depth_mag = abs(uz)
    atten = lateral_mag / (lateral_mag + depth_mag + 1e-6)

    theta = theta_2d * atten
    theta = min(theta, NAO_MAX_SHOULDER_ROLL)

    if side == "L":
        return theta
    elif side == "R":
        return -theta
    else:
        raise ValueError("side must be 'L' or 'R'")


# =========================
# SHOULDER PITCH (2D)
# =========================

def compute_shoulder_pitch(
    shoulder: Mapping[str, float],
    elbow: Mapping[str, float],
) -> float:
    """
    Approximate NAO ShoulderPitch from MediaPipe 2D landmarks.

    Uses vertical component (y) of shoulder->elbow to map into [-2.0, 1.6].

    Args:
        shoulder: mapping with keys 'x', 'y'
        elbow: mapping with keys 'x', 'y'

    Returns:
        float: pitch angle in radians in [PITCH_MIN, PITCH_MAX]
    """
    dx = elbow["x"] - shoulder["x"]
    dy = elbow["y"] - shoulder["y"]

    length = math.hypot(dx, dy)
    if length == 0.0:
        return 0.0

    uy = dy / length
    uy = max(-1.0, min(1.0, uy))

    # uy =  1 -> +1.6 (down)
    # uy = -1 -> -2.0 (up)
    pitch = 1.8 * uy - 0.2
    pitch = max(PITCH_MIN, min(PITCH_MAX, pitch))

    return pitch


# =========================
# ELBOW ROLL (2D, DISCRETE)
# =========================

def compute_elbow_roll_2d(
    shoulder: Mapping[str, float],
    elbow: Mapping[str, float],
    wrist: Mapping[str, float],
    side: str,
    low_flex_deg: float = 10.0,
    high_flex_deg: float = 70.0,
    mid_nao_deg: float = 30.0,
    max_nao_deg: float = 88.5,
) -> float:
    """
    2D-only NAO ElbowRoll from MediaPipe landmarks.

    - Ignores z.
    - Uses angle between:
            v1 = shoulder -> elbow
            v2 = wrist    -> elbow
    - Converts to flexion:
            0°  = straight
            90° = clearly bent
    - Discrete mapping:
        flex <  low_flex_deg      -> mid_nao_deg
        low_flex_deg..high_flex   -> mid_nao_deg (30°)
        flex >= high_flex_deg     -> max_nao_deg (88.5°)

    Returns:
        float: radians
            L: negative
            R: positive
    """
    # v1: shoulder -> elbow
    v1x = elbow["x"] - shoulder["x"]
    v1y = elbow["y"] - shoulder["y"]

    # v2: wrist -> elbow
    v2x = elbow["x"] - wrist["x"]
    v2y = elbow["y"] - wrist["y"]

    len1 = math.hypot(v1x, v1y)
    len2 = math.hypot(v2x, v2y)
    if len1 == 0.0 or len2 == 0.0:
        return 0.0

    dot = v1x * v2x + v1y * v2y
    cos_theta = dot / (len1 * len2)
    cos_theta = max(-1.0, min(1.0, cos_theta))

    theta_rad = math.acos(cos_theta)
    theta_deg = math.degrees(theta_rad)

    # Flexion: 0 = straight, 90 = bent
    flex_deg = max(0.0, 180.0 - theta_deg)

    if flex_deg < low_flex_deg:
        nao_deg = mid_nao_deg
    elif flex_deg < high_flex_deg:
        nao_deg = mid_nao_deg  # 30°
    else:
        nao_deg = max_nao_deg  # 88.5°

    nao_rad = math.radians(nao_deg)

    if side == "L":
        return -nao_rad
    elif side == "R":
        return nao_rad
    else:
        raise ValueError("side must be 'L' or 'R'")


# =========================
# ELBOW YAW (FIXED)
# =========================

def compute_elbow_yaw(
    shoulder: Mapping[str, float],
    elbow: Mapping[str, float],
    wrist: Mapping[str, float],
    side: str,
    threshold: float = 0.05,
) -> float:
    """
    NAO ElbowYaw heuristic.

    Current behavior: always returns a fixed yaw per side
    (ignores landmarks and threshold).

    Returns:
        float: yaw in radians
    """
    if side == "L":
        return -1.3
    elif side == "R":
        return 1.3
    else:
        raise ValueError("side must be 'L' or 'R'")


# =========================
# BUILD NAO ANGLES ARRAY
# =========================

def build_nao_angles(landmarks: Mapping[str, Mapping[str, float]]) -> Dict[str, Any]:
    """
    Build a NAO joint-angle list from pose landmarks.

    Expected keys in `landmarks`:
        'Left shoulder', 'Right shoulder',
        'Left elbow',    'Right elbow',
        'Left wrist',    'Right wrist'

    Returns:
        dict with named joints + 'angles' list in this order:

            [LShoulderPitch, LShoulderRoll, LElbowRoll, LElbowYaw, LWristYaw,
            RShoulderPitch, RShoulderRoll, RElbowRoll, RElbowYaw, RWristYaw,
            LHipRoll, LHipPitch, LKneePitch, LAnklePitch, LAnkleRoll,
            RHipRoll, RHipPitch, RKneePitch, RAnklePitch, RAnkleRoll,
            HeadYaw, HeadPitch]
    """
    LS = landmarks["Left shoulder"]
    RS = landmarks["Right shoulder"]
    LE = landmarks["Left elbow"]
    RE = landmarks["Right elbow"]
    LW = landmarks["Left wrist"]
    RW = landmarks["Right wrist"]

    # shoulders
    LShoulderPitch = compute_shoulder_pitch(LS, LE)
    RShoulderPitch = compute_shoulder_pitch(RS, RE)
    LShoulderRoll = compute_shoulder_roll(LS, LE, side="L")
    RShoulderRoll = compute_shoulder_roll(RS, RE, side="R")

    # elbows
    LElbowRoll = compute_elbow_roll_2d(LS, LE, LW, side="L")
    RElbowRoll = compute_elbow_roll_2d(RS, RE, RW, side="R")
    LElbowYaw = compute_elbow_yaw(LS, LE, LW, side="L")
    RElbowYaw = compute_elbow_yaw(RS, RE, RW, side="R")

    angles = [
        LShoulderPitch,
        LShoulderRoll,
        LElbowRoll,
        LElbowYaw,
        0.0,  # LWristYaw

        RShoulderPitch,
        RShoulderRoll,
        RElbowRoll,
        RElbowYaw,
        0.0,  # RWristYaw

        0.0, 0.0, 0.0, 0.0, 0.0,  # left leg
        0.0, 0.0, 0.0, 0.0, 0.0,  # right leg

        0.0, 0.0,  # head yaw/pitch
    ]

    return {
        "LShoulderPitch": LShoulderPitch,
        "LShoulderRoll": LShoulderRoll,
        "LElbowRoll": LElbowRoll,
        "LElbowYaw": LElbowYaw,
        "RShoulderPitch": RShoulderPitch,
        "RShoulderRoll": RShoulderRoll,
        "RElbowRoll": RElbowRoll,
        "RElbowYaw": RElbowYaw,
        "angles": angles,
    }


# Optional: small helper alias if you want a shorter name in other services.
def translate_arms(landmarks: Mapping[str, Mapping[str, float]]) -> Dict[str, Any]:
    """
    Convenience wrapper around build_nao_angles.

    Args:
        landmarks: MediaPipe-style landmark dict for upper body.

    Returns:
        dict: same as build_nao_angles(...)
    """
    return build_nao_angles(landmarks)
