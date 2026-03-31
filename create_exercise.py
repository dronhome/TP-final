import json, urllib.request, urllib.parse
import mimetypes, uuid

frames = json.load(open("frames.json"))
video_bytes = open("video_2.mp4", "rb").read()

# Build multipart/form-data manually
boundary = uuid.uuid4().hex

def field(name, value):
    return (
        f'--{boundary}\r\n'
        f'Content-Disposition: form-data; name="{name}"\r\n\r\n'
        f'{value}\r\n'
    ).encode()

def file_field(name, filename, data):
    return (
        f'--{boundary}\r\n'
        f'Content-Disposition: form-data; name="{name}"; filename="{filename}"\r\n'
        f'Content-Type: video/mp4\r\n\r\n'
    ).encode() + data + b'\r\n'

body = (
    field("name", "Video 2 Exercise") +
    field("pose_engine", "mediapipe") +
    field("frames", json.dumps(frames)) +
    file_field("media", "video_2.mp4", video_bytes) +
    f'--{boundary}--\r\n'.encode()
)

req = urllib.request.Request(
    "http://localhost:7001/exercise/create",
    data=body,
    headers={"Content-Type": f"multipart/form-data; boundary={boundary}"},
    method="POST"
)
res = json.loads(urllib.request.urlopen(req).read())
print(json.dumps(res, indent=2))
