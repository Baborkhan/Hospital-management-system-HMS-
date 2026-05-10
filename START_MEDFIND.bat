@echo off
title MedFind Bangladesh — Local Development
color 0A
echo.
echo  ╔══════════════════════════════════════════╗
echo  ║   MedFind Bangladesh — Starting Up...   ║
echo  ╚══════════════════════════════════════════╝
echo.

cd backend

:: Check if venv exists
if not exist "venv\Scripts\activate.bat" (
    echo Creating Python virtual environment...
    python -m venv venv
)

:: Activate venv
call venv\Scripts\activate.bat

:: Install dependencies if needed
echo Checking dependencies...
pip install -r requirements_render.txt -q

:: Run migrations
echo Running database migrations...
python manage.py migrate --settings=medfind_project.settings -v 0

:: Start backend in background
echo.
echo Starting Django backend on http://127.0.0.1:8000 ...
start "MedFind Backend" cmd /k "python manage.py runserver --settings=medfind_project.settings"

:: Wait 3 seconds then start frontend
timeout /t 3 /nobreak > nul

:: Start frontend
cd ..\frontend
echo Starting Frontend on http://localhost:5500 ...
start "MedFind Frontend" cmd /k "python -m http.server 5500"

timeout /t 2 /nobreak > nul

:: Open browser
start http://localhost:5500

echo.
echo  ════════════════════════════════════════
echo  ✅ MedFind is running!
echo  🌐 Frontend: http://localhost:5500
echo  ⚙️  Backend:  http://127.0.0.1:8000
echo  🤖 AI Test:  http://127.0.0.1:8000/api/v1/health/
echo  ════════════════════════════════════════
echo.
pause
