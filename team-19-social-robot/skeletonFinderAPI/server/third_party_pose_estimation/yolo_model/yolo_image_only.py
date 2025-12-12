import base64
import io
import json
from typing import Dict, Optional, Union

import cv2
import numpy as np
from PIL import Image
from ultralytics import YOLO
# adapted from https://medium.com/@staytechrich/human-pose-estimation-with-yolov11-96932a5d7159


def __get_pose_configuration(keypoints_xy, keypoints_conf, visualized_image, thickness=2) -> Dict:
    if keypoints_xy is None or len(keypoints_xy) == 0 or keypoints_conf is None:
        return visualized_image

    # COCO 17-keypoint skeleton (edges between keypoints)
    skeleton = [
        (0, 1), (0, 2), (1, 3), (2, 4), (5, 6), (5, 7), (7, 9), (6, 8), (8, 10),
        (5, 11), (6, 12), (11, 12), (11, 13), (13, 15), (12, 14), (14, 16)
    ]

    configuration = {}
    for person_idx, (kpts, confs) in enumerate(zip(keypoints_xy, keypoints_conf)):
        person_configuration = {}
        kpts = kpts.cpu().numpy()  # Shape: (17, 2) [x, y]
        confs = confs.cpu().numpy()  # Shape: (17,) [confidence]

        # Draw keypoints
        for i, (x, y) in enumerate(kpts):
            if visualized_image is not None:
                if confs[i] > 0.5:  # Draw keypoints with sufficient confidence
                    cv2.circle(visualized_image, (int(x), int(y)), 5, (0, 0, 255), -1)

            person_configuration[str(i)] = {"x": int(x), "y": int(y), "confidence": float(confs[i])}

        # Draw skeleton lines
        for (start, end) in skeleton:
            if visualized_image is not None:
                if confs[start] > 0.5 and confs[end] > 0.5:
                    start_pt = (int(kpts[start][0]), int(kpts[start][1]))
                    end_pt = (int(kpts[end][0]), int(kpts[end][1]))
                    cv2.line(visualized_image, start_pt, end_pt, (255, 0, 0), thickness)
        configuration["person_pose_" + str(person_idx)] = person_configuration

    return configuration


def __detect_bounding_rects(image, visualized_result: Optional[np.array],
                            pose_configuration: Dict, device: str = "cpu") -> Dict:
    det_model = YOLO('yolo11x.pt')
    print("Started boundary detection on image...")

    det_results = det_model(
        image,
        conf=0.25,
        iou=0.45,
        classes=[0],  # Person class only
        device=device,
        half=True,
        verbose=False
    )

    # Extract bounding boxes from detection results
    for result in det_results:
        if result.boxes is not None and result.boxes.xyxy is not None:
            boxes = result.boxes.xyxy.cpu().numpy()  # Bounding boxes (xyxy)
            # Draw bounding boxes
            for box in boxes:
                x1, y1, x2, y2 = map(int, box)
                cv2.rectangle(visualized_result, (x1, y1), (x2, y2), (0, 255, 0), 3)
                cv2.putText(visualized_result, "Person", (x1, y1 - 10),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 0), 3)
                this_person = True
                for person_name, person_config in pose_configuration.items():
                    for i in range(0, 17):
                        if str(i) in person_config.keys():
                            if x1 > person_config[str(i)]["x"] > x2:
                                this_person = False
                                break
                            if y1 > person_config[str(i)]["y"] > y2:
                                this_person = False
                                break
                    if not this_person:
                        break
                if this_person:
                    pose_configuration["x_bounding_box"] = {
                        "first_point": {
                            "x": float(x1),
                            "y": float(y1)
                        },
                        "second_point": {
                            "x": float(x2),
                            "y": float(y1)
                        },
                        "third_point": {
                            "x": float(x1),
                            "y": float(y2)
                        },
                        "fourth_point": {
                            "x": float(x2),
                            "y": float(y2)
                        }
                    }
    return pose_configuration


# first run - 12 minutes for one image on CPU
def process_image(orig_image: Union[bytes, str], is_base64encoded: bool = True, device: str = "cpu",
                  view_img: bool = False, get_bounding_box: bool = False):
    orig_image = base64.b64decode(orig_image) if is_base64encoded else orig_image

    pose_model = YOLO('yolo11x-pose.pt')
    with Image.open(io.BytesIO(orig_image)) as img:
        image = cv2.cvtColor(np.array(img), cv2.COLOR_BGR2RGB)  # convert frame to RGB

        print("Started pose estimation on image...")
        pose_results = pose_model(
            image,
            conf=0.25,
            iou=0.45,
            classes=[0],  # Person class only
            device=device,
            half=True,
            verbose=False
        )
        # Extract keypoints and confidence scores
        keypoints_xy, keypoints_conf = [], []
        for result in pose_results:
            if result.keypoints is not None:
                keypoints_xy = result.keypoints.xy  # Shape: (num_persons, 17, 2) [x, y]
                keypoints_conf = result.keypoints.conf  # Shape: (num_persons, 17) [conf]
        visualized_result = image.copy() if view_img else None
        pose_configuration = __get_pose_configuration(keypoints_xy, keypoints_conf, visualized_result)
        if get_bounding_box:
            pose_configuration = __detect_bounding_rects(
                image, visualized_result, pose_configuration, device)
        if visualized_result is not None:
            ret, buf = cv2.imencode('.png', visualized_result)
            pose_configuration["visualization_base64"] = base64.b64encode(
                np.array(buf)).decode("utf-8")
        return pose_configuration
