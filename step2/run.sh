#!/bin/bash

# Default port
PORT=${1:-8000}

# Start FastAPI backend (in background)
uvicorn backend.main:app --reload --port $PORT &

# Wait for backend to start
sleep 2

# Export backend URL for frontend
export BACKEND_URL="http://localhost:$PORT"

# Start Streamlit frontend
streamlit run frontend/app.py

# When script is terminated, kill the background process
trap "trap - SIGTERM && kill -- -$$" SIGINT SIGTERM EXIT 