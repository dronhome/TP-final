"""
Unit tests for arms_translator.py — pure math, no network calls.
"""

import math
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from arms_translator import (
    compute_shoulder_pitch,
    compute_shoulder_roll,
    compute_elbow_roll_2d,
    compute_elbow_yaw,
    translate_arms,
)

# ---------------------------------------------------------------------------
# Fixtures — simple landmark positions
# ---------------------------------------------------------------------------

# Arm pointing straight down from shoulder
SHOULDER = {"x": 0.5, "y": 0.3, "z": 0.0}
ELBOW_DOWN = {"x": 0.5, "y": 0.5, "z": 0.0}   # directly below shoulder
ELBOW_UP = {"x": 0.5, "y": 0.1, "z": 0.0}      # directly above shoulder
ELBOW_SIDE = {"x": 0.7, "y": 0.3, "z": 0.0}    # directly to the side
WRIST_STRAIGHT = {"x": 0.5, "y": 0.7, "z": 0.0}  # straight arm (no bend)
WRIST_BENT = {"x": 0.5, "y": 0.3, "z": 0.0}      # wrist back at shoulder level (bent)

FULL_LANDMARKS = {
    "Left shoulder":  {"x": 0.60, "y": 0.40, "z": -0.30},
    "Right shoulder": {"x": 0.42, "y": 0.36, "z": -0.31},
    "Left elbow":     {"x": 0.62, "y": 0.53, "z": -0.24},
    "Right elbow":    {"x": 0.36, "y": 0.26, "z": -0.41},
    "Left wrist":     {"x": 0.61, "y": 0.63, "z": -0.28},
    "Right wrist":    {"x": 0.32, "y": 0.11, "z": -0.43},
}


# ---------------------------------------------------------------------------
# compute_shoulder_pitch
# ---------------------------------------------------------------------------

def test_pitch_arm_down():
    """Elbow below shoulder → positive pitch (arm hanging down)."""
    pitch = compute_shoulder_pitch(SHOULDER, ELBOW_DOWN)
    assert pitch > 0, f"Expected positive pitch for arm down, got {pitch}"


def test_pitch_arm_up():
    """Elbow above shoulder → negative pitch (arm raised up)."""
    pitch = compute_shoulder_pitch(SHOULDER, ELBOW_UP)
    assert pitch < 0, f"Expected negative pitch for arm up, got {pitch}"


def test_pitch_within_limits():
    """Pitch must always stay within NAO limits [-2.0, 1.6]."""
    for elbow in [ELBOW_DOWN, ELBOW_UP, ELBOW_SIDE]:
        pitch = compute_shoulder_pitch(SHOULDER, elbow)
        assert -2.0 <= pitch <= 1.6, f"Pitch {pitch} out of NAO limits"


def test_pitch_zero_length():
    """Elbow at same position as shoulder → pitch = 0."""
    pitch = compute_shoulder_pitch(SHOULDER, SHOULDER)
    assert pitch == 0.0


# ---------------------------------------------------------------------------
# compute_shoulder_roll
# ---------------------------------------------------------------------------

def test_roll_arm_down_no_lateral():
    """Arm straight down — no lateral movement → roll near 0."""
    roll = compute_shoulder_roll(SHOULDER, ELBOW_DOWN, side="L")
    assert abs(roll) < 0.1, f"Expected roll ~0 for arm down, got {roll}"


def test_roll_arm_sideways_left():
    """Arm out to the side → positive roll for L."""
    roll = compute_shoulder_roll(SHOULDER, ELBOW_SIDE, side="L")
    assert roll > 0, f"Expected positive roll for L arm sideways, got {roll}"


def test_roll_arm_sideways_right():
    """Arm out to the side → negative roll for R."""
    roll = compute_shoulder_roll(SHOULDER, ELBOW_SIDE, side="R")
    assert roll < 0, f"Expected negative roll for R arm sideways, got {roll}"


def test_roll_within_limits():
    """Roll must never exceed NAO_MAX_SHOULDER_ROLL (1.2)."""
    for side in ("L", "R"):
        roll = compute_shoulder_roll(SHOULDER, ELBOW_SIDE, side=side)
        assert abs(roll) <= 1.2, f"Roll {roll} exceeds NAO max for side {side}"


