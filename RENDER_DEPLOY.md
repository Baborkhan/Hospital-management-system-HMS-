# 🚀 MedFind Bangladesh — Render.com Deploy Guide

## সমস্যাগুলো যা fix হয়েছে

| # | সমস্যা | Fix |
|---|--------|-----|
| 1 | `TemplateDoesNotExist at /` | `urls.py` থেকে `TemplateView` সরিয়ে health check দেওয়া হয়েছে |
| 2 | AI "Connection error" | `config.js` এ Render URL সেট হয়েছে |
| 3 | Render build fail | নতুন `settings_render.py` ও `requirements_render.txt` তৈরি |

---

## Step 1 — GitHub এ push করুন

```bash
cd medfind_FIXED
git add -A
git commit -m "fix: Render deployment - settings, urls, config"
git push origin main
```

---

## Step 2 — Render Dashboard Settings

Render Dashboard → Your Service → **Environment** → এই variables গুলো set করুন:

| Variable | Value |
|----------|-------|
| `DJANGO_SETTINGS_MODULE` | `medfind_project.settings_render` |
| `SECRET_KEY` | (যেকোনো random string, 50+ chars) |
| `DEBUG` | `False` |
| `ALLOWED_HOSTS` | `.onrender.com,medfind-bangladesh-ai-healthcare-platform.onrender.com` |
| `GEMINI_API_KEY` | আপনার Gemini API key |
| `EMAIL_HOST_USER` | `ahsanulyaminbabor@gmail.com` |
| `EMAIL_HOST_PASSWORD` | Gmail App Password |
| `CORS_ALLOWED_ORIGINS` | `https://medfind-bangladesh.web.app` |
| `CSRF_TRUSTED_ORIGINS` | `https://medfind-bangladesh-ai-healthcare-platform.onrender.com,https://medfind-bangladesh.web.app` |

---

## Step 3 — Render Build & Start Commands

Settings → Build Command:
```
pip install -r requirements_render.txt && python manage.py migrate --noinput && python manage.py collectstatic --noinput
```

Start Command:
```
gunicorn medfind_project.wsgi:application --bind 0.0.0.0:$PORT --workers 2 --timeout 120
```

---

## Step 4 — Test করুন

Backend live হলে এই URL এ JSON দেখবেন:
```
https://medfind-bangladesh-ai-healthcare-platform.onrender.com/
```
Response:
```json
{"status": "ok", "service": "MedFind Bangladesh API", "version": "3.0", "ai": "gemini"}
```

AI test:
```
https://medfind-bangladesh-ai-healthcare-platform.onrender.com/api/v1/ai/chat/
```

---

## Step 5 — Frontend (Firebase) Config

`frontend/assets/js/config.js` এ ইতিমধ্যে Render URL সেট হয়েছে:
```js
const PRODUCTION_API_URL = 'https://medfind-bangladesh-ai-healthcare-platform.onrender.com/api/v1';
```

Firebase deploy:
```bash
firebase deploy --only hosting
```

---

## ⚠️ Important Notes

- Render **free tier** এ প্রথম request আসতে ~30 সেকেন্ড লাগে (cold start) — এটা normal
- PostgreSQL না থাকলে SQLite ব্যবহার হবে (free tier এ ঠিক আছে)
- Redis নেই — local memory cache ব্যবহার হবে
