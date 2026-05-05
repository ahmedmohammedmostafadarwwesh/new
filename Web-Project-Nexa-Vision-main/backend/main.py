# عبدالله محمد عادل
from fastapi import FastAPI, HTTPException, Header, Depends
from pydantic import BaseModel, EmailStr
from typing import List, Optional
from motor.motor_asyncio import AsyncIOMotorClient
import os
from datetime import datetime, timedelta
import jwt
import bcrypt
import atexit

# load .env if exists
from dotenv import load_dotenv
load_dotenv()

# Import robot control module
try:
    from robot_control import robot
except ImportError:
    print("⚠️  Warning: robot_control module not available (RPi.GPIO not installed)")
    robot = None

# Import robot integration if available
try:
    from robot_integration import robot_client
except ImportError:
    robot_client = None

MONGODB_URI = os.getenv("MONGODB_URI", "mongodb://localhost:27017")
DB_NAME = os.getenv("DB_NAME", "dashboard_db")
SECRET_KEY = os.getenv("SECRET_KEY", "your-secret-key-change-this-in-production")
ALGORITHM = "HS256"

app = FastAPI(title="Nexa Vision Dashboard API")

# enable CORS so that the front-end can be served separately
from fastapi.middleware.cors import CORSMiddleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# async Mongo client
client = AsyncIOMotorClient(MONGODB_URI)
db = client[DB_NAME]
rows_collection = db["rows"]
users_collection = db["users"]

# Models
class Row(BaseModel):
    id: int
    name: str
    col1: str
    col2: str
    col3: str
    col4: str
    col5: str
    col6: str

class UserRegister(BaseModel):
    username: str
    email: str
    password: str
    role: str = "user"

class UserLogin(BaseModel):
    username: str
    password: str

class User(BaseModel):
    username: str
    email: str
    role: str = "user"  # "admin" or "user"
    created_at: datetime = None
    is_active: bool = True

class UserInDB(User):
    password_hash: str

class TokenResponse(BaseModel):
    access_token: str
    token_type: str
    user: User

# Helper Functions
def hash_password(password: str) -> str:
    return bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()

def verify_password(password: str, password_hash: str) -> bool:
    return bcrypt.checkpw(password.encode(), password_hash.encode())

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(hours=24)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

async def verify_token(authorization: Optional[str] = Header(None)):
    if not authorization:
        raise HTTPException(status_code=401, detail="Not authenticated")
    try:
        token = authorization.replace("Bearer ", "")
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise HTTPException(status_code=401, detail="Invalid token")
        return username
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=401, detail="Invalid token")

async def verify_admin(username: str = Depends(verify_token)):
    user_doc = await users_collection.find_one({"username": username})
    if not user_doc or user_doc.get("role") != "admin":
        raise HTTPException(status_code=403, detail="Admin access required")
    return username

# Auth Endpoints
@app.post("/api/auth/register", response_model=TokenResponse)
async def register(user_data: UserRegister):
    """Register a new user"""
    existing = await users_collection.find_one({"username": user_data.username})
    if existing:
        raise HTTPException(status_code=400, detail="Username already exists")
    
    existing_email = await users_collection.find_one({"email": user_data.email})
    if existing_email:
        raise HTTPException(status_code=400, detail="Email already exists")
    
    role = user_data.role if user_data.role in ["admin", "user"] else "user"
    
    user_doc = {
        "username": user_data.username,
        "email": user_data.email,
        "password_hash": hash_password(user_data.password),
        "role": role,
        "created_at": datetime.utcnow(),
        "is_active": True
    }
    
    await users_collection.insert_one(user_doc)
    
    access_token = create_access_token(data={"sub": user_data.username})
    
    return TokenResponse(
        access_token=access_token,
        token_type="bearer",
        user=User(
            username=user_data.username,
            email=user_data.email,
            role=role,
            created_at=user_doc["created_at"],
            is_active=True
        )
    )

@app.post("/api/auth/login", response_model=TokenResponse)
async def login(credentials: UserLogin):
    """Login user"""
    user_doc = await users_collection.find_one({"username": credentials.username})
    if not user_doc:
        raise HTTPException(status_code=400, detail="Invalid credentials")
    
    if not verify_password(credentials.password, user_doc["password_hash"]):
        raise HTTPException(status_code=400, detail="Invalid credentials")
    
    if not user_doc.get("is_active", True):
        raise HTTPException(status_code=402, detail="User account is deactivated")
    
    access_token = create_access_token(data={"sub": credentials.username})
    
    return TokenResponse(
        access_token=access_token,
        token_type="bearer",
        user=User(
            username=user_doc["username"],
            email=user_doc["email"],
            role=user_doc.get("role", "user"),
            created_at=user_doc.get("created_at"),
            is_active=user_doc.get("is_active", True)
        )
    )

