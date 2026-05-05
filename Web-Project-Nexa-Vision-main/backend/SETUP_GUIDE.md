# MEGASYST - Complete Integration Setup Guide

## 🎯 Overview

The MEGASYST control system is now fully integrated with three layers:

1. **Frontend** (Control.html) - User interface with authentication
2. **Dashboard API** (Port 8001) - Control center & authentication layer
3. **Robot API** (Port 8000) - Direct robot hardware control

## 📐 Architecture Diagram

```
┌─────────────────────────────────────────────────────────────┐
│                     Web Browser (Port 8080)                 │
│  ┌──────────────────────────────────────────────────────┐   │
│  │              login.html                              │   │
│  │   - Register new user                                │   │
│  │   - Login with credentials                           │   │
│  │   - Stores JWT token in localStorage                 │   │
│  └────────────────────┬─────────────────────────────────┘   │
│                       │ Redirects to                         │
│  ┌────────────────────▼─────────────────────────────────┐   │
│  │              Control.html                            │   │
│  │   - Authenticated dashboard                          │   │
│  │   - Robot control with all buttons                   │   │
│  │   - Real-time telemetry & AI detection              │   │
│  │   - Video stream from camera                         │   │
│  └────────────────────┬─────────────────────────────────┘   │
└─────────────────────────┼───────────────────────────────────┘
                          │ HTTP + JWT Token
                          ▼
        ┌─────────────────────────────────┐
        │    Dashboard API (Port 8001)    │
        │         (FastAPI)               │
        │  ┌───────────────────────────┐  │
        │  │ Authentication Layer      │  │
        │  │ - /api/auth/login         │  │
        │  │ - /api/auth/register      │  │
        │  │ - Token verification      │  │
        │  └───────────────────────────┘  │
        │  ┌───────────────────────────┐  │
        │  │ Robot Control Proxy       │  │
        │  │ - /api/robot/move         │  │
        │  │ - /api/robot/status       │  │
        │  │ - /api/robot/distance     │  │
        │  │ - /api/robot/ai           │  │
        │  │ - /api/robot/video-stream │  │
        │  └──────────┬────────────────┘  │
        └─────────────┼──────────────────┘
                      │ HTTP (No Auth needed)
                      ▼
        ┌─────────────────────────────────┐
        │    Robot API (Port 8000)        │
        │         (FastAPI)               │
        │  ┌───────────────────────────┐  │
        │  │ Motor Control             │  │
        │  │ - /move                   │  │
        │  │ - /status                 │  │
        │  └───────────────────────────┘  │
        │  ┌───────────────────────────┐  │
        │  │ Sensors & AI              │  │
        │  │ - /distance               │  │
        │  │ - /encoder                │  │
        │  │ - /ai/run                 │  │
        │  │ - /video (MJPEG stream)   │  │
        │  └───────────────────────────┘  │
        └─────────────┬──────────────────┘
                      │
                      ▼
        ┌─────────────────────────────────┐
        │   Raspberry Pi / Hardware       │
        │  ┌───────────────────────────┐  │
        │  │ Motor Control             │  │
        │  │ GPIO pins, PWM signals    │  │
        │  └───────────────────────────┘  │
        │  ┌───────────────────────────┐  │
        │  │ Sensors                   │  │
        │  │ - Ultrasonic              │  │
        │  │ - Encoders                │  │
        │  └───────────────────────────┘  │
        │  ┌───────────────────────────┐  │
        │  │ Camera/AI Processing      │  │
        │  │ - MJPEG streaming         │  │
        │  │ - YOLOv8 detection        │  │
        │  └───────────────────────────┘  │
        └─────────────────────────────────┘
```

## 🚀 Quick Start

### Prerequisites
- Python 3.8+
- MongoDB (local or Atlas cloud)
- All dependencies in requirements.txt

### Step 1: Install & Configure

```bash
# Navigate to project root
cd "Nexa Vision Project"

# Install Dashboard Backend dependencies
cd web/backend
pip install -r requirements.txt

# Install Robot dependencies
cd ../../Software_Project/Software_Project_Nexa_Vision-main/pipe_ropot_project
pip install -r requirements.txt
cd ../../../
```

