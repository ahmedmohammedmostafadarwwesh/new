# Backend for Nexa Vision Dashboard

This directory contains a FastAPI application that provides a simple REST API backed by MongoDB. The frontend (Dashboard.html) can query this API to display dynamic data.

## Requirements

- Python 3.9+
- MongoDB running locally or remote
- Dependencies in `requirements.txt` (install with `pip install -r requirements.txt`)

## Setup

1. Create a Python virtual environment and activate it:
   ```sh
   python -m venv venv
   source venv/Scripts/activate    # Windows
   ```
2. Install dependencies:
   ```sh
   pip install -r requirements.txt
   ```
3. Copy `.env.example` to `.env` and adjust connection string if necessary.

## Running

Start the API server using uvicorn:
```sh
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

The application also serves the frontend files from the project root so you can open
`http://localhost:8000/Dashboard/Dashboard.html` in your browser.  You no longer need a
separate static server.

The dashboard data endpoint is now prefixed with `/api` and can be reached at
`http://localhost:8000/api/dashboard`.

## Seeding sample data

You can insert example rows with:
```sh
python seed.py
```

## API Endpoints

- `GET /api/dashboard` – returns list of all rows.
- `POST /api/dashboard` – add a new row (body should match the Row model).
- `PUT /api/dashboard/{row_id}` – update a row.
- `DELETE /api/dashboard/{row_id}` – remove a row.

You can also insert rows directly from Python using `add_row.py`:
```sh
python add_row.py '{"id":6,"name":"Another","col1":"X","col2":"Y","col3":"Z","col4":"10%","col5":"20%","col6":"70%"}'
```

The front-end HTML already fetches from the GET endpoint and populates the table.

## Quick start scripts

If you want a one-command way to create a virtual environment, install dependencies and run the API server, use the helper scripts provided here.

- Windows (PowerShell):

   ```powershell
   cd backend
   .\start_backend.ps1
   ```

- Unix / WSL / macOS:

   ```bash
   cd backend
   ./start_backend.sh
   ```

The scripts will create a `venv` directory if missing and run `uvicorn main:app --reload --host 0.0.0.0 --port 8000`.
