import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BCM)

IN1 = 17
IN2 = 18
IN3 = 22
IN4 = 23

GPIO.setup(IN1, GPIO.OUT)
GPIO.setup(IN2, GPIO.OUT)
GPIO.setup(IN3, GPIO.OUT)
GPIO.setup(IN4, GPIO.OUT)

def stop():
    GPIO.output(IN1, GPIO.LOW)
    GPIO.output(IN2, GPIO.LOW)
    GPIO.output(IN3, GPIO.LOW)
    GPIO.output(IN4, GPIO.LOW)

def forward():
    stop()
    GPIO.output(IN1, GPIO.HIGH)
    GPIO.output(IN3, GPIO.HIGH)

def backward():
    stop()
    GPIO.output(IN2, GPIO.HIGH)
    GPIO.output(IN4, GPIO.HIGH)

def left():
    stop()
    GPIO.output(IN2, GPIO.HIGH)
    GPIO.output(IN3, GPIO.HIGH)

def right():
    stop()
    GPIO.output(IN1, GPIO.HIGH)
    GPIO.output(IN4, GPIO.HIGH)