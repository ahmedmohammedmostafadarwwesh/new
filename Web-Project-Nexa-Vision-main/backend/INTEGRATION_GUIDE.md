# Web Project & Software Project Integration Guide

## Overview
The Web Project (Dashboard) is now integrated with the Software Project (Pipe Robot). The web dashboard can control the robot and display its telemetry data.

## Project Structure

```
├── Web Project (Dashboard Backend - Port 8001)
│   ├── main.py (FastAPI server with dashboard endpoints)
│   ├── robot_integration.py (Robot client & communication)
│   └── backend/
│
└── Software Project (Robot Control - Port 8000)
    └── pipe_ropot_project/
        ├── main.py (FastAPI server with robot endpoints)
        ├── motor.py (Motor control)
        ├── camira.py (Camera streaming)
        ├── ai.py (AI detection)
        ├── ultrasonic.py (Distance sensor)
        └── encoder.py (Movement tracking)
```

## Setup Instructions

### 1. Environment Configuration

**Copy the environment template:**
```bash
cd web/backend
cp .env.example .env
```

**Edit `.env` with your configuration:**
```env
# MongoDB (local or cloud)
MONGODB_URI=mongodb://localhost:27017
DB_NAME=dashboard_db

# Robot API URL (adjust IP if robot is on different network)
ROBOT_API_URL=http://localhost:8000
# OR for Raspberry Pi:
# ROBOT_API_URL=http://192.168.x.x:8000

# JWT Security (change in production)
SECRET_KEY=your-super-secret-key-here
```

### 2. Install Dependencies

**Dashboard Backend:**
```bash
cd web/backend
pip install -r requirements.txt
```

**Robot Backend:**
```bash
cd Software_Project/Software_Project_Nexa_Vision-main/pipe_ropot_project
pip install -r requirements.txt
```

### 3. Start MongoDB

```bash
# On Windows with MongoDB installed
mongod

# OR using Docker
docker run -d -p 27017:27017 --name mongodb mongo
```

### 4. Start Both Services

**Terminal 1 - Robot Service (Pipe Project):**
```bash
cd Software_Project/Software_Project_Nexa_Vision-main/pipe_ropot_project
python main.py
# Server runs on http://localhost:8000
```

**Terminal 2 - Dashboard Backend:**
```bash
cd web/backend
python main.py
# Server runs on http://localhost:8001
```

**Terminal 3 - Frontend:**
```bash
cd web
# Open with Live Server or
python -m http.server 8080
# Visit http://localhost:8080
```

## API Endpoints

### Dashboard Authentication
- `POST /api/auth/register` - Register new user
- `POST /api/auth/login` - Login user
- `GET /api/auth/me` - Get current user profile

### Robot Control (via Dashboard)
- `POST /api/robot/move` - Move robot (forward/backward/left/right/stop)
- `GET /api/robot/status` - Get current robot status
- `GET /api/robot/distance` - Get ultrasonic sensor distance
- `GET /api/robot/ai` - Run AI detection
- `GET /api/robot/encoder` - Get encoder count
- `GET /api/robot/video` - Get video stream URL

### Dashboard Management
- `GET /api/dashboard` - Get all dashboard rows
- `POST /api/dashboard` - Create new row (admin)
- `PUT /api/dashboard/{id}` - Update row (admin)
- `DELETE /api/dashboard/{id}` - Delete row (admin)

### User Management (Admin only)
- `GET /api/users` - Get all users
- `PUT /api/users/{username}/role` - Update user role
- `PUT /api/users/{username}/activate` - Activate user
- `PUT /api/users/{username}/deactivate` - Deactivate user
- `DELETE /api/users/{username}` - Delete specific user
- `DELETE /api/users` - Delete all users except admin

## Features

### Web Dashboard
✅ User authentication & authorization
✅ Admin dashboard for data management
✅ User role management (admin/user)

### Robot Integration
✅ Remote robot movement control
✅ Real-time status monitoring
✅ AI detection triggering
✅ Sensor data access (ultrasonic, encoder)
✅ Live video streaming (MJPEG)

## Configuration Examples

### Local Development
```env
ROBOT_API_URL=http://localhost:8000
DASHBOARD_PORT=8001
```

### Robot on Raspberry Pi
```env
# Find Pi IP: ping raspberrypi.local or use router
ROBOT_API_URL=http://192.168.1.100:8000
ROBOT_HOST=192.168.1.100
ROBOT_PORT=8000
```

### Production (with proxy)
```env
ROBOT_API_URL=https://robot.example.com
```

## Troubleshooting

### Robot service not responding
1. Check if robot service is running on port 8000
2. Verify `ROBOT_API_URL` in `.env` is correct
3. Check network connectivity to robot

### MongoDB connection errors
1. Ensure MongoDB is running
2. Verify `MONGODB_URI` in `.env`
3. Check database permissions

### CORS errors in frontend
- CORS is already enabled in both backends
- Check if frontend is on a different port

### Video streaming not working
- Ensure camera is connected to robot
- Check `camira.py` for camera initialization
- Verify `/video` endpoint is accessible

## Next Steps

1. **Initialize Database:**
   ```bash
   cd web/backend
   python seed.py
   ```

2. **Create Admin User:**
   - Register via `/api/auth/register` with role "admin"

3. **Test with Postman:**
   - Import API collection to test endpoints
   - Start with `/api/robot/status`

4. **Build Custom Frontend:**
   - Update HTML files to call robot endpoints
   - Display video stream in iframe: `<img src="http://localhost:8001/api/robot/video">`

## Database Schema

### Users Collection
```json
{
  "username": "admin",
  "email": "admin@example.com",
  "password_hash": "hashed_password",
  "role": "admin",
  "created_at": "2024-01-01T00:00:00",
  "is_active": true
}
```

### Dashboard Rows Collection
```json
{
  "id": 1,
  "name": "Row Name",
  "col1": "value1",
  "col2": "value2",
  "col3": "value3",
  "col4": "value4",
  "col5": "value5",
  "col6": "value6"
}
```

## Support

For issues or questions:
1. Check the README files in each project
2. Review error logs from both services
3. Test endpoints with curl or Postman
4. Verify network connectivity between services
