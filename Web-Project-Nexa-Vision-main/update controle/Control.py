from fastapi import FastAPI
from fastapi.responses import StreamingResponse
from pydantic import BaseModel

import camira
import motor
import ultrasonic
import encoder
import ai

app = FastAPI()

# =========================
# 📦 SYSTEM STATE
# =========================
latest_detections = []
current_command = "stop"


# =========================
# 📡 MODELS
# =========================
class MoveCommand(BaseModel):
    direction: str


class Detection(BaseModel):
    detections: list


# =========================
# 🌐 MOTOR CONTROL API
# =========================
@app.post("/move")
def move_robot(cmd: MoveCommand):

    global current_command
    current_command = cmd.direction

    if cmd.direction == "forward":
        motor.forward()

    elif cmd.direction == "backward":
        motor.backward()

    elif cmd.direction == "left":
        motor.left()

    elif cmd.direction == "right":
        motor.right()

    else:
        motor.stop()

    return {"status": current_command}


# =========================
# 🤖 AI MANUAL RUN (optional trigger)
# =========================
@app.get("/ai/run")
def run_ai():
    global latest_detections
    latest_detections = ai.detect()

    return {"detections": latest_detections}


# =========================
# 📡 RECEIVE AI FROM STREAM (if used later)
# =========================
@app.post("/detections")
def receive_detections(data: Detection):
    global latest_detections
    latest_detections = data.detections

    return {"status": "received"}


# =========================
# 📏 ULTRASONIC SENSOR
# =========================
@app.get("/distance")
def get_distance():
    d = ultrasonic.get_distance()

    if d < 20:
        motor.stop()

    return {"distance": d}


# =========================
# 🔄 ENCODER
# =========================
@app.get("/encoder")
def get_encoder():
    return {"count": encoder.get_count()}


# =========================
# 📊 STATUS ENDPOINT
# =========================
@app.get("/status")
def status():
    return {
        "command": current_command,
        "detections": latest_detections
    }


# =========================
# 📷 CAMERA STREAM (IMPORTANT)
# =========================
@app.get("/video")
def video_stream():
    return StreamingResponse(
        camira.generate_frames(),
        media_type="multipart/x-mixed-replace; boundary=frame"
    )