#!/bin/bash
# MedFind Bangladesh — One-command local start (Mac/Linux)

echo ""
echo "╔══════════════════════════════════════════╗"
echo "║   MedFind Bangladesh — Starting Up...   ║"
echo "╚══════════════════════════════════════════╝"
echo ""

cd backend

# Create venv if needed
if [ ! -f "venv/bin/activate" ]; then
    echo "Creating Python virtual environment..."
    python3 -m venv venv
fi

source venv/bin/activate

echo "Installing dependencies..."
pip install -r requirements_render.txt -q

echo "Running migrations..."
python manage.py migrate --settings=medfind_project.settings -v 0

echo "Starting backend on http://127.0.0.1:8000..."
python manage.py runserver --settings=medfind_project.settings &
BACKEND_PID=$!

sleep 2

echo "Starting frontend on http://localhost:5500..."
cd ../frontend
python3 -m http.server 5500 &
FRONTEND_PID=$!

sleep 1
echo ""
echo "════════════════════════════════════════"
echo "✅ MedFind is running!"
echo "🌐 Frontend: http://localhost:5500"
echo "⚙️  Backend:  http://127.0.0.1:8000"
echo "🤖 Health:   http://127.0.0.1:8000/api/v1/health/"
echo ""
echo "Press Ctrl+C to stop both servers"
echo "════════════════════════════════════════"

# Open browser (Mac)
if command -v open &> /dev/null; then
    open http://localhost:5500
fi

# Wait for Ctrl+C
wait $BACKEND_PID $FRONTEND_PID
