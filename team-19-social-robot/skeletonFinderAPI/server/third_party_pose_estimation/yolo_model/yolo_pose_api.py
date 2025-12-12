import json
from typing import Optional

from PIL import Image
from flask import Blueprint, request

from .pose_estimate import evaluate_yolo_pose_from_video
from .yolo_image_only import process_image


def application_json_response(payload, status):
    return json.dumps(payload), status, {"content-type": "application/json"}


def text_response(payload, status=200):
    return payload, status, {"content-type": "plain_text"}


yolo_pose_api = Blueprint("yolo_pose_api", __name__, template_folder="templates")


@yolo_pose_api.route("/pose_from_image", methods=["GET"])
def pose_from_image_local():
    file_location = request.args.get("file_location", "")
    if file_location:
        view_img = bool(request.args.get("view_img", "False"))
        get_bounding_box = bool(request.args.get("get_bounding_box", "False"))
        with open(file_location, "rb") as evaluated_image:
            evaluation_response = process_image(evaluated_image.read(), is_base64encoded=False,
                                                view_img=view_img, get_bounding_box=get_bounding_box)
        return application_json_response(evaluation_response, 200)
    return application_json_response({
        "Error": "File path does not specified. "
                 "Please specify location of file (using file_location request parameter) "
                 "on disk or mounted docker volume."
    }, 500)


@yolo_pose_api.route("/pose_from_video", methods=["GET"])
def pose_from_video_local():
    file_location = request.args.get("file_location", "")
    if file_location:
        number_frames_per_sec = int(request.args.get("number_frames_per_sec", 1))
        number_seconds_to_process = int(request.args.get("number_seconds_to_process", -1))
        evaluation_response = list(
            evaluate_yolo_pose_from_video(source=file_location, number_frames_per_sec=number_frames_per_sec,
                                          number_seconds_to_process=number_seconds_to_process,
                                          is_base64encoded=False))
        return application_json_response(evaluation_response, 200)
    return application_json_response({
        "Error": "File path does not specified. Please specify location of file "
                 "(using file_location request parameter) on disk or mounted docker volume."
    }, 500)


@yolo_pose_api.route("/pose_from_image", methods=["POST"])
def pose_from_image():
    encoded_image = request.get_data().decode("utf-8", "ignore")
    view_img = bool(request.args.get("view_img", "False"))
    get_bounding_box = bool(request.args.get("get_bounding_box", "False"))
    evaluation_response = process_image(encoded_image, is_base64encoded=True,
                                        view_img=view_img, get_bounding_box=get_bounding_box)
    return application_json_response(evaluation_response, 200)


@yolo_pose_api.route("/pose_from_video", methods=["POST"])
def pose_from_video():
    encoded_video = request.get_data().decode("utf-8", "ignore")
    number_frames_per_sec = int(request.args.get("number_frames_per_sec", 1))
    number_seconds_to_process = int(request.args.get("number_seconds_to_process", -1))
    evaluation_response = list(
        evaluate_yolo_pose_from_video(source=encoded_video, number_frames_per_sec=number_frames_per_sec,
                                      number_seconds_to_process=number_seconds_to_process,
                                      is_base64encoded=True))
    return application_json_response(evaluation_response, 200)