### Step 2: Configure Environment

```bash
# Create/Edit .env file
cd web/backend
nano .env  # or use Notepad

# Add these settings:
MONGODB_URI=mongodb://localhost:27017
DB_NAME=dashboard_db
SECRET_KEY=your-super-secret-key-change-this-in-production
ROBOT_API_URL=http://localhost:8000
```

### Step 3: Start Services

**Terminal 1 - Robot API:**
```bash
cd Software_Project/Software_Project_Nexa_Vision-main/pipe_ropot_project
python main.py
# Running on http://localhost:8000
```

**Terminal 2 - Dashboard API:**
```bash
cd web/backend
python main.py
# Running on http://localhost:8001
```

**Terminal 3 - Frontend:**
```bash
cd web
# Option A: Python HTTP server
python -m http.server 8080

# Option B: VS Code Live Server Extension
# Right-click index.html → Open with Live Server
```

### Step 4: Access the System

1. Open browser: **http://localhost:8080/login.html**
2. Register new account or login (test user: admin/admin)
3. Click "Control" or go to **http://localhost:8080/Control.html**

## 📋 File Structure

```
web/
├── login.html                    ← Authentication page
├── Control.html                  ← Main control dashboard (UPDATED)
├── nexa_vision_client.js        ← JavaScript API client
├── backend/
│   ├── main.py                  ← Dashboard API (UPDATED with robot endpoints)
│   ├── robot_integration.py     ← Robot communication bridge (NEW)
│   ├── requirements.txt         ← Dependencies (UPDATED)
│   ├── .env.example             ← Configuration template (NEW)
│   └── .env                     ← Your configuration (DO NOT COMMIT)
│
Software_Project/Software_Project_Nexa_Vision-main/
└── pipe_ropot_project/
    ├── main.py                  ← Robot API
    ├── motor.py                 ← Motor control
    ├── camira.py                ← Camera streaming
    ├── ai.py                    ← AI detection
    ├── ultrasonic.py            ← Distance sensor
    ├── encoder.py               ← Movement encoder
    └── requirements.txt
```

## 🔐 Authentication Flow

### 1. User Registration
```
User fills form (username, email, password)
          ↓
POST /api/auth/register
          ↓
MongoDB stores user with hashed password
          ↓
Returns JWT token + user info
          ↓
Frontend stores token in localStorage
          ↓
Redirect to Control.html
```

### 2. User Login
```
User enters credentials
          ↓
POST /api/auth/login
          ↓
Validate password hash
          ↓
Generate JWT token (24-hour expiry)
          ↓
Frontend stores token: Authorization: Bearer <TOKEN>
          ↓
All subsequent requests include this header
```

### 3. Token Verification
```
Control.html reads token from localStorage
          ↓
Every API request includes: Authorization: Bearer <TOKEN>
          ↓
Dashboard API verifies token integrity
          ↓
If invalid/expired → Redirect to login.html
          ↓
If valid → Forward request to Robot API
```

## 🎮 Control.html Changes

### Before (Direct Robot Connection)
```javascript
const BACKEND_URL = "http://127.0.0.1:8000";

const sendCommand = async (endpoint, payload) => {
    const res = await fetch(`${BACKEND_URL}${endpoint}`, {
        method: "POST",
        body: JSON.stringify(payload)
    });
    return await res.json();
};

sendCommand("/move", { direction: "forward" });
```

### After (Dashboard API + Authentication)
```javascript
const DASHBOARD_API = "http://localhost:8001";
let authToken = localStorage.getItem('nexavision_token');

const sendCommand = async (endpoint, payload) => {
    const res = await fetch(`${DASHBOARD_API}${endpoint}`, {
        method: "POST",
        headers: {
            'Content-Type': 'application/json',
            'Authorization': `Bearer ${authToken}`  // ← Token included
        },
        body: JSON.stringify(payload)
    });
    return await res.json();
};

sendCommand("/api/robot/move", { direction: "forward" });
```

