
from ultralytics import YOLO


model = YOLO("yolo11n-pose.yaml")  # build a new model from YAML
model = YOLO("../yolo11n-pose.pt")  # load a pretrained model (recommended for training)
model = YOLO("yolo11n-pose.yaml").load("../yolo11x-pose.pt")  # build from YAML and transfer weights

# Train the model
results = model.train(data="coco8-pose.yaml", epochs=100, imgsz=640)
model.export(format="onnx")
result = model("https://ultralytics.com/images/bus.jpg")
for result in results:
    xy = result.keypoints.xy  # x and y coordinates
    xyn = result.keypoints.xyn  # normalized
    kpts = result.keypoints.data  # x, y, visibility (if available)
    print(xy)
    print(xyn)
    print(kpts)
