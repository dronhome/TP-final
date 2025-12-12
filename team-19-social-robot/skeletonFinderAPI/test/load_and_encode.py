import base64

print("Image")
with open("pose.png", "rb") as file:
    with open("imageBase64.txt", "w", encoding="utf-8") as file2:
        file2.write(base64.b64encode(file.read()).decode("utf-8"))

print("Video")
with open("testVideo.mp4", "rb") as file:
    with open("videoBase64.txt", "w", encoding="utf-8") as file2:
        file2.write(base64.b64encode(file.read()).decode("utf-8"))
