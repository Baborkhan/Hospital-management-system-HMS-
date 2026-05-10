#!/usr/bin/env bash
# ═══════════════════════════════════════════════════════════════
#  MedFind Bangladesh — One-Click Local Development Server
# ═══════════════════════════════════════════════════════════════
set -e

GREEN='\033[0;32m'
CYAN='\033[0;36m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
RESET='\033[0m'

echo ""
echo -e "${CYAN}╔══════════════════════════════════════════════╗${RESET}"
echo -e "${CYAN}║     🏥  MedFind Bangladesh — v3.0           ║${RESET}"
echo -e "${CYAN}║        Starting Development Server           ║${RESET}"
echo -e "${CYAN}╚══════════════════════════════════════════════╝${RESET}"
echo ""

PROJECT_DIR="$(cd "$(dirname "$0")" && pwd)"
BACKEND_DIR="$PROJECT_DIR/backend"
FRONTEND_DIR="$PROJECT_DIR/frontend"

# ── Check Python ──
if ! command -v python3 &>/dev/null; then
  echo -e "${RED}❌ Python3 not found. Install from python.org${RESET}"
  exit 1
fi
PYTHON=$(command -v python3)

# ── Check .env ──
if [ ! -f "$BACKEND_DIR/.env" ]; then
  echo -e "${YELLOW}⚠️  .env not found — copying from .env.example${RESET}"
  cp "$BACKEND_DIR/.env.example" "$BACKEND_DIR/.env"
  echo -e "${RED}📌 Edit backend/.env and add your ANTHROPIC_API_KEY${RESET}"
fi

# ── Install dependencies (if needed) ──
echo -e "${CYAN}📦 Checking Python dependencies...${RESET}"
cd "$BACKEND_DIR"
if ! $PYTHON -c "import django" 2>/dev/null; then
  echo -e "${YELLOW}Installing local requirements...${RESET}"
  $PYTHON -m pip install -r requirements-local.txt --quiet
fi

# ── Run migrations ──
echo -e "${CYAN}🗄️  Running database migrations...${RESET}"
DJANGO_SETTINGS_MODULE=config.settings.dev $PYTHON manage.py migrate --run-syncdb --verbosity=0 2>/dev/null || true

# ── Create superadmin if not exists ──
echo -e "${CYAN}👤 Ensuring admin account...${RESET}"
DJANGO_SETTINGS_MODULE=config.settings.dev $PYTHON manage.py shell -c "
from apps.accounts.models import User
if not User.objects.filter(email='ahsanulyaminbabor@gmail.com').exists():
    u = User.objects.create_superuser(
        email='ahsanulyaminbabor@gmail.com',
        password='medadmin146199',
        full_name='Ahsanul Yamin Babor',
    )
    u.role = 'superadmin'
    u.is_verified = True
    u.save()
    print('✅ Superadmin created: ahsanulyaminbabor@gmail.com')
else:
    print('✅ Superadmin already exists')
" 2>/dev/null || echo "  (User model may differ — check manually)"

# ── Start Django backend (Daphne for HTTP + WebSocket) ──
echo ""
if $PYTHON -c "import daphne" 2>/dev/null; then
  echo -e "${GREEN}🚀 Starting Daphne (HTTP + WebSocket) on http://127.0.0.1:8000${RESET}"
  DJANGO_SETTINGS_MODULE=config.settings.dev $PYTHON -m daphne -b 0.0.0.0 -p 8000 config.asgi:application &
else
  echo -e "${YELLOW}⚠️  Daphne not installed — using runserver (no WebSocket/video calls)${RESET}"
  echo -e "${YELLOW}   Run: pip install daphne channels channels-redis${RESET}"
  DJANGO_SETTINGS_MODULE=config.settings.dev $PYTHON manage.py runserver 0.0.0.0:8000 &
fi
BACKEND_PID=$!
echo -e "   PID: ${BACKEND_PID}"
sleep 2

# ── Start frontend (Python simple server) ──
echo ""
echo -e "${GREEN}🌐 Starting frontend on http://127.0.0.1:5500${RESET}"
cd "$FRONTEND_DIR"
$PYTHON -m http.server 5500 &
FRONTEND_PID=$!

# ── Done ──
echo ""
echo -e "${CYAN}╔══════════════════════════════════════════════╗${RESET}"
echo -e "${CYAN}║  ✅  MedFind is running!                     ║${RESET}"
echo -e "${CYAN}║                                              ║${RESET}"
echo -e "${CYAN}║  🌐 Frontend:  http://127.0.0.1:5500         ║${RESET}"
echo -e "${CYAN}║  📡 Backend:   http://127.0.0.1:8000         ║${RESET}"
echo -e "${CYAN}║  🔧 Admin:     http://127.0.0.1:8000/admin   ║${RESET}"
echo -e "${CYAN}║  🤖 AI Proxy:  /api/v1/ai/chat/              ║${RESET}"
echo -e "${CYAN}║                                              ║${RESET}"
echo -e "${CYAN}║  👤 Admin: ahsanulyaminbabor@gmail.com       ║${RESET}"
echo -e "${CYAN}║  🔑 Pass:  medadmin146199                    ║${RESET}"
echo -e "${CYAN}║                                              ║${RESET}"
echo -e "${YELLOW}║  Press Ctrl+C to stop all servers            ║${RESET}"
echo -e "${CYAN}╚══════════════════════════════════════════════╝${RESET}"
echo ""

# ── Cleanup on exit ──
trap "echo ''; echo -e '${RED}Stopping servers...${RESET}'; kill $BACKEND_PID $FRONTEND_PID 2>/dev/null; exit 0" SIGINT SIGTERM
wait
