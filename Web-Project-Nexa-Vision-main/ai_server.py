from fastapi import FastAPI, UploadFile, File
from fastapi.responses import StreamingResponse
from fastapi.middleware.cors import CORSMiddleware # السطر ده ضفناه
from ultralytics import YOLO
import cv2
import numpy as np
import time
import threading
import os
app = FastAPI()

# ====== إعدادات الـ CORS (هام جداً للربط بالويب) ======
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ====== Load Model ======
import os

# 1. الكود بيكتشف المسار الحالي اللي هو شغال منه أوتوماتيكياً
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# 2. بنبني المسار الجديد بدمج المسار الحالي مع فولدر الموديل
model_path = os.path.join(BASE_DIR, "detections", "best.pt")

# 3. تحميل الموديل بالمسار الديناميكي
model = YOLO(model_path)
# ====== Shared Data ======
latest_frame = None
lock = threading.Lock()


# =========================
#  استقبال الصور + AI Processing
# =========================
@app.post("/upload_frame")
async def upload_frame(file: UploadFile = File(...)):
    global latest_frame

    # تحويل الصورة
    image_bytes = await file.read()
    np_arr = np.frombuffer(image_bytes, np.uint8)
    frame = cv2.imdecode(np_arr, cv2.IMREAD_COLOR)

    # AI detection
    results = model(frame, imgsz=320)
    annotated = results[0].plot() # رسم المربعات على العيوب

    # حفظ الفريم بشكل آمن
    with lock:
        latest_frame = annotated

    return {"status": "processed"}


# =========================
#  Live Video Stream للويب
# =========================
@app.get("/video")
def video_feed():
    def generate():
        global latest_frame

        while True:
            with lock:
                if latest_frame is None:
                    continue
                frame = latest_frame.copy()

            _, buffer = cv2.imencode('.jpg', frame)
            frame_bytes = buffer.tobytes()

            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' +
                   frame_bytes + b'\r\n')

            time.sleep(0.05)  # smooth stream

    return StreamingResponse(
        generate(),
        media_type='multipart/x-mixed-replace; boundary=frame'
    )


# =========================
#  Test Endpoint
# =========================
@app.get("/")
def home():
    return {"status": "AI server running "}