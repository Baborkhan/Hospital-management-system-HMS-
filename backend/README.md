# MedFind Backend — Django REST API

## Stack
- Django 4.x + Django REST Framework
- PostgreSQL (primary DB)
- MongoDB (medical records, doctors, hospitals)
- Redis (sessions, Celery, WebSocket)
- Celery (async tasks)
- Django Channels / Daphne (WebRTC signalling)

## Quick Start (Development)

```bash
cd backend
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
cp .env.example .env    # Fill in your values
python manage.py migrate --settings=config.settings.dev
python manage.py runserver --settings=config.settings.dev
```

## Production Deployment

```bash
# 1. Set env vars (never hardcode)
export DJANGO_SETTINGS_MODULE=config.settings.prod

# 2. Collect static files
python manage.py collectstatic --noinput

# 3. Run migrations
python manage.py migrate

# 4. Start with Gunicorn + Daphne
gunicorn config.wsgi:application --workers 4 --bind 0.0.0.0:8000
daphne -b 0.0.0.0 -p 8001 config.asgi:application
```

## Pre-Deployment Checklist

- [ ] `.env` filled with production values
- [ ] `DEBUG=False` in .env
- [ ] `SSLCOMMERZ_IS_SANDBOX=False` in .env
- [ ] `SECRET_KEY` is a strong random 50+ char string
- [ ] DB backups configured (`scripts/backup.sh`)
- [ ] HTTPS / SSL enabled on domain
- [ ] `ALLOWED_HOSTS` set to real domain
- [ ] `CORS_ALLOWED_ORIGINS` set to real frontend URL
- [ ] `SEED_*_PASS` changed if seed_data.py was run

## Backup

```bash
# Manual backup
bash scripts/backup.sh

# Cron (daily 2am)
0 2 * * * cd /path/to/backend && bash scripts/backup.sh
```
