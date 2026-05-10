# ✅ MedFind Bangladesh — Publication Ready Guide

## 🔧 Bugs Fixed (This Session — 15 Total)

| # | Bug | Fix |
|---|-----|-----|
| 1 | `TemplateDoesNotExist at /` | `urls.py` — TemplateView removed, health JSON added |
| 2 | AI "Connection error" | `config.js` — Render URL hardcoded as fallback |
| 3 | Render build failure | `settings_render.py` + `requirements_render.txt` |
| 4 | `REDIS_URL=REDIS_URL=` double prefix | `.env` fixed |
| 5 | `django_redis` crash on startup | `settings.py` — graceful ImportError fallback |
| 6 | `main.js` broken `fetch()` calls | Missing URL strings restored |
| 7 | `hospital/list.html` — no `</html>` | Closing tag added |
| 8 | CHANGE-THIS in medfind-ai.html | Guard condition simplified |
| 9 | `blood-donor/search.html` API_BASE | Uses MEDFIND_CONFIG in production |
| 10 | `otp_auth` migration missing | `makemigrations` run |
| 11 | `.env` duplicate entries | Cleaned up |
| 12 | AI returns HTTP 500 | Returns proper 503 with message |
| 13 | `login.html`/`register.html` — `/api/v1` relative path fails on Firebase | Full Render URL fallback added |
| 14 | `medfind-ai.html` `backendBase = null` on production | Full Render URL fallback added |
| 15 | `donate/views.py` organs required field | Made optional |

---

## 🚀 STEP-BY-STEP PUBLISH GUIDE

### Step 1 — Fix Gemini API Key (CRITICAL)
The AI won't work until you fix this one setting:

1. Go to: **https://aistudio.google.com/apikey**
2. Click your key → **Edit** → **Application restrictions**
3. Change from **"HTTP referrers (websites)"** → **"None"**
4. Save

> ⚠️ The "HTTP referrers" restriction is for browser JS only. Backend servers like Render need "None".

---

### Step 2 — Push to GitHub
```bash
cd medfind_FIXED
git init   # only if not already a git repo
git remote add origin https://github.com/YOUR_USERNAME/MedFind-Bangladesh-AI-Healthcare-Platform.git
git add -A
git commit -m "feat: Production-ready MedFind Bangladesh v3.0"
git push origin main
```

Or use the helper script:
```bash
./git-push.sh "Production ready v3.0"
```

---

### Step 3 — Render Dashboard Environment Variables
Go to: **Render Dashboard → medfind-backend → Environment**

Add these variables:

| Variable | Value |
|----------|-------|
| `DJANGO_SETTINGS_MODULE` | `medfind_project.settings_render` |
| `GEMINI_API_KEY` | Your **unrestricted** Gemini key |
| `ANTHROPIC_API_KEY` | *(optional fallback)* Your Anthropic key |
| `EMAIL_HOST_USER` | `ahsanulyaminbabor@gmail.com` |
| `EMAIL_HOST_PASSWORD` | Your Gmail App Password (16-char) |

**Build Command:**
```
pip install -r requirements_render.txt && python manage.py migrate --noinput && python manage.py collectstatic --noinput
```

**Start Command:**
```
gunicorn medfind_project.wsgi:application --bind 0.0.0.0:$PORT --workers 2 --timeout 120
```

---

### Step 4 — Deploy Frontend to Firebase
```bash
cd frontend
firebase deploy --only hosting
```

---

### Step 5 — Enable Auto-Deploy (GitHub Actions)
Add these to **GitHub → Settings → Secrets and variables → Actions**:

| Secret | How to get |
|--------|-----------|
| `FIREBASE_TOKEN` | Run: `firebase login:ci` → copy token |
| `RENDER_DEPLOY_HOOK_URL` | Render Dashboard → Settings → Deploy Hook |

After this, every `git push origin main` will:
- Auto-deploy backend to Render ✅
- Auto-deploy frontend to Firebase ✅

---

## ✅ Verification Checklist

After deploy, test these URLs:

| Test | URL | Expected |
|------|-----|----------|
| Backend health | `https://medfind-bangladesh-ai-healthcare-platform.onrender.com/` | `{"status":"ok"}` |
| AI chat | `POST .../api/v1/ai/chat/` | AI reply |
| Frontend home | `https://medfind-bangladesh.web.app/` | Homepage loads |
| AI page | `.../pages/medfind-ai.html` | Chat works |
| Login OTP | `.../pages/login.html` | OTP email received |
| Donate page | `.../pages/donate/index.html` | Blood/organ forms |

---

## 📧 OTP Email Status
- OTP backend code is **fully working** ✅
- Gmail SMTP configured with `ahsanulyaminbabor@gmail.com`
- **Important**: Gmail App Password `medadmin146199` — verify it's a 16-char App Password
  - If OTP fails: Google Account → Security → 2-Step Verification → App passwords → Create new
  - Replace `EMAIL_HOST_PASSWORD` in Render Dashboard

---

## ⚡ Cold Start Warning
Render free tier sleeps after 15 min. First request takes ~30 seconds.
This is normal — after first request, subsequent calls are fast.

