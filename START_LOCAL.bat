@echo off
:: MedFind Bangladesh — Windows One-Click Start
title MedFind Bangladesh — Dev Server

echo.
echo ╔══════════════════════════════════════════════╗
echo ║     MedFind Bangladesh — v3.0               ║
echo ║        Starting Development Server           ║
echo ╚══════════════════════════════════════════════╝
echo.

cd /d "%~dp0backend"

echo [1/4] Checking Python packages...
pip install -r requirements-local.txt --quiet

echo [2/4] Running migrations...
set DJANGO_SETTINGS_MODULE=config.settings.dev
python manage.py migrate --run-syncdb --verbosity=0

echo [3/4] Creating admin account...
python manage.py shell -c "from apps.accounts.models import User; User.objects.filter(email='ahsanulyaminbabor@gmail.com').exists() or User.objects.create_superuser(email='ahsanulyaminbabor@gmail.com', password='medadmin146199', full_name='Ahsanul Yamin Babor')"

echo [4/4] Starting servers...
start "MedFind Backend" cmd /k "set DJANGO_SETTINGS_MODULE=config.settings.dev && python -m daphne -b 0.0.0.0 -p 8000 config.asgi:application || python manage.py runserver 0.0.0.0:8000"

cd /d "%~dp0frontend"
start "MedFind Frontend" cmd /k "python -m http.server 5500"

echo.
echo ╔══════════════════════════════════════════════╗
echo ║  Frontend:  http://127.0.0.1:5500           ║
echo ║  Backend:   http://127.0.0.1:8000           ║
echo ║  Admin:     http://127.0.0.1:8000/admin     ║
echo ╚══════════════════════════════════════════════╝
echo.
pause
