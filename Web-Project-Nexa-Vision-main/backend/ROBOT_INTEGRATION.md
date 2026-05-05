# 🤖 Robot Control Integration Guide

## Overview
Your robot control system from `main.py` has been integrated into the Nexa Vision backend and is now fully linked with `Control.html`.

## File Structure

### New Files Created
- **[robot_control.py](robot_control.py)** - Robot hardware control module with support for:
  - Motor control (forward, backward, left, right, stop)
  - Ultrasonic distance sensor
  - Encoder pulse counting

### Modified Files
- **[main.py](main.py)** - Backend API now includes:
  - `/move` - POST endpoint for robot movement (no auth required)
  - `/distance` - GET endpoint for ultrasonic sensor readings
  - `/encoder` - GET endpoint for encoder counts
  - `/ai/run` - GET endpoint for AI detection
  - `/video` - GET endpoint for video feed
  - Authenticated API endpoints under `/api/robot/`

- **[requirements.txt](requirements.txt)** - Added `RPi.GPIO` dependency

## How It Works

### Hardware Control Flow
```
Control.html (Frontend)
    ↓ (HTTP Requests)
Backend FastAPI (main.py)
    ↓ (Uses robot_control module)
robot_control.py (RobotController class)
    ↓ (GPIO control)
Raspberry Pi GPIO Pins
    ↓
Robot Hardware (Motors, Sensors)
```

### Endpoints

#### Movement Control
```http
POST /move
Content-Type: application/json

{
  "direction": "forward"  // or: backward, left, right, stop
}

Response:
{
  "status": "success",
  "action": "forward"
}
```

#### Distance Sensing
```http
GET /distance

Response:
{
  "distance_cm": 25.5,
  "status": "success"
}
```

#### Encoder Reading
```http
GET /encoder

Response:
{
  "count": 1250,
  "status": "success"
}
```

#### AI Detection
```http
GET /ai/run

Response:
{
  "status": "success",
  "detections": [...]
}
```

## Control.html Integration

The `Control.html` file automatically sends commands to these endpoints:

### Motor Control Panel
- **Arrow Buttons**: Send `/move` requests with direction changes
  - Mouse down/touch start → move command
  - Mouse up/touch end → stop command

### Status Display
- **Distance Meter**: Queries `/distance` every 2 seconds
- **Connection Status**: Updates based on distance sensor response
- **Encoder Display**: (Ready for integration with `/encoder` endpoint)

### Quick Actions
- **Scan Button**: Calls `/ai/run` for AI-based object detection
- **Emergency Stop**: Sends immediate `/move` with "stop" direction

## Installation & Setup

### 1. Install Dependencies
```bash
cd web/backend
pip install -r requirements.txt
```

### 2. Run the Backend Server
```bash
# Linux/Mac
python -m uvicorn main:app --host 0.0.0.0 --port 8000

# Windows
python -m uvicorn main:app --host 0.0.0.0 --port 8000
```

### 3. Access the Control Panel
Open in your browser:
```
http://localhost:8000/Control.html
```

## GPIO Pin Configuration

The robot uses the following Raspberry Pi GPIO pins:

### Motor Control
- IN1: GPIO 17
- IN2: GPIO 27
- IN3: GPIO 22
- IN4: GPIO 23

### Ultrasonic Sensor
- TRIG: GPIO 16
- ECHO: GPIO 18

### Encoder
- ENCODER_PIN: GPIO 25

*You can modify these in `robot_control.py` if your setup uses different pins.*

## Error Handling

The system gracefully handles missing hardware:

- If RPi.GPIO is not available (non-Raspberry Pi systems):
  - Backend logs a warning
  - API endpoints return error responses
  - Control.html shows "Server Connection Failed" message

- If GPIO initialization fails:
  - Endpoints return `{"status": "error", ...}` responses
  - Frontend displays user-friendly error messages

## Testing

### Test Motor Movement
```bash
curl -X POST http://localhost:8000/move \
  -H "Content-Type: application/json" \
  -d '{"direction": "forward"}'
```

### Test Distance Sensor
```bash
curl http://localhost:8000/distance
```

### Test Encoder
```bash
curl http://localhost:8000/encoder
```

## Advanced Features

### Authenticated Endpoints
All `/api/robot/*` endpoints require JWT authentication token:

```bash
curl -H "Authorization: Bearer YOUR_TOKEN" \
  http://localhost:8000/api/robot/status
```

### Video Streaming
The backend supports video streaming proxy through:
- `/video` - Direct video feed endpoint
- `/api/robot/video-stream` - Authenticated streaming

### AI Detection Integration
The `/ai/run` endpoint can integrate with your AI module for real-time object detection.

## Troubleshooting

| Issue | Solution |
|-------|----------|
| "Server Connection Failed" | Verify backend is running on port 8000 |
| GPIO permission denied | Run with `sudo` or add user to gpio group |
| RPi.GPIO not found | Install: `pip install RPi.GPIO` |
| Distance always shows -1 | Check ultrasonic sensor wiring (GPIO 16, 18) |

## Next Steps

1. **Video Integration**: Configure camera streaming from your AI robot module
2. **AI Detection**: Link `/ai/run` endpoint to your YOLOv8 or detection model
3. **Advanced Controls**: Add camera pan/tilt servos to control panel
4. **Data Logging**: Store movement patterns and detections to MongoDB
5. **Real-time Dashboard**: Update dashboard with telemetry data

## Original Files Reference

- Original robot control: `web/main.py` (now integrated into backend)
- Robot AI module: `Software_Project/Software_Project_Nexa_Vision-main/pipe_ropot_project/ai.py`
- Robot camera: `Software_Project/Software_Project_Nexa_Vision-main/pipe_ropot_project/camira.py`

---

**Status**: ✅ Successfully integrated with Control.html
**Last Updated**: 2026-04-28
