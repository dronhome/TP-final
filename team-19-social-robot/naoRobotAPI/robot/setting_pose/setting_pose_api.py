import json
from flask import Blueprint, request

from setting_pose import set_nao_pose, set_nao_pose_mediapipe


def application_json_response(payload, status):
    return json.dumps(payload), status, {"content-type": "application/json"}


def text_response(payload, status=200):
    return payload, status, {"content-type": "plain_text"}


setting_pose_api = Blueprint("setting_pose_api", __name__, template_folder="templates")


@setting_pose_api.route("/setPose", methods=["POST"])
def set_pose():
    data = request.get_json(force=True)
    angles = data["angles"]
    set_nao_pose(angles)
    return application_json_response({"success": True}, 200)



@setting_pose_api.route("/setPoseMediapipe", methods=["POST"])
def set_pose_mediapipe():
    angles_dict = request.get_data().decode("utf-8", "ignore")
    set_nao_pose_mediapipe(angles_dict)
    return application_json_response({"success": True}, 200)
