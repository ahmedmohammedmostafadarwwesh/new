from fastapi import FastAPI
import RPi.GPIO as GPIO
import time
import atexit

app = FastAPI()

GPIO.setmode(GPIO.BCM)

# ====== MOTOR ======
IN1 = 17
IN2 = 27
IN3 = 22
IN4 = 23

GPIO.setup(IN1, GPIO.OUT)
GPIO.setup(IN2, GPIO.OUT)
GPIO.setup(IN3, GPIO.OUT)
GPIO.setup(IN4, GPIO.OUT)

def stop():
    GPIO.output(IN1, 0)
    GPIO.output(IN2, 0)
    GPIO.output(IN3, 0)
    GPIO.output(IN4, 0)

def forward():
    GPIO.output(IN1, 1)
    GPIO.output(IN2, 0)
    GPIO.output(IN3, 1)
    GPIO.output(IN4, 0)

def backward():
    GPIO.output(IN1, 0)
    GPIO.output(IN2, 1)
    GPIO.output(IN3, 0)
    GPIO.output(IN4, 1)

# ====== ULTRASONIC ======
TRIG = 16
ECHO = 18

GPIO.setup(TRIG, GPIO.OUT)
GPIO.setup(ECHO, GPIO.IN)

def get_distance():
    GPIO.output(TRIG, False)
    time.sleep(0.05)

    GPIO.output(TRIG, True)
    time.sleep(0.00001)
    GPIO.output(TRIG, False)

    start = time.time()
    timeout = start + 0.04

    while GPIO.input(ECHO) == 0:
        start = time.time()
        if start > timeout:
            return -1

    stop_time = time.time()
    timeout = stop_time + 0.04

    while GPIO.input(ECHO) == 1:
        stop_time = time.time()
        if stop_time > timeout:
            return -1

    distance = (stop_time - start) * 17150
    return round(distance, 2)

# ====== ENCODER ======
ENCODER_PIN = 25
counter = 0

GPIO.setup(ENCODER_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)

def count_pulse(channel):
    global counter
    counter += 1

GPIO.add_event_detect(ENCODER_PIN, GPIO.RISING, callback=count_pulse)

# ====== API ======
@app.get("/")
def home():
    return {"status": "robot ready"}

@app.get("/forward")
def move_forward():
    forward()
    return {"action": "forward"}

@app.get("/backward")
def move_backward():
    backward()
    return {"action": "backward"}

@app.get("/stop")
def stop_robot():
    stop()
    return {"action": "stop"}

@app.get("/distance")
def distance():
    return {"distance_cm": get_distance()}

@app.get("/encoder")
def encoder():
    return {"count": counter}

# ====== CLEANUP ======
def cleanup():
    GPIO.cleanup()

atexit.register(cleanup)