# User Management Endpoints (No authentication required for admin dashboard)
@app.get("/api/users", response_model=List[User])
async def get_all_users():
    """Get all users"""
    docs = []
    cursor = users_collection.find({})
    async for doc in cursor:
        doc.pop("_id", None)
        doc.pop("password_hash", None)
        docs.append(User(**doc))
    return docs

@app.put("/api/users/{username}/role")
async def update_user_role(username: str, new_role: str):
    """Update user role"""
    if new_role not in ["user", "admin"]:
        raise HTTPException(status_code=400, detail="Invalid role")
    
    result = await users_collection.update_one(
        {"username": username},
        {"$set": {"role": new_role}}
    )
    
    if result.matched_count == 0:
        raise HTTPException(status_code=404, detail="User not found")
    
    return {"status": "updated", "username": username, "role": new_role}

@app.put("/api/users/{username}/deactivate")
async def deactivate_user(username: str):
    """Deactivate a user"""
    result = await users_collection.update_one(
        {"username": username},
        {"$set": {"is_active": False}}
    )
    
    if result.matched_count == 0:
        raise HTTPException(status_code=404, detail="User not found")
    
    return {"status": "deactivated", "username": username}

@app.put("/api/users/{username}/activate")
async def activate_user(username: str):
    """Activate a user"""
    result = await users_collection.update_one(
        {"username": username},
        {"$set": {"is_active": True}}
    )
    
    if result.matched_count == 0:
        raise HTTPException(status_code=404, detail="User not found")
    
    return {"status": "activated", "username": username}

@app.delete("/api/users/{username}")
async def delete_user(username: str):
    """Delete a user"""
    result = await users_collection.delete_one({"username": username})
    
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="User not found")
    
    return {"status": "deleted", "username": username}

@app.delete("/api/users")
async def delete_all_users():
    """Delete all users"""
    result = await users_collection.delete_many({})
    
    return {"status": "deleted", "deleted_count": result.deleted_count, "message": f"Deleted {result.deleted_count} users"}

# Get current user info
@app.get("/api/auth/me", response_model=User)
async def get_current_user(username: str = Depends(verify_token)):
    """Get current user info"""
    user_doc = await users_collection.find_one({"username": username})
    if not user_doc:
        raise HTTPException(status_code=404, detail="User not found")
    
    user_doc.pop("_id", None)
    user_doc.pop("password_hash", None)
    return User(**user_doc)

# Dashboard Endpoints (unchanged)
@app.get("/api/dashboard", response_model=List[Row])
async def get_rows():
    """Return all rows in the dashboard collection."""
    docs = []
    cursor = rows_collection.find({})
    async for doc in cursor:
        doc.pop("_id", None)
        docs.append(Row(**doc))
    return docs

@app.post("/api/dashboard", response_model=Row)
async def create_row(row: Row, admin: str = Depends(verify_admin)):
    """Insert a new row; id must be unique (admin only)."""
    existing = await rows_collection.find_one({"id": row.id})
    if existing:
        raise HTTPException(status_code=400, detail="Row with that id already exists")
    await rows_collection.insert_one(row.dict())
    return row

@app.put("/api/dashboard/{row_id}", response_model=Row)
async def update_row(row_id: int, row: Row, admin: str = Depends(verify_admin)):
    """Update an existing row by its id (admin only)."""
    result = await rows_collection.update_one({"id": row_id}, {"$set": row.dict()})
    if result.matched_count == 0:
        raise HTTPException(status_code=404, detail="Row not found")
    return row

@app.delete("/api/dashboard/{row_id}")
async def delete_row(row_id: int, admin: str = Depends(verify_admin)):
    """Delete a row from the collection (admin only)."""
    result = await rows_collection.delete_one({"id": row_id})
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Row not found")
    return {"status": "deleted"}

# =========================
# 🤖 ROBOT CONTROL ENDPOINTS
# =========================

class MoveRequest(BaseModel):
    direction: str  # forward, backward, left, right, stop

