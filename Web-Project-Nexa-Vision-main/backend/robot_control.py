# Robot Hardware Control Module
# Handles motor, ultrasonic sensor, and encoder functionality

import RPi.GPIO as GPIO
import time

class RobotController:
    def __init__(self):
        """Initialize GPIO and robot hardware"""
        GPIO.setmode(GPIO.BCM)
        
        # ====== MOTOR PINS ======
        self.IN1 = 17
        self.IN2 = 27
        self.IN3 = 22
        self.IN4 = 23
        
        GPIO.setup(self.IN1, GPIO.OUT)
        GPIO.setup(self.IN2, GPIO.OUT)
        GPIO.setup(self.IN3, GPIO.OUT)
        GPIO.setup(self.IN4, GPIO.OUT)
        
        # ====== ULTRASONIC PINS ======
        self.TRIG = 16
        self.ECHO = 18
        
        GPIO.setup(self.TRIG, GPIO.OUT)
        GPIO.setup(self.ECHO, GPIO.IN)
        
        # ====== ENCODER PIN ======
        self.ENCODER_PIN = 25
        self.counter = 0
        
        GPIO.setup(self.ENCODER_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)
        GPIO.add_event_detect(self.ENCODER_PIN, GPIO.RISING, callback=self._count_pulse)
    
    def _count_pulse(self, channel):
        """Encoder pulse counter callback"""
        self.counter += 1
    
    def stop(self):
        """Stop all motor movement"""
        GPIO.output(self.IN1, 0)
        GPIO.output(self.IN2, 0)
        GPIO.output(self.IN3, 0)
        GPIO.output(self.IN4, 0)
    
    def forward(self):
        """Move robot forward"""
        GPIO.output(self.IN1, 1)
        GPIO.output(self.IN2, 0)
        GPIO.output(self.IN3, 1)
        GPIO.output(self.IN4, 0)
    
    def backward(self):
        """Move robot backward"""
        GPIO.output(self.IN1, 0)
        GPIO.output(self.IN2, 1)
        GPIO.output(self.IN3, 0)
        GPIO.output(self.IN4, 1)
    
    def left(self):
        """Turn robot left"""
        GPIO.output(self.IN1, 0)
        GPIO.output(self.IN2, 0)
        GPIO.output(self.IN3, 1)
        GPIO.output(self.IN4, 0)
    
    def right(self):
        """Turn robot right"""
        GPIO.output(self.IN1, 1)
        GPIO.output(self.IN2, 0)
        GPIO.output(self.IN3, 0)
        GPIO.output(self.IN4, 0)
    
    def get_distance(self):
        """Get distance from ultrasonic sensor (in cm)"""
        try:
            GPIO.output(self.TRIG, False)
            time.sleep(0.05)
            
            GPIO.output(self.TRIG, True)
            time.sleep(0.00001)
            GPIO.output(self.TRIG, False)
            
            start = time.time()
            timeout = start + 0.04
            
            while GPIO.input(self.ECHO) == 0:
                start = time.time()
                if start > timeout:
                    return -1
            
            stop_time = time.time()
            timeout = stop_time + 0.04
            
            while GPIO.input(self.ECHO) == 1:
                stop_time = time.time()
                if stop_time > timeout:
                    return -1
            
            distance = (stop_time - start) * 17150
            return round(distance, 2)
        except Exception as e:
            print(f"Error reading ultrasonic sensor: {e}")
            return -1
    
    def get_encoder_count(self):
        """Get encoder pulse count"""
        return self.counter
    
    def reset_encoder(self):
        """Reset encoder counter"""
        self.counter = 0
    
    def cleanup(self):
        """Clean up GPIO on shutdown"""
        try:
            self.stop()
            GPIO.cleanup()
        except Exception as e:
            print(f"Error during cleanup: {e}")


# Global robot controller instance
try:
    robot = RobotController()
except Exception as e:
    print(f"Warning: Could not initialize robot hardware: {e}")
    robot = None
