#"../../venv/Scripts/python.exe" pose_estimate.py --source ../../datasets/exercisesVideoFast/exercise1Fast.mp4
import base64
import io
import math
import os
import sys
import tempfile
from typing import Dict, List, Iterator

import cv2
import time
import argparse
import numpy as np
import matplotlib.pyplot as plt
from PIL import Image
from torchvision import transforms

from third_party_pose_estimation.yolo_model.utils.datasets import letterbox
from third_party_pose_estimation.yolo_model.utils.plots import output_to_keypoint, plot_one_box_kpt, colors
from third_party_pose_estimation.yolo_model.models.experimental import attempt_load
from third_party_pose_estimation.yolo_model.utils.general import non_max_suppression_kpt, strip_optimizer

import torch

from third_party_pose_estimation.yolo_model.utils.torch_utils import select_device

# Save the original torch.load function
_original_torch_load = torch.load


# Define a new function that forces weights_only=False
def custom_torch_load(*args, **kwargs):
    if "weights_only" not in kwargs:
        kwargs["weights_only"] = False
    return _original_torch_load(*args, **kwargs)


# Override torch.load globally
torch.load = custom_torch_load


def get_skeleton_parts(x, kpts, steps):
    x_coord_start, y_coord_start = float(x[0]), float(x[1])
    x_coord_end, y_coord_end = float(x[2]), float(x[3])
    config = {"x_bound_rect": {"first_point": {"x": float(x_coord_start), "y": float(y_coord_start)},
                               "second_point": {"x": float(x_coord_end), "y": float(y_coord_start)},
                               "third_point": {"x": float(x_coord_start), "y": float(y_coord_end)},
                               "fourth_point": {"x": float(x_coord_end), "y": float(y_coord_end)}
                               }}
    num_kpts = len(kpts) // steps

    for kid in range(num_kpts):
        x_coord, y_coord = kpts[steps * kid], kpts[steps * kid + 1]
        config["" + str(kid)] = {"x": float(x_coord), "y": float(y_coord)}
    return config