@app.post("/move")
async def move_robot(request: MoveRequest):
    """
    Control robot movement (compatible with Control.html)
    Directions: forward, backward, left, right, stop
    """
    if not robot:
        return {"status": "error", "detail": "Robot hardware not initialized"}
    
    try:
        direction = request.direction.lower()
        if direction == "forward":
            robot.forward()
        elif direction == "backward":
            robot.backward()
        elif direction == "left":
            robot.left()
        elif direction == "right":
            robot.right()
        elif direction == "stop":
            robot.stop()
        else:
            raise ValueError(f"Unknown direction: {direction}")
        
        return {"status": "success", "action": direction}
    except Exception as e:
        return {"status": "error", "detail": str(e)}

@app.get("/distance")
async def get_robot_distance():
    """Get distance from ultrasonic sensor (compatible with Control.html)"""
    if not robot:
        return {"status": "error", "distance_cm": -1}
    
    try:
        distance = robot.get_distance()
        return {"distance_cm": distance, "status": "success"}
    except Exception as e:
        return {"status": "error", "distance_cm": -1, "detail": str(e)}

@app.get("/encoder")
async def get_robot_encoder():
    """Get encoder count"""
    if not robot:
        return {"status": "error", "count": 0}
    
    try:
        count = robot.get_encoder_count()
        return {"count": count, "status": "success"}
    except Exception as e:
        return {"status": "error", "count": 0, "detail": str(e)}

# Legacy endpoints for API compatibility
@app.post("/api/robot/move")
async def move_robot_api(request: MoveRequest, username: str = Depends(verify_token)):
    """
    Control robot movement (authenticated)
    Directions: forward, backward, left, right, stop
    """
    if not robot:
        raise HTTPException(status_code=503, detail="Robot hardware not initialized")
    
    try:
        direction = request.direction.lower()
        if direction == "forward":
            robot.forward()
        elif direction == "backward":
            robot.backward()
        elif direction == "left":
            robot.left()
        elif direction == "right":
            robot.right()
        elif direction == "stop":
            robot.stop()
        else:
            raise ValueError(f"Unknown direction: {direction}")
        
        return {"status": "success", "action": direction}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/robot/status")