# ---------------------------------------------------------------------------
# compute_elbow_roll_2d
# ---------------------------------------------------------------------------

def test_elbow_roll_straight_arm():
    """Straight arm (wrist below elbow in line) → mid_nao_deg (30°)."""
    roll = compute_elbow_roll_2d(SHOULDER, ELBOW_DOWN, WRIST_STRAIGHT, side="L")
    expected = math.radians(30.0)
    assert abs(abs(roll) - expected) < 0.01, f"Expected ~30° for straight arm, got {math.degrees(abs(roll)):.1f}°"


def test_elbow_roll_bent_arm():
    """Bent arm → max_nao_deg (88.5°)."""
    roll = compute_elbow_roll_2d(SHOULDER, ELBOW_DOWN, WRIST_BENT, side="L")
    expected = math.radians(88.5)
    assert abs(abs(roll) - expected) < 0.01, f"Expected ~88.5° for bent arm, got {math.degrees(abs(roll)):.1f}°"


def test_elbow_roll_sign_left():
    """Left elbow roll must be negative."""
    roll = compute_elbow_roll_2d(SHOULDER, ELBOW_DOWN, WRIST_STRAIGHT, side="L")
    assert roll < 0, f"Expected negative roll for L, got {roll}"


def test_elbow_roll_sign_right():
    """Right elbow roll must be positive."""
    roll = compute_elbow_roll_2d(SHOULDER, ELBOW_DOWN, WRIST_STRAIGHT, side="R")
    assert roll > 0, f"Expected positive roll for R, got {roll}"


# ---------------------------------------------------------------------------
# compute_elbow_yaw
# ---------------------------------------------------------------------------

def test_elbow_yaw_left_fixed():
    """Left elbow yaw is always -1.3."""
    yaw = compute_elbow_yaw(SHOULDER, ELBOW_DOWN, WRIST_STRAIGHT, side="L")
    assert yaw == -1.3


def test_elbow_yaw_right_fixed():
    """Right elbow yaw is always +1.3."""
    yaw = compute_elbow_yaw(SHOULDER, ELBOW_DOWN, WRIST_STRAIGHT, side="R")
    assert yaw == 1.3


# ---------------------------------------------------------------------------
# translate_arms (full pipeline)
# ---------------------------------------------------------------------------

def test_translate_arms_returns_all_keys():
    """Result must contain all 8 named joints + angles list."""
    result = translate_arms(FULL_LANDMARKS)
    for key in ["LShoulderPitch", "LShoulderRoll", "LElbowRoll", "LElbowYaw",
                "RShoulderPitch", "RShoulderRoll", "RElbowRoll", "RElbowYaw", "angles"]:
        assert key in result, f"Missing key: {key}"


def test_translate_arms_angles_length():
    """Angles array must have exactly 22 elements."""
    result = translate_arms(FULL_LANDMARKS)
    assert len(result["angles"]) == 22, f"Expected 22 angles, got {len(result['angles'])}"


def test_translate_arms_elbow_yaw_values():
    """ElbowYaw values in angles array must be fixed -1.3 and +1.3."""
    result = translate_arms(FULL_LANDMARKS)
    angles = result["angles"]
    # LElbowYaw is index 3, RElbowYaw is index 8
    assert angles[3] == -1.3, f"LElbowYaw expected -1.3, got {angles[3]}"
    assert angles[8] == 1.3, f"RElbowYaw expected 1.3, got {angles[8]}"


def test_translate_arms_legs_and_head_are_zero():
    """All leg and head joints must be 0.0."""
    result = translate_arms(FULL_LANDMARKS)
    angles = result["angles"]
    for i in range(10, 22):
        assert angles[i] == 0.0, f"Expected 0.0 at index {i}, got {angles[i]}"


def test_translate_arms_missing_landmark():
    """Missing required landmark must raise KeyError."""
    bad = dict(FULL_LANDMARKS)
    del bad["Left elbow"]
    try:
        translate_arms(bad)
        assert False, "Expected KeyError"
    except KeyError:
        pass