def should_extract_frame(frame_number: int, fps: int = 30, number_frames_per_sec: int = 1):
    if int(fps // number_frames_per_sec) == 0:
        if frame_number % fps == 0:
            return True
        else:
            return False
    for frame_occurrence in range(0, int(fps), int(fps // number_frames_per_sec)):
        if (frame_occurrence == 0 and frame_number % fps == 0) or (
                frame_occurrence != 0 and frame_number % frame_occurrence == 0):
            return True
    return False


def process_image(orig_image: bytes, model, names,device='cpu', line_thickness=3,
                        hide_labels=False, hide_conf=True):
    with Image.open(io.BytesIO(orig_image)) as img:
        image = cv2.cvtColor(np.array(img), cv2.COLOR_BGR2RGB)  # convert frame to RGB
        image = transforms.ToTensor()(image)
        image = torch.tensor(np.array([image.numpy()]))

        image = image.to(device)  # convert image data to device
        image = image.float()  # convert image to float precision (cpu)

        with torch.no_grad():  # get predictions
            output_data, _ = model(image)

        output_data = non_max_suppression_kpt(output_data,  # Apply non max suppression
                                              0.25,  # Conf. Threshold.
                                              0.65,  # IoU Threshold.
                                              nc=model.yaml['nc'],  # Number of classes.
                                              nkpt=model.yaml['nkpt'],  # Number of keypoints.
                                              kpt_label=True)

        # output = output_to_keypoint(output_data)

        im0 = image[0].permute(1, 2,
                               0) * 255  # Change format [b, c, h, w] to [h, w, c] for displaying the image.
        im0 = im0.cpu().numpy().astype(np.uint8)

        im0 = cv2.cvtColor(im0, cv2.COLOR_RGB2BGR)  # reshape image format to (BGR)
        # gn = torch.tensor(im0.shape)[[1, 0, 1, 0]]  # normalization gain whwh
        for i, pose in enumerate(output_data):  # detections per image
            print(pose)
            if len(output_data):  # check if no pose
                for c in pose[:, 5].unique():  # Print results
                    n = (pose[:, 5] == c).sum()  # detections per class
                    print("No of Objects in Current Frame : {}".format(n))

                for det_index, (*xyxy, conf, cls) in enumerate(
                        reversed(pose[:, :6])):  # loop over poses for drawing on frame
                    c = int(cls)  # integer class
                    kpts = pose[det_index, 6:]
                    label = None if hide_labels else (
                        names[c] if hide_conf else f'{names[c]} {conf:.2f}')
                    plot_one_box_kpt(xyxy, im0, label=label, color=colors(c, True),
                                     line_thickness=line_thickness, kpt_label=True, kpts=kpts, steps=3,
                                     orig_shape=im0.shape[:2])
                    data_with_pose = get_skeleton_parts(xyxy, kpts, 3)
                    yield data_with_pose


def process_video_image(orig_image, model, names, frame_width, out, total_fps, fps_list, time_list, device='cpu', line_thickness=3,
                        hide_labels=False, hide_conf=True, view_img=False):
    image = cv2.cvtColor(orig_image, cv2.COLOR_BGR2RGB)  # convert frame to RGB
    image = letterbox(image, (frame_width), stride=64, auto=True)[0]
    # image_ = image.copy()
    image = transforms.ToTensor()(image)
    image = torch.tensor(np.array([image.numpy()]))

    image = image.to(device)  # convert image data to device
    image = image.float()  # convert image to float precision (cpu)
    start_time = time.time()  # start time for fps calculation

    with torch.no_grad():  # get predictions
        output_data, _ = model(image)

    output_data = non_max_suppression_kpt(output_data,  # Apply non max suppression
                                          0.25,  # Conf. Threshold.
                                          0.65,  # IoU Threshold.
                                          nc=model.yaml['nc'],  # Number of classes.
                                          nkpt=model.yaml['nkpt'],  # Number of keypoints.
                                          kpt_label=True)

    # output = output_to_keypoint(output_data)

    im0 = image[0].permute(1, 2,
                           0) * 255  # Change format [b, c, h, w] to [h, w, c] for displaying the image.
    im0 = im0.cpu().numpy().astype(np.uint8)

    im0 = cv2.cvtColor(im0, cv2.COLOR_RGB2BGR)  # reshape image format to (BGR)
    # gn = torch.tensor(im0.shape)[[1, 0, 1, 0]]  # normalization gain whwh

    for i, pose in enumerate(output_data):  # detections per image
        print(pose)
        if len(output_data):  # check if no pose
            for c in pose[:, 5].unique():  # Print results
                n = (pose[:, 5] == c).sum()  # detections per class
                print("No of Objects in Current Frame : {}".format(n))

            for det_index, (*xyxy, conf, cls) in enumerate(
                    reversed(pose[:, :6])):  # loop over poses for drawing on frame
                c = int(cls)  # integer class
                kpts = pose[det_index, 6:]
                label = None if hide_labels else (
                    names[c] if hide_conf else f'{names[c]} {conf:.2f}')
                plot_one_box_kpt(xyxy, im0, label=label, color=colors(c, True),
                                 line_thickness=line_thickness, kpt_label=True, kpts=kpts, steps=3,
                                 orig_shape=im0.shape[:2])
                data_with_pose = get_skeleton_parts(xyxy, kpts, 3)
                yield data_with_pose
    end_time = time.time()  # Calculatio for FPS
    fps = 1 / (end_time - start_time)
    total_fps += fps
    fps_list.append(total_fps)  # append FPS in list
    time_list.append(end_time - start_time)  # append time in list

    # Stream results
    if view_img:
        cv2.imshow("YOLOv7 Pose Estimation Demo", im0)
        cv2.waitKey(1)  # 1 millisecond

    out.write(im0)  # writing the video frame

@torch.no_grad()
def evaluate_yolo_pose_from_image(poseweights="yolov7-w6-pose.pt", source: str = "football1.mp4", device='cpu', view_img=False,
        save_conf=False, line_thickness=3, hide_labels=False, hide_conf=True, video_frame_per_second: int = 30,
                       number_frames_per_sec: int = 1, number_seconds_to_process: int = -1,
                       is_base64encoded = False) -> Iterator[Dict]:
    source = base64.b64decode(source) if is_base64encoded else source
    if number_frames_per_sec > video_frame_per_second:
        raise Exception("Number of frames per sec to extract cannot be higher as fps!")
    elif number_frames_per_sec < 1:
        raise Exception("Number of frames per sec to extract should be at least 1")

    device = select_device(device)  # select device

    is_server = True
    if is_server:
        sys.path.insert(0, './third_party_pose_estimation/yolo_model')
    model = attempt_load(poseweights, map_location=device)  # Load model

    torch.serialization.add_safe_globals([model])
    _ = model.eval()
    names = model.module.names if hasattr(model, 'module') else model.names  # get class names

    for image_config in process_image(source, model, names, device, line_thickness,
                        hide_labels, hide_conf):
        yield image_config

@torch.no_grad()
def evaluate_yolo_pose_from_video(poseweights="yolov7-w6-pose.pt", source: str = "football1.mp4", device='cpu', view_img=False,
        save_conf=False, line_thickness=3, hide_labels=False, hide_conf=True, video_frame_per_second: int = 30,
                       number_frames_per_sec: int = 1, number_seconds_to_process: int = -1,
                       is_base64encoded = False) -> Iterator[Dict]:
    source = base64.b64decode(source) if is_base64encoded else source
    if number_frames_per_sec > video_frame_per_second:
        raise Exception("Number of frames per sec to extract cannot be higher as fps!")
    elif number_frames_per_sec < 1:
        raise Exception("Number of frames per sec to extract should be at least 1")
    frame_count = 0  # count no of frames
    total_fps = 0  # count total fps
    time_list = []  # list to store time
    fps_list = []  # list to store fps

    device = select_device(device)  # select device
    half = device.type != 'cpu'

    is_server = True
    if is_server:
        sys.path.insert(0, './third_party_pose_estimation/yolo_model')
    model = attempt_load(poseweights, map_location=device)  # Load model

    torch.serialization.add_safe_globals([model])
    _ = model.eval()
    names = model.module.names if hasattr(model, 'module') else model.names  # get class names

    if isinstance(source, bytes):
        tfile = tempfile.NamedTemporaryFile(delete=True)
        tfile.write(source)
        cap = cv2.VideoCapture(tfile.name)
        tfile.close()
    elif source.isnumeric():
        cap = cv2.VideoCapture(int(source))  # pass video to videocapture object
    else:
        cap = cv2.VideoCapture(source)  # pass video to videocapture object

    if not cap.isOpened():  # check if videocapture not opened
        print('Error while trying to read video. Please check path again')
        raise SystemExit()
    else:
        frame_width = int(cap.get(3))  # get video frame width
        frame_height = int(cap.get(4))  # get video frame height

        vid_write_image = letterbox(cap.read()[1], (frame_width), stride=64, auto=True)[0]  # init videowriter
        resize_height, resize_width = vid_write_image.shape[:2]

        out = cv2.VideoWriter(f"{source}_keypoint.mp4",
                              cv2.VideoWriter_fourcc(*'mp4v'), video_frame_per_second,
                              (resize_width, resize_height))

        processed = 0
        frame_number = 0

        while cap.isOpened:  # loop until cap opened or video not complete
            print("Frame {} Processing".format(frame_number + 1))

            ret, frame = cap.read()  # get frame and success from video capture
            if number_seconds_to_process != -1 and frame_number / video_frame_per_second > number_seconds_to_process:
                print("Number seconds exceeded given threshold of " + str(number_seconds_to_process))
                break
            if ret:  # if success is true, means frame exist
                frame_number = frame_number + 1
                if should_extract_frame(frame_number - 1, video_frame_per_second, number_frames_per_sec):
                    for image_config in process_video_image(frame, model, names, frame_width, out,
                                                            total_fps, fps_list, time_list,
                                                            device, line_thickness, hide_labels,
                                                            hide_conf, view_img):
                        yield image_config
                    frame_count += 1
                    if processed > 6:
                        break
                    processed = processed + 1

            else:
                break

        cap.release()
        # cv2.destroyAllWindows()
        avg_fps = total_fps / frame_count
        print(f"Average FPS: {avg_fps:.3f}")

        # plot the comparision graph
        plot_fps_time_comparision(time_list=time_list, fps_list=fps_list)


def parse_opt():
    parser = argparse.ArgumentParser()
    parser.add_argument('--poseweights', nargs='+', type=str, default='yolov7-w6-pose.pt', help='model path(s)')
    parser.add_argument('--source', type=str, default='football1.mp4', help='video/0 for webcam')  # video source
    parser.add_argument('--device', type=str, default='cpu', help='cpu/0,1,2,3(gpu)')  # device arugments
    parser.add_argument('--view-img', action='store_true', help='display results')  # display results
    parser.add_argument('--save-conf', action='store_true',
                        help='save confidences in --save-txt labels')  # save confidence in txt writing
    parser.add_argument('--line-thickness', default=3, type=int,
                        help='bounding box thickness (pixels)')  # box linethickness
    parser.add_argument('--hide-labels', default=False, action='store_true', help='hide labels')  # box hidelabel
    parser.add_argument('--hide-conf', default=False, action='store_true', help='hide confidences')  # boxhideconf
    opt = parser.parse_args()
    return opt


# function for plot fps and time comparision graph
def plot_fps_time_comparision(time_list, fps_list) -> None:
    plt.figure()
    plt.xlabel('Time (s)')
    plt.ylabel('FPS')
    plt.title('FPS and Time Comparision Graph')
    plt.plot(time_list, fps_list, 'b', label="FPS & Time")
    plt.savefig("FPS_and_Time_Comparision_pose_estimate.png")


# main function
def main(opt):
    evaluate_yolo_pose_from_video(**vars(opt))


if __name__ == "__main__":
    opt = parse_opt()
    strip_optimizer(opt.device, opt.poseweights)
    main(opt)
