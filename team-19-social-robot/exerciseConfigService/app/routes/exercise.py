import os
import json
from flask import Blueprint, request, jsonify

from app.storage import (
    exercise_exists,
    create_exercise,
    get_exercise,
    list_exercises,
    delete_exercise,
    update_config,
    update_sequence,
    get_frames,
    get_frame,
    update_frame,
    add_frame,
    delete_frame,
)

exercise_bp = Blueprint("exercise", __name__, url_prefix="/exercise")


# ---------------------------------------------------------------------------
# POST /exercise/create
# Accepts either:
#   a) application/json:
#      {"name": "Arm Wave", "frames": [...], "pose_engine": "mediapipe"}
#
#   b) multipart/form-data:
#      name        — string
#      frames      — JSON string
#      pose_engine — string (optional)
#      media       — file (optional)
# ---------------------------------------------------------------------------
@exercise_bp.route("/create", methods=["POST"])
def create():
    if request.content_type and "multipart/form-data" in request.content_type:
        name = request.form.get("name")
        frames_raw = request.form.get("frames")
        pose_engine = request.form.get("pose_engine", "mediapipe")

        if not name:
            return jsonify({"error": "'name' is required"}), 400
        if not frames_raw:
            return jsonify({"error": "'frames' is required"}), 400
        try:
            frames = json.loads(frames_raw)
        except json.JSONDecodeError:
            return jsonify({"error": "'frames' must be valid JSON"}), 400

        media_bytes = None
        media_ext = ".bin"
        if "media" in request.files:
            f = request.files["media"]
            media_bytes = f.read()
            _, media_ext = os.path.splitext(f.filename)
            if not media_ext:
                media_ext = ".bin"
    else:
        data = request.get_json(silent=True)
        if not data:
            return jsonify({"error": "JSON body or multipart/form-data required"}), 400
        name = data.get("name")
        frames = data.get("frames")
        pose_engine = data.get("pose_engine", "mediapipe")
        media_bytes = None
        media_ext = ".bin"

    if not name:
        return jsonify({"error": "'name' is required"}), 400
    if not isinstance(frames, list) or len(frames) == 0:
        return jsonify({"error": "'frames' must be a non-empty list"}), 400

    config = create_exercise(
        name=name,
        frames=frames,
        pose_engine=pose_engine,
        media_bytes=media_bytes,
        media_ext=media_ext,
    )
    return jsonify(config), 201


# ---------------------------------------------------------------------------
# GET /exercise/list
# ---------------------------------------------------------------------------
@exercise_bp.route("/list", methods=["GET"])
def list_all():
    return jsonify(list_exercises()), 200


# ---------------------------------------------------------------------------
# GET /exercise/<id>
# ---------------------------------------------------------------------------
@exercise_bp.route("/<exercise_id>", methods=["GET"])
def get(exercise_id):
    if not exercise_exists(exercise_id):
        return jsonify({"error": f"Exercise '{exercise_id}' not found"}), 404
    return jsonify(get_exercise(exercise_id)), 200


# ---------------------------------------------------------------------------
# DELETE /exercise/<id>
# ---------------------------------------------------------------------------
@exercise_bp.route("/<exercise_id>", methods=["DELETE"])
def delete(exercise_id):
    if not exercise_exists(exercise_id):
        return jsonify({"error": f"Exercise '{exercise_id}' not found"}), 404
    delete_exercise(exercise_id)
    return jsonify({"deleted": exercise_id}), 200


# ---------------------------------------------------------------------------
# PUT /exercise/<id>/config
# Body (JSON): {"name": "...", "repetitions": 3}  (both optional)
# ---------------------------------------------------------------------------
@exercise_bp.route("/<exercise_id>/config", methods=["PUT"])
def patch_config(exercise_id):
    if not exercise_exists(exercise_id):
        return jsonify({"error": f"Exercise '{exercise_id}' not found"}), 404

    data = request.get_json(silent=True) or {}
    name = data.get("name")
    repetitions = data.get("repetitions")

    if repetitions is not None:
        if not isinstance(repetitions, int) or repetitions < 1:
            return jsonify({"error": "'repetitions' must be a positive integer"}), 400

    cfg = update_config(exercise_id, name=name, repetitions=repetitions)
    return jsonify(cfg), 200


# ---------------------------------------------------------------------------
# GET /exercise/<id>/frames
# Returns frames in frame_sequence order
# ---------------------------------------------------------------------------
@exercise_bp.route("/<exercise_id>/frames", methods=["GET"])
def get_frames_route(exercise_id):
    if not exercise_exists(exercise_id):
        return jsonify({"error": f"Exercise '{exercise_id}' not found"}), 404
    try:
        frames = get_frames(exercise_id)
    except FileNotFoundError as e:
        return jsonify({"error": str(e)}), 404
    return jsonify(frames), 200


# ---------------------------------------------------------------------------
# PUT /exercise/<id>/sequence
# Body (JSON): {"frame_sequence": [0, 2, 1, 2, 0]}
# ---------------------------------------------------------------------------
@exercise_bp.route("/<exercise_id>/sequence", methods=["PUT"])
def patch_sequence(exercise_id):
    if not exercise_exists(exercise_id):
        return jsonify({"error": f"Exercise '{exercise_id}' not found"}), 404

    data = request.get_json(silent=True)
    if not data or "frame_sequence" not in data:
        return jsonify({"error": "'frame_sequence' is required"}), 400

    seq = data["frame_sequence"]
    if not isinstance(seq, list):
        return jsonify({"error": "'frame_sequence' must be a list of integers"}), 400

    try:
        cfg = update_sequence(exercise_id, seq)
    except ValueError as e:
        return jsonify({"error": str(e)}), 400
    return jsonify(cfg), 200


# ---------------------------------------------------------------------------
# GET /exercise/<id>/frame/<idx>
# ---------------------------------------------------------------------------
@exercise_bp.route("/<exercise_id>/frame/<int:frame_index>", methods=["GET"])
def get_frame_route(exercise_id, frame_index):
    if not exercise_exists(exercise_id):
        return jsonify({"error": f"Exercise '{exercise_id}' not found"}), 404
    try:
        frame = get_frame(exercise_id, frame_index)
    except FileNotFoundError as e:
        return jsonify({"error": str(e)}), 404
    return jsonify(frame), 200


# ---------------------------------------------------------------------------
# PUT /exercise/<id>/frame/<idx>
# Body (JSON): {"nao_angles": [...], "keypoints": {...}}  (both optional)
# ---------------------------------------------------------------------------
@exercise_bp.route("/<exercise_id>/frame/<int:frame_index>", methods=["PUT"])
def put_frame(exercise_id, frame_index):
    if not exercise_exists(exercise_id):
        return jsonify({"error": f"Exercise '{exercise_id}' not found"}), 404

    data = request.get_json(silent=True) or {}
    nao_angles = data.get("nao_angles")
    keypoints = data.get("keypoints")

    if nao_angles is None and keypoints is None:
        return jsonify({"error": "provide 'nao_angles' and/or 'keypoints'"}), 400

    try:
        frame = update_frame(exercise_id, frame_index, nao_angles=nao_angles, keypoints=keypoints)
    except FileNotFoundError as e:
        return jsonify({"error": str(e)}), 404
    return jsonify(frame), 200


# ---------------------------------------------------------------------------
# POST /exercise/<id>/frame
# Body (JSON): {"keypoints": {...}, "nao_angles": [...]}
# ---------------------------------------------------------------------------
@exercise_bp.route("/<exercise_id>/frame", methods=["POST"])
def post_frame(exercise_id):
    if not exercise_exists(exercise_id):
        return jsonify({"error": f"Exercise '{exercise_id}' not found"}), 404

    data = request.get_json(silent=True)
    if not data:
        return jsonify({"error": "JSON body required"}), 400

    keypoints = data.get("keypoints")
    nao_angles = data.get("nao_angles")

    if keypoints is None or nao_angles is None:
        return jsonify({"error": "'keypoints' and 'nao_angles' are required"}), 400

    frame = add_frame(exercise_id, keypoints=keypoints, nao_angles=nao_angles)
    return jsonify(frame), 201


# ---------------------------------------------------------------------------
# DELETE /exercise/<id>/frame/<idx>
# ---------------------------------------------------------------------------
@exercise_bp.route("/<exercise_id>/frame/<int:frame_index>", methods=["DELETE"])
def del_frame(exercise_id, frame_index):
    if not exercise_exists(exercise_id):
        return jsonify({"error": f"Exercise '{exercise_id}' not found"}), 404
    try:
        cfg = delete_frame(exercise_id, frame_index)
    except FileNotFoundError as e:
        return jsonify({"error": str(e)}), 404
    return jsonify(cfg), 200