## 📡 API Endpoints

### Authentication
```
POST   /api/auth/register
       Body: { username, email, password, role }
       Returns: { access_token, token_type, user }

POST   /api/auth/login
       Body: { username, password }
       Returns: { access_token, token_type, user }

GET    /api/auth/me
       Headers: Authorization: Bearer <TOKEN>
       Returns: Current user info
```

### Robot Control
```
POST   /api/robot/move
       Headers: Authorization: Bearer <TOKEN>
       Body: { direction: "forward|backward|left|right|stop" }
       Returns: { status, data }

GET    /api/robot/status
       Headers: Authorization: Bearer <TOKEN>
       Returns: { command, detections }

GET    /api/robot/distance
       Headers: Authorization: Bearer <TOKEN>
       Returns: { distance: float }

GET    /api/robot/encoder
       Headers: Authorization: Bearer <TOKEN>
       Returns: { count: int }

GET    /api/robot/ai
       Headers: Authorization: Bearer <TOKEN>
       Triggers AI detection, returns: { detections: [] }

GET    /api/robot/video-stream
       Headers: Authorization: Bearer <TOKEN>
       Returns: MJPEG video stream (multipart/x-mixed-replace)
```

## 🔌 Integration Points

### 1. Video Stream Proxy
```python
# Dashboard API intercepts and proxies video
@app.get("/api/robot/video-stream")
async def video_stream_proxy(username: str = Depends(verify_token)):
    # Get video from robot API
    # Pass through with authentication
    # Return to frontend
```

**Usage in HTML:**
```html
<img id="main-video" src="http://localhost:8001/api/robot/video-stream">
```

### 2. Robot Commands
```python
# Dashboard API forwards to robot
@app.post("/api/robot/move")
async def move_robot(request: MoveRequest, username: str = Depends(verify_token)):
    result = await robot_client.move(request.direction)
    return {"status": "success", "data": result}
```

**Usage:**
```javascript
await fetch("http://localhost:8001/api/robot/move", {
    method: "POST",
    headers: { "Authorization": `Bearer ${authToken}` },
    body: JSON.stringify({ direction: "forward" })
});
```

### 3. Sensor Data
```python
@app.get("/api/robot/distance")
async def get_robot_distance(username: str = Depends(verify_token)):
    distance = await robot_client.get_distance()
    return {"status": "success", "data": distance}
```

## 🧪 Testing

### Test All Endpoints
```bash
python test_client.py
```

### Manual cURL Testing
```bash
# 1. Register
curl -X POST http://localhost:8001/api/auth/register \
  -H "Content-Type: application/json" \
  -d '{"username":"testuser","email":"test@example.com","password":"pass123","role":"user"}'

# 2. Login and get token
TOKEN=$(curl -X POST http://localhost:8001/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{"username":"testuser","password":"pass123"}' | jq -r '.access_token')

# 3. Move robot with token
curl -X POST http://localhost:8001/api/robot/move \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"direction":"forward"}'

# 4. Get distance
curl -X GET http://localhost:8001/api/robot/distance \
  -H "Authorization: Bearer $TOKEN"

# 5. Get video stream URL
curl -X GET http://localhost:8001/api/robot/video \
  -H "Authorization: Bearer $TOKEN"
```

### Browser Testing (JavaScript Console)
```javascript
// In browser console while on Control.html

// Get token
const token = localStorage.getItem('nexavision_token');

// Test move command
fetch('http://localhost:8001/api/robot/move', {
    method: 'POST',
    headers: {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${token}`
    },
    body: JSON.stringify({ direction: 'forward' })
}).then(r => r.json()).then(console.log);

// Test distance
fetch('http://localhost:8001/api/robot/distance', {
    headers: { 'Authorization': `Bearer ${token}` }
}).then(r => r.json()).then(console.log);

