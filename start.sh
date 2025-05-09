#!/bin/bash

# --- Load env variables ---
echo "Loading environment variables..."
export $(grep -v '^#' apikey.env | xargs)

# --- Install Python dependencies ---
echo "Installing Python dependencies..."
cd backend
pip install -r requirements.txt || pip install "groq" "fastapi[all]" "uvicorn[standard]" "python-dotenv"

# --- Start backend in background ---
echo "Starting FastAPI backend..."
python -m uvicorn main:app --reload &
BACKEND_PID=$!

# --- Start React frontend ---
echo "Starting React frontend..."
cd ../webpage/react-environment
npm install
npm run dev

# --- Cleanup: Kill backend when frontend exits ---
kill $BACKEND_PID
