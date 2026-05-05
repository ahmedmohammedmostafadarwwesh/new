import pathlib
import sys

project_root = pathlib.Path(__file__).resolve().parent
backend_path = project_root / "backend"

# Add backend folder to import path so backend.main can import robot_control and robot_integration.
sys.path.insert(0, str(backend_path))

from backend.main import app

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
