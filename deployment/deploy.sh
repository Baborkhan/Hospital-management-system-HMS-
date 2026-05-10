#!/bin/bash
# ═══════════════════════════════════════════════════════════════════════
#  MedFind — Production Deploy Script
#  Run on Ubuntu 22.04 server as root or sudo user
#  Usage: bash deploy.sh
# ═══════════════════════════════════════════════════════════════════════
set -e

APP_DIR="/var/www/medfind"
REPO="https://github.com/Baborkhan/medfind.git"   # Update with your repo
BRANCH="main"
VENV="$APP_DIR/venv"
BACKEND="$APP_DIR/backend"

echo ""
echo "╔══════════════════════════════════════════════╗"
echo "║   🏥 MedFind Production Deploy               ║"
echo "╚══════════════════════════════════════════════╝"

# ── 1. System packages ────────────────────────────────────────────────
echo "📦 Installing system packages..."
apt-get update -q
apt-get install -y -q python3.11 python3.11-venv python3-pip \
    postgresql postgresql-contrib redis-server \
    nginx certbot python3-certbot-nginx \
    git curl build-essential libpq-dev

# ── 2. Pull latest code ───────────────────────────────────────────────
echo "📥 Pulling code..."
if [ -d "$APP_DIR/.git" ]; then
    cd "$APP_DIR" && git fetch origin && git reset --hard "origin/$BRANCH"
else
    git clone -b "$BRANCH" "$REPO" "$APP_DIR"
fi

# ── 3. Python venv + dependencies ────────────────────────────────────
echo "🐍 Setting up Python environment..."
python3.11 -m venv "$VENV"
"$VENV/bin/pip" install --upgrade pip -q
"$VENV/bin/pip" install -r "$BACKEND/requirements.txt" -q

# ── 4. Environment file ───────────────────────────────────────────────
if [ ! -f "$APP_DIR/.env" ]; then
    echo "⚠️  .env file not found at $APP_DIR/.env"
    echo "    Copy backend/.env.example → $APP_DIR/.env and fill in values"
    exit 1
fi

# ── 5. Database migrations ────────────────────────────────────────────
echo "🗃️  Running migrations..."
cd "$BACKEND"
DJANGO_SETTINGS_MODULE=config.settings.prod "$VENV/bin/python" manage.py migrate --noinput
DJANGO_SETTINGS_MODULE=config.settings.prod "$VENV/bin/python" manage.py collectstatic --noinput

# ── 6. Logs directory ─────────────────────────────────────────────────
mkdir -p /var/log/medfind "$BACKEND/logs"
chown -R ubuntu:ubuntu /var/log/medfind "$APP_DIR"

# ── 7. systemd services ───────────────────────────────────────────────
echo "⚙️  Installing systemd services..."
cp deployment/medfind-gunicorn.service /etc/systemd/system/
cp deployment/medfind-daphne.service   /etc/systemd/system/
systemctl daemon-reload
systemctl enable  medfind-gunicorn medfind-daphne
systemctl restart medfind-gunicorn medfind-daphne

# ── 8. Nginx ──────────────────────────────────────────────────────────
echo "🌐 Configuring Nginx..."
cp deployment/nginx.conf /etc/nginx/sites-available/medfind
ln -sf /etc/nginx/sites-available/medfind /etc/nginx/sites-enabled/medfind
nginx -t && systemctl reload nginx

echo ""
echo "✅ Deploy complete!"
echo "   Run: certbot --nginx -d medfind.app -d www.medfind.app"
echo "   Then: systemctl reload nginx"
echo ""