// Test AI
fetch('http://localhost:8001/api/robot/ai', {
    headers: { 'Authorization': `Bearer ${token}` }
}).then(r => r.json()).then(console.log);
```

## 🐛 Troubleshooting

### Issue: "Not authenticated" error
**Solution:**
- Make sure login.html redirects you to Control.html
- Check localStorage for 'nexavision_token'
- Open DevTools → Application → Local Storage
- If token is missing, go back to login.html

### Issue: Robot API unreachable
**Solution:**
- Check if Robot API is running on port 8000
- Verify ROBOT_API_URL in .env
- Test directly: `curl http://localhost:8000/docs`

### Issue: CORS errors
**Solution:**
- CORS is enabled in both APIs with `allow_origins=["*"]`
- If errors persist, check browser console for details
- Clear cache and hard reload (Ctrl+Shift+R)

### Issue: Camera not showing
**Solution:**
- Check if robot is connected and camera initialized
- Go to http://localhost:8000/docs to test /video endpoint directly
- Verify in Control.html that token is being sent

### Issue: MongoDB connection failed
**Solution:**
```bash
# Check if MongoDB is running
mongosh  # or mongo

# If not running, start it
mongod

# Or use Docker
docker run -d -p 27017:27017 --name mongodb mongo

# Or use MongoDB Atlas (cloud)
# Update MONGODB_URI in .env
```

## 📱 Mobile Access

To access from another device on the network:

### Find Your Computer IP
```bash
# Windows
ipconfig

# Linux/Mac
ifconfig
# or
hostname -I
```

### Update Browser URL
```
http://YOUR_COMPUTER_IP:8080/login.html
```

### Update .env if Robot is on Raspberry Pi
```env
ROBOT_API_URL=http://192.168.x.x:8000
ROBOT_HOST=192.168.x.x
```

## 🎯 Production Deployment

### 1. Security Updates
```env
# Change these in .env
SECRET_KEY=your-very-long-random-secret-key-256-chars
ALGORITHM=HS256
```

### 2. Database Migration
```env
# Use MongoDB Atlas instead of local
MONGODB_URI=mongodb+srv://username:password@cluster.mongodb.net/dashboard_db
```

### 3. API Configuration
```env
# Use actual domain/IP
ROBOT_API_URL=https://robot.yourdomain.com
```

### 4. HTTPS Setup
- Use nginx as reverse proxy
- Install SSL certificate (Let's Encrypt)
- Forward ports 80→8080, 443→8001

### 5. Environment Variables
```bash
# Use system env vars instead of .env
export MONGODB_URI=...
export SECRET_KEY=...
export ROBOT_API_URL=...

python main.py
```

## 📊 Database Schema

### Users Collection
```json
{
  "_id": ObjectId,
  "username": "user1",
  "email": "user@example.com",
  "password_hash": "hashed_password",
  "role": "admin",
  "created_at": timestamp,
  "is_active": true
}
```

### Dashboard Rows Collection
```json
{
  "_id": ObjectId,
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

## 🔗 Related Files

- [INTEGRATION_README.md](./INTEGRATION_README.md) - User-friendly setup guide
- [INTEGRATION_GUIDE.md](./backend/INTEGRATION_GUIDE.md) - Technical details
- [test_client.py](./test_client.py) - Python test client
- [nexa_vision_client.js](./nexa_vision_client.js) - JavaScript client library

## ✅ Verification Checklist

- [ ] Both backend services running (ports 8000, 8001)
- [ ] MongoDB running
- [ ] Frontend can be accessed (port 8080)
- [ ] Can register/login on login.html
- [ ] Video stream shows in Control.html
- [ ] Robot movement buttons respond
- [ ] Distance sensor updates every 2 seconds
- [ ] AI scan button triggers detection
- [ ] All API endpoints respond in Swagger UI
- [ ] Token persists in localStorage
- [ ] Logout clears token properly

## 🎓 Next Steps

1. **Customize UI** - Modify Control.html colors, layout
2. **Add Logging** - Log robot actions to database
3. **Advanced Stats** - Dashboard for historical data
4. **Mobile App** - React Native app using same API
5. **Alerts** - Notifications for detection results
6. **Map Integration** - Show robot path/location

---

**Last Updated:** April 2026
**Version:** 1.0 - Full Integration
**Status:** Production Ready ✅
