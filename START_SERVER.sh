#!/bin/bash
# ═══════════════════════════════════════════════════════════
#  MedFind — One-Command Backend Starter
#  Developer: Ahsanul Yamin Babor | github.com/Baborkhan
# ═══════════════════════════════════════════════════════════
echo ""
echo "╔═══════════════════════════════════════════════════╗"
echo "║     🏥 MedFind Backend Server                     ║"
echo "║     Developer: Ahsanul Yamin Babor                ║"  
echo "╚═══════════════════════════════════════════════════╝"
echo ""

cd "$(dirname "$0")/backend"

# Check Python
if ! command -v python3 &> /dev/null; then
    echo "❌ Python3 not found. Install Python 3.11+ first."
    exit 1
fi

# Create venv if missing
if [ ! -d "venv" ]; then
    echo "📦 Creating virtual environment..."
    python3 -m venv venv
fi

# Activate venv
source venv/bin/activate 2>/dev/null || source venv/Scripts/activate 2>/dev/null

# Install deps
echo "📦 Installing dependencies..."
pip install -r requirements.txt -q

# Run migrations
echo "🗃️  Running migrations..."
DJANGO_SETTINGS_MODULE=config.settings.dev python manage.py migrate --run-syncdb 2>/dev/null

# Start server
echo ""
echo "✅ Starting MedFind backend server..."
echo "   API URL: http://127.0.0.1:8000/api/v1/"
echo "   Admin:   http://127.0.0.1:8000/admin/"
echo "   Login:   admin@medfind.com / Admin@12345"
echo ""
echo "   Open frontend/index.html with Live Server"
echo ""
DJANGO_SETTINGS_MODULE=config.settings.dev python manage.py runserver 8000

# ─────────────────────────────────────────────────────────────
# PRODUCTION: use deployment/deploy.sh instead of this script
# ─────────────────────────────────────────────────────────────
