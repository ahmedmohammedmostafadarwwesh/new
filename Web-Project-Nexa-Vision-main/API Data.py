from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse
from pydantic import BaseModel
from typing import List

import camira
import motor
import ultrasonic
import encoder
import ai

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

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

class DashboardRow(BaseModel):
    id: int
    name: str
    col1: str
    col2: str
    col3: str
    col4: str
    col5: str
    col6: str


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
# � DASHBOARD DATA
# =========================
@app.get("/api/dashboard", response_model=List[DashboardRow])
def get_dashboard():
    # Example dashboard rows. Replace with real data as needed.
    return [
        DashboardRow(id=1, name="Robot 1", col1="OK", col2="20", col3="15", col4="Active", col5="Normal", col6="Ready"),
        DashboardRow(id=2, name="Robot 2", col1="OK", col2="25", col3="18", col4="Active", col5="Normal", col6="Ready"),
    ]


# =========================
# �📏 ULTRASONIC SENSOR
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