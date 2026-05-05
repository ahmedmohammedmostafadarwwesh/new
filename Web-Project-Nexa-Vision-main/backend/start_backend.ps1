<#
start_backend.ps1
Windows helper: creates a venv (if missing), activates it, installs requirements
and starts the FastAPI app with uvicorn on port 8000.
#>
$ErrorActionPreference = 'Stop'
$here = Split-Path -Parent $MyInvocation.MyCommand.Definition
Set-Location $here

if (-not (Test-Path venv)) {
    python -m venv venv
}

# Activate the virtual environment for the current session
. .\venv\Scripts\Activate

# Install dependencies and start the server
pip install -r requirements.txt
uvicorn main:app --reload --host 0.0.0.0 --port 8000