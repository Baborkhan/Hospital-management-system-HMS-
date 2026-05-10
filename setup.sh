#!/bin/bash
# ============================================================
# MedFind Django Backend - One-Command Setup
# ============================================================
set -e
cd "$(dirname "$0")"

echo ""
echo "╔══════════════════════════════════════════════╗"
echo "║     MedFind Bangladesh - Backend Setup       ║"
echo "╚══════════════════════════════════════════════╝"
echo ""

# Python version check
python3 -c "import sys; assert sys.version_info >= (3,10), 'Python 3.10+ required'" 2>/dev/null \
  || { echo "❌ Python 3.10+ required"; exit 1; }

echo "📦 Installing dependencies..."
pip install -r requirements/base.txt -q
echo "✓ Dependencies installed"

echo ""
echo "🗄️  Running database migrations..."
python manage.py makemigrations --settings=config.settings.dev
python manage.py migrate --settings=config.settings.dev
echo "✓ Database ready (SQLite)"

echo ""
echo "🌱 Seeding sample data..."
python seed_data.py
echo "✓ Sample data loaded"

echo ""
echo "📁 Collecting static files..."
mkdir -p static staticfiles
python manage.py collectstatic --noinput --settings=config.settings.dev 2>/dev/null || true

echo ""
echo "╔══════════════════════════════════════════════╗"
echo "║  ✅  Setup Complete!                         ║"
echo "║                                              ║"
echo "║  Start server:                               ║"
echo "║  python manage.py runserver 0.0.0.0:8000    ║"
echo "║                                              ║"
echo "║  API base: http://localhost:8000/api/v1/     ║"
echo "║  Django admin: http://localhost:8000/admin/  ║"
echo "╚══════════════════════════════════════════════╝"
