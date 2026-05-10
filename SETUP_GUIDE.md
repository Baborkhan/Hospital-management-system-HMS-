# 🏥 MedFind Bangladesh — Setup Guide v3.0

## ⚡ Quick Start (3 Steps)

### Step 1 — Get Anthropic API Key
1. Go to **[console.anthropic.com](https://console.anthropic.com)**
2. Sign Up → Dashboard → **API Keys** → **Create Key**
3. Copy your key: `sk-ant-api03-...`

### Step 2 — Set your API Key
Open `backend/.env` and replace:
```
ANTHROPIC_API_KEY=sk-ant-api03-PASTE-YOUR-KEY-HERE
```

### Step 3 — Start Servers

**Mac/Linux:**
```bash
chmod +x START_LOCAL.sh
./START_LOCAL.sh
```

**Windows:**
```
Double-click START_LOCAL.bat
```

✅ Frontend: http://127.0.0.1:5500  
✅ Backend: http://127.0.0.1:8000  
✅ Admin: http://127.0.0.1:8000/admin

---

## 👤 Admin Login

| Field    | Value                         |
|----------|-------------------------------|
| Email    | ahsanulyaminbabor@gmail.com   |
| Password | medadmin146199                |
| Role     | Superadmin                    |

---

## 🤖 How AI Works

```
User types → Frontend → Django /api/v1/ai/chat/ → Anthropic API
                           ↑ Your API key lives here (safe)
```

Users **never** need to enter an API key.  
The key stays in `backend/.env` — never exposed to browser.

---

## 📧 Gmail Setup (Email Notifications)

Gmail এ **App Password** দরকার (not your main password):

1. Google Account → Security → **2-Step Verification** ON করুন
2. Security → **App passwords** → "Mail" select → Generate
3. Generated 16-char password টা `.env` এ দিন:

```env
EMAIL_HOST_USER=ahsanulyaminbabor@gmail.com
EMAIL_HOST_PASSWORD=xxxx-xxxx-xxxx-xxxx   ← App Password (16 chars)
```

> ⚠️ `medadmin146199` is your Google account password — Gmail SMTP needs an App Password, not the main password.

---

## 🚀 Production Deployment

### Option A — Render.com (Free)
1. Push to GitHub
2. New Web Service → Connect repo → `backend/`
3. Build: `pip install -r requirements.txt`
4. Start: `gunicorn config.wsgi:application`
5. Add environment variables from `.env`

### Option B — Railway.app (Easy)
```bash
railway up
```

### Option C — Google Cloud Run
```bash
gcloud run deploy medfind-backend --source backend/
```

After deploy, update `frontend/assets/js/config.js`:
```js
const PRODUCTION_API_URL = 'https://your-deployed-url.com/api/v1';
```

---

## 🛠️ Manual Backend Setup

```bash
cd backend

# Install dependencies
pip install -r requirements-local.txt

# Run migrations
DJANGO_SETTINGS_MODULE=config.settings.dev python manage.py migrate

# Create admin
DJANGO_SETTINGS_MODULE=config.settings.dev python manage.py createsuperuser

# Start server
DJANGO_SETTINGS_MODULE=config.settings.dev python manage.py runserver
```

---

## 📁 Project Structure

```
medfind_fixed/
├── START_LOCAL.sh          ← Mac/Linux one-click start
├── START_LOCAL.bat         ← Windows one-click start
├── SETUP_GUIDE.md          ← This file
├── backend/
│   ├── .env                ← Your API keys (never commit!)
│   ├── manage.py
│   ├── requirements-local.txt  ← Minimal for local dev
│   ├── requirements.txt    ← Full production requirements
│   ├── ai/                 ← AI proxy (routes to Anthropic)
│   │   ├── views.py        ← ProxyAIChatView
│   │   └── urls.py
│   ├── apps/
│   │   ├── accounts/       ← Login, Register, JWT auth
│   │   ├── patients/       ← Patient management
│   │   ├── doctors/        ← Doctor profiles
│   │   └── ...
│   └── config/
│       └── settings/
│           ├── base.py     ← Shared settings
│           ├── dev.py      ← SQLite, console email
│           └── prod.py     ← PostgreSQL, real email
└── frontend/
    ├── index.html          ← Main landing page
    ├── assets/
    │   └── js/
    │       └── config.js   ← Frontend config (API URL etc)
    └── pages/
        ├── medfind-ai.html ← AI Chat interface
        ├── login.html
        ├── register.html
        └── patients/
            ├── dashboard.html
            ├── profile.html
            └── medical-history.html
```

---

## ❓ Troubleshooting

| Problem | Solution |
|---------|----------|
| AI says "Connection error" | Start Django server + set ANTHROPIC_API_KEY in .env |
| Login not working | Check browser console, verify Django is running on :8000 |
| Email not sending | Use Gmail App Password (not main password) |
| CORS error | Add your frontend URL to CORS_ALLOWED_ORIGINS in .env |
| Migration error | Delete db.sqlite3 and run migrate again |

---

## 📹 Video Call System — How It Works

```
Doctor (telemedicine.html)          Patient (video-join.html)
        |                                    |
        |── WebSocket ──────────────────────>|
        |   ws://host:8000/ws/session/{id}/  |
        |                                    |
        |<── offer (SDP) ──────────────────>|
        |<── ICE candidates ──────────────>|
        |                                    |
        |══ RTCPeerConnection (P2P video) ══|
```

### Requirements for Video Call
- **Daphne** must be running (not plain `runserver`)
- `START_LOCAL.sh` / `START_LOCAL.bat` handles this automatically

### Test Video Call Locally
1. Start servers: `./START_LOCAL.sh`
2. Doctor: `http://127.0.0.1:5500/telemedicine.html?session=test123`
3. Patient: `http://127.0.0.1:5500/pages/patients/video-join.html?session=test123`
4. Both open in same browser (different tabs) or different browsers

### Production TURN Server (Required for real users)
Without TURN, calls fail when both users are behind NAT (mobile networks, etc).

Free TURN: **Metered.ca** or **Twilio TURN**
```env
TURN_SERVER_URL=turn:your-turn-server.com:3478
TURN_SERVER_USER=your-username
TURN_SERVER_PASS=your-password
```
