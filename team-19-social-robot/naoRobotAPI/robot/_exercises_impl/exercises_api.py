import json
from flask import Blueprint


def application_json_response(payload, status):
    return json.dumps(payload), status, {"content-type": "application/json"}


def text_response(payload, status=200):
    return payload, status, {"content-type": "plain_text"}


exercises_api = Blueprint("exercises_api", __name__, template_folder="templates")


@exercises_api.route("/first_exercise", methods=["GET"])
def first_exercise():
    return application_json_response({"success": True}, 200)
