# مريم حارس
from fastapi import FastAPI
from fastapi.responses import StreamingResponse
import cv2

app = FastAPI()

camera = cv2.VideoCapture(0)

# بث الكاميرا
def generate_frames():
    while True:
        success, frame = camera.read()
        if not success:
            break
        else:
            ret, buffer = cv2.imencode('.jpg', frame)
            frame = buffer.tobytes()

            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')


@app.get("/")
def home():
    return {"robot": "online"}


# API للكاميرا
@app.get("/video")
def video_feed():
    return StreamingResponse(generate_frames(),
            media_type="multipart/x-mixed-replace; boundary=frame")


# أوامر التحكم
@app.get("/forward")
def move_forward():
    return {"command": "forward"}

@app.get("/backward")
def move_backward():
    return {"command": "backward"}

@app.get("/left")
def move_left():
    return {"command": "left"}

@app.get("/right")
def move_right():
    return {"command": "right"}

@app.get("/stop")
def stop():
    return {"command": "stop"}