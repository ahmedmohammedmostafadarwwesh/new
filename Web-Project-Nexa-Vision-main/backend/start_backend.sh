#!/usr/bin/env bash
# start_backend.sh
# Unix helper: creates a venv, activates it, installs requirements and
# starts the FastAPI app with uvicorn on port 8000.
set -euo pipefail
cd "$(dirname "$0")"

if [ ! -d "venv" ]; then
  python3 -m venv venv
fi

. venv/bin/activate
pip install -r requirements.txt
uvicorn main:app --reload --host 0.0.0.0 --port 8000
