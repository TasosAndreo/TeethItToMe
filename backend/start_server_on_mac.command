
#!/bin/bash

# Stop if a command fails
set -e

# Move to the backend directory
cd "$(dirname "$0")"

# Activate the Python virtual environment
source venv/bin/activate

# Start the FastAPI server
python -m uvicorn main:app --reload --host 127.0.0.1 --port 8000

