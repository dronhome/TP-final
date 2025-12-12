#!/usr/bin/env python3
"""
nao_pose_service.py

Flask microservice that:
    - /arms/from_image: accept a single image, compute pose, send to NAO.
    - /arms/from_video: accept a video, split into frames via pose_from_video,
                        filter incomplete frames, send each valid pose to NAO,
                        save debug frame images.
"""

import os
import uuid

from flask import Flask, request, jsonify
import requests

from arms_translator import translate_arms
from video_pose_processor import process_video_bytes

# =========================
# CONFIG
# =========================

POSE_API_URL = "http://skeletonFinderAPI:6001/media_pipe_pose/pose_from_image"
SET_POSE_URL = "http://naoRobotAPI:5000/setting_pose/setPose"

# Host directory mounted into pose container as /images
POSE_HOST_ROOT = "/home/ubuntu/Pictures"      # host/VM path
POSE_CONT_ROOT = "/images"                    # container path

# Subdir for single-image uploads (used by /arms/from_image)
UPLOAD_SUBDIR = "nao_pose_uploads"
UPLOAD_DIR = os.path.join(POSE_HOST_ROOT, UPLOAD_SUBDIR)
os.makedirs(UPLOAD_DIR, exist_ok=True)

# Root dir for video debug frames (host only; not used by pose container)
VIDEO_FRAMES_ROOT = os.path.join(POSE_HOST_ROOT, "nao_video_frames")
os.makedirs(VIDEO_FRAMES_ROOT, exist_ok=True)

app = Flask(__name__)


# =========================
# HELPERS
# =========================

def call_pose_service(container_path: str):
    """
    Call the MediaPipe pose_from_image API with a file path
    (as seen inside the pose container) and return landmarks.
    """
    params = {"file_location": container_path}
    resp = requests.get(POSE_API_URL, params=params, timeout=15)
    resp.raise_for_status()
    data = resp.json()

    required_joints = [
        "Left shoulder",
        "Right shoulder",
        "Left elbow",
        "Right elbow",
        "Left wrist",
        "Right wrist",
    ]
    required_coords = ["x", "y", "z"]

    for joint in required_joints:
        if joint not in data:
            raise KeyError(f"Missing landmark: {joint}")
        for c in required_coords:
            if c not in data[joint]:
                raise KeyError(f"Missing coordinate '{c}' for {joint}")

    return data


def call_nao_set_pose(angles):
    """
    Call NAO pose endpoint with the given angles.
    """
    payload = {"angles": angles}
    resp = requests.post(SET_POSE_URL, json=payload, timeout=15)
    resp.raise_for_status()
    return resp.json()


# =========================
# ROUTES
# =========================

@app.route("/arms/from_image", methods=["POST"])
def arms_from_image():
    """
    Accept an image, compute NAO arm pose, and send it to NAO.

    Request:
        multipart/form-data
        image: file

    Response:
        200 JSON with angles, joint values, debug paths
        4xx/5xx error JSON otherwise
    """
    if "image" not in request.files:
        return jsonify({"error": "image file is required (multipart/form-data, field 'image')"}), 400

    file = request.files["image"]
    if file.filename == "":
        return jsonify({"error": "empty filename"}), 400

    # Save file on host in /home/noetic/Pictures/nao_pose_uploads
    ext = os.path.splitext(file.filename)[1] or ".jpg"
    tmp_name = f"{uuid.uuid4().hex}{ext}"
    host_path = os.path.join(UPLOAD_DIR, tmp_name)

    try:
        file.save(host_path)
    except Exception as e:
        return jsonify({"error": "failed to save uploaded file", "detail": str(e)}), 500

    # Path as seen inside the pose container
    container_path = os.path.join(POSE_CONT_ROOT, UPLOAD_SUBDIR, tmp_name)

    # 1) Pose estimation
    try:
        landmarks = call_pose_service(container_path)
    except requests.RequestException as e:
        return jsonify({
            "error": "failed to call pose service",
            "detail": str(e),
            "file_location_pose_container": container_path,
            "file_location_host": host_path,
        }), 502
    except KeyError as e:
        return jsonify({
            "error": "pose not detected or incomplete (missing landmarks)",
            "detail": str(e),
            "file_location_pose_container": container_path,
            "file_location_host": host_path,
        }), 422

    # 2) Translate landmarks -> NAO angles
    try:
        result = translate_arms(landmarks)
        angles = result["angles"]
    except Exception as e:
        return jsonify({
            "error": "failed to translate landmarks to NAO angles",
            "detail": str(e),
        }), 500

    # Optional: treat all-zero as "no useful pose"
    if all(abs(a) < 1e-4 for a in angles):
        return jsonify({
            "error": "image did not produce usable NAO angles (all ~0)",
        }), 422

    # 3) Send to NAO
    try:
        nao_response = call_nao_set_pose(angles)
    except requests.RequestException as e:
        return jsonify({
            "error": "failed to send pose to NAO",
            "detail": str(e),
        }), 502

    joint_keys = [
        "LShoulderPitch",
        "LShoulderRoll",
        "LElbowRoll",
        "LElbowYaw",
        "RShoulderPitch",
        "RShoulderRoll",
        "RElbowRoll",
        "RElbowYaw",
    ]

    return jsonify({
        "file_location_host": host_path,
        "file_location_pose_container": container_path,
        "nao_angles": [float(a) for a in angles],
        "joint_values": {k: float(result[k]) for k in joint_keys},
        "nao_response": nao_response,
    })


@app.route("/arms/from_video", methods=["POST"])
def arms_from_video():
    """
    Accept a video, split into frames via pose_from_video, filter incomplete
    frames, send each valid pose to NAO, and save debug frame images.

    Request:
      multipart/form-data
        video: file
      optional form fields:
        fps: int (default 1)
        seconds: int (default -1, process full video)

    Response:
      200 JSON summary with counts and debug paths
      4xx/5xx JSON on error
    """
    if "video" not in request.files:
        return jsonify({"error": "video file is required (multipart/form-data, field 'video')"}), 400

    file = request.files["video"]
    if file.filename == "":
        return jsonify({"error": "empty filename"}), 400

    # Optional controls
    try:
        fps = int(request.form.get("fps", "1"))
    except ValueError:
        return jsonify({"error": "fps must be an integer"}), 400

    try:
        seconds = int(request.form.get("seconds", "-1"))
    except ValueError:
        return jsonify({"error": "seconds must be an integer"}), 400

    # Read video bytes (not necessarily saving the original file)
    try:
        video_bytes = file.read()
    except Exception as e:
        return jsonify({"error": "failed to read uploaded video", "detail": str(e)}), 500

    # Each upload gets its own debug frame folder
    upload_id = uuid.uuid4().hex
    output_dir = os.path.join(VIDEO_FRAMES_ROOT, upload_id)
    os.makedirs(output_dir, exist_ok=True)

    # 1) Process video via pose_from_video → frames + debug images
    try:
        summary = process_video_bytes(
            video_bytes=video_bytes,
            output_dir=output_dir,
            number_frames_per_sec=fps,
            number_seconds_to_process=seconds,
            attach_visualization=True,
        )
    except requests.RequestException as e:
        return jsonify({
            "error": "failed to call pose_from_video service",
            "detail": str(e),
        }), 502
    except Exception as e:
        return jsonify({
            "error": "failed to process video",
            "detail": str(e),
        }), 500

    if summary["valid_frames"] == 0:
        return jsonify({
            "error": "no valid frames with complete landmarks in video",
            "total_frames": summary["total_frames"],
            "output_dir": output_dir,
            "invalid_image_paths": summary["invalid_image_paths"],
        }), 422

    # 2) For each valid frame, translate landmarks -> NAO angles and send to NAO
    nao_results = []
    for idx, landmarks in enumerate(summary["valid_landmarks"]):
        try:
            result = translate_arms(landmarks)
            angles = result["angles"]
        except Exception as e:
            return jsonify({
                "error": "failed to translate landmarks to NAO angles for a frame",
                "detail": str(e),
                "frame_index_in_valid_list": idx,
            }), 500

        # Send to NAO
        try:
            nao_response = call_nao_set_pose(angles)
        except requests.RequestException as e:
            return jsonify({
                "error": "failed to send pose to NAO for a frame",
                "detail": str(e),
                "frame_index_in_valid_list": idx,
            }), 502

        # Collect a minimal per-frame summary (avoid huge payload)
        nao_results.append({
            "frame_valid_index": idx,
            "nao_response": nao_response,
        })

    # 3) Final summary
    return jsonify({
        "upload_id": upload_id,
        "output_dir": output_dir,
        "total_frames": summary["total_frames"],
        "valid_frames": summary["valid_frames"],
        "invalid_frames": summary["invalid_frames"],
        "valid_image_paths": summary["valid_image_paths"],
        "invalid_image_paths": summary["invalid_image_paths"],
        "landmarks_valid_json": summary["landmarks_valid_json"],
        "landmarks_all_json": summary["landmarks_all_json"],
        "nao_results": nao_results,
    })


# =========================
# ENTRY POINT
# =========================

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=7000, debug=True)