async def get_robot_status(username: str = Depends(verify_token)):
    """Get current robot status"""
    if not robot:
        raise HTTPException(status_code=503, detail="Robot hardware not initialized")
    
    try:
        return {
            "status": "online",
            "distance_cm": robot.get_distance(),
            "encoder_count": robot.get_encoder_count()
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/robot/distance")
async def get_robot_distance_api(username: str = Depends(verify_token)):
    """Get distance from ultrasonic sensor"""
    if not robot:
        raise HTTPException(status_code=503, detail="Robot hardware not initialized")
    
    try:
        distance = robot.get_distance()
        return {"status": "success", "distance_cm": distance}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/robot/encoder")
async def get_robot_encoder_api(username: str = Depends(verify_token)):
    """Get encoder count"""
    if not robot:
        raise HTTPException(status_code=503, detail="Robot hardware not initialized")
    
    try:
        count = robot.get_encoder_count()
        return {"status": "success", "count": count}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Cleanup on shutdown
def cleanup_robot():
    """Clean up robot hardware on shutdown"""
    if robot:
        robot.cleanup()

atexit.register(cleanup_robot)

@app.get("/ai/run")
async def run_ai_detection():
    """Trigger AI detection (compatible with Control.html)"""
    try:
        # Check if robot_client is available for AI integration
        if robot_client:
            detections = await robot_client.run_ai_detection()
            return {"status": "success", "detections": detections}
        else:
            # Placeholder response
            return {"status": "success", "detections": []}
    except Exception as e:
        return {"status": "error", "detections": [], "detail": str(e)}

@app.get("/video")
async def get_video_feed():
    """Get video feed (returns placeholder or actual stream)"""
    try:
        if robot_client:
            return {"status": "success", "url": robot_client.get_video_stream_url()}
        else:
            # Return placeholder
            return {"status": "error", "url": ""}
    except Exception as e:
        return {"status": "error", "detail": str(e)}

# =========================
# 📹 VIDEO STREAM PROXY
# =========================
@app.get("/api/robot/video-stream")
async def video_stream_proxy(username: str = Depends(verify_token)):
    """Stream video from robot (authenticated users only)"""
    try:
        import aiohttp
        robot_url = robot_client.base_url.rstrip("/") + "/video"
        
        async def generate():
            async with aiohttp.ClientSession() as session:
                async with session.get(robot_url) as resp:
                    async for chunk in resp.content.iter_chunked(8096):
                        yield chunk
        
        from fastapi.responses import StreamingResponse
        return StreamingResponse(
            generate(),
            media_type="multipart/x-mixed-replace; boundary=frame"
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Unable to stream video: {str(e)}")

@app.post("/api/robot/detections")
async def send_detections(data: dict, admin: str = Depends(verify_admin)):
    """Send detections to robot (admin only)"""
    try:
        if robot_client:
            result = await robot_client.receive_detections(data.get("detections", []))
            return {"status": "success", "data": result}
        else:
            return {"status": "success", "data": []}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# serve the frontend files (serve project root static files)
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
import pathlib
proj_dir = pathlib.Path(__file__).resolve().parent.parent
app.mount("/", StaticFiles(directory=str(proj_dir), html=True), name="static")

@app.get("/dashboard")
async def user_dashboard():
    """Serve the regular dashboard page"""
    dashboard_file = proj_dir / "Dashboard" / "Dashboard.html"
    if dashboard_file.exists():
        return FileResponse(str(dashboard_file))
    raise HTTPException(status_code=404, detail="Dashboard not found")

# =========================
# 🤖 SIMPLE ROBOT ENDPOINTS (No Auth Required for Control Panel)
# =========================

@app.post("/move")
async def simple_move_robot(request: MoveRequest):
    """Simple robot move endpoint (no auth)"""
    try:
        if robot_client:
            result = await robot_client.move(request.direction)
            return {"status": "success", "direction": request.direction}
        else:
            return {"status": "error", "message": "Robot client not available"}
    except Exception as e:
        return {"status": "error", "message": str(e)}

@app.get("/distance")
async def simple_get_distance():
    """Simple distance endpoint (no auth)"""
    try:
        if robot_client:
            distance = await robot_client.get_distance()
            return {"distance": distance}
        else:
            return {"distance": 0, "error": "Robot client not available"}
    except Exception as e:
        return {"distance": 0, "error": str(e)}

@app.get("/encoder")
async def simple_get_encoder():
    """Simple encoder endpoint (no auth)"""
    try:
        if robot_client:
            encoder = await robot_client.get_encoder_count()
            return {"count": encoder}
        else:
            return {"count": 0}
    except Exception as e:
        return {"count": 0, "error": str(e)}

@app.get("/ai/run")
async def simple_run_ai():
    """Simple AI detection endpoint (no auth)"""
    try:
        if robot_client:
            detections = await robot_client.run_ai_detection()
            return {"detections": detections if isinstance(detections, list) else []}
        else:
            return {"detections": []}
    except Exception as e:
        return {"detections": [], "error": str(e)}

@app.get("/status")
async def simple_get_status():
    """Simple status endpoint (no auth)"""
    try:
        if robot_client:
            status = await robot_client.get_status()
            return {"status": "success", "data": status}
        else:
            return {"status": "error", "data": {"command": "stop", "detections": []}}
    except Exception as e:
        return {"status": "error", "data": {"command": "stop", "detections": []}}

@app.get("/video")
async def simple_get_video_stream():
    """Simple video stream endpoint (no auth)"""
    try:
        if robot_client:
            from fastapi.responses import StreamingResponse
            import aiohttp
            
            robot_url = robot_client.base_url.rstrip("/") + "/video"
            
            async def generate():
                async with aiohttp.ClientSession() as session:
                    async with session.get(robot_url, timeout=aiohttp.ClientTimeout(total=30)) as resp:
                        async for chunk in resp.content.iter_chunked(8096):
                            yield chunk
            
            return StreamingResponse(
                generate(),
                media_type="multipart/x-mixed-replace; boundary=frame"
            )
        else:
            raise HTTPException(status_code=500, detail="Robot client not available")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Unable to stream video: {str(e)}")

@app.post("/detections")
async def simple_receive_detections(data: dict):
    """Simple detections endpoint (no auth)"""
    try:
        if robot_client:
            result = await robot_client.receive_detections(data.get("detections", []))
            return {"status": "received", "data": result}
        else:
            return {"status": "error", "message": "Robot client not available"}
    except Exception as e:
        return {"status": "error", "message": str(e)}
