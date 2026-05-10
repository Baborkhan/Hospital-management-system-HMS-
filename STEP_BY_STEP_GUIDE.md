# 🏥 MedFind Bangladesh — সম্পূর্ণ Step-by-Step গাইড
## VS Code Terminal থেকে Live Deploy পর্যন্ত

---

## ✅ এই গাইড পড়লে যা হবে:
- ✅ Local PC-তে run করতে পারবে
- ✅ GitHub-এ push হবে
- ✅ Render-এ backend auto-deploy হবে  
- ✅ Firebase-এ frontend auto-deploy হবে
- ✅ AI (Gemini) কাজ করবে
- ✅ OTP email পাঠাবে
- ✅ Real-time database update হবে

---

## 📋 প্রথমে যা লাগবে (Install করো)

| Tool | Download Link |
|------|--------------|
| VS Code | https://code.visualstudio.com |
| Git | https://git-scm.com/downloads |
| Python 3.11+ | https://www.python.org/downloads |
| Node.js 20+ | https://nodejs.org |

---

## 🗂️ PHASE 1 — Project Setup (VS Code Terminal)

### Step 1: ZIP extract করো ও VS Code-এ open করো

```bash
# Windows: zip থেকে extract করে folder open করো
# তারপর VS Code-এ:
# File → Open Folder → medfind_FINAL_FIXED folder select করো
```

### Step 2: VS Code Terminal খোলো
```
Ctrl + ` (backtick key)
```

---

## 🐍 PHASE 2 — Backend Setup

### Step 3: Python Virtual Environment তৈরি করো

```bash
# terminal-এ এই commands একটার পর একটা চালাও:

cd backend

python -m venv venv

# Windows:
venv\Scripts\activate

# Mac/Linux:
source venv/bin/activate

# দেখবে terminal-এ (venv) লেখা আসবে ✅
```

### Step 4: Dependencies install করো

```bash
pip install -r requirements_render.txt
```

> ⏳ 2-3 মিনিট লাগবে। শেষ হলে "Successfully installed" দেখাবে।

### Step 5: .env file তৈরি করো (SECRET CONFIG)

```bash
# backend folder-এ .env নামে file তৈরি করো
# VS Code-এ: New File → .env
```

`.env` file-এ এটা লেখো:
```env
DEBUG=True
SECRET_KEY=medfind-super-secret-key-change-in-production-2026
GEMINI_API_KEY=AIzaSyAJGKkaMB4ixVPmd5r-cRR1e5ea4AxKmwQ
EMAIL_HOST_USER=তোমার_gmail@gmail.com
EMAIL_HOST_PASSWORD=তোমার_gmail_app_password
ALLOWED_HOSTS=localhost,127.0.0.1
```

> ⚠️ **Gmail App Password পাওয়ার উপায়:**
> 1. Gmail → Settings (⚙️) → Account → Security
> 2. "2-Step Verification" চালু করো
> 3. "App passwords" → Select app: Mail → Generate
> 4. 16-character password পাবে → এটাই EMAIL_HOST_PASSWORD

### Step 6: Database migrate করো

```bash
python manage.py migrate --settings=medfind_project.settings
```

> ✅ "Applying..." messages দেখবে — এটাই OTP table, AI table সব তৈরি হচ্ছে

### Step 7: Backend চালু করো

```bash
python manage.py runserver --settings=medfind_project.settings
```

> ✅ দেখবে: `Starting development server at http://127.0.0.1:8000/`

**নতুন terminal tab খোলো** (Ctrl+Shift+` ) এবং test করো:
```bash
curl http://127.0.0.1:8000/api/v1/health/
```
Output হবে: `{"status": "ok", "service": "MedFind Bangladesh API"}`  ✅

---

## 🌐 PHASE 3 — Frontend চালু করো (Local Test)

### Step 8: নতুন terminal-এ frontend চালাও

```bash
# root folder-এ যাও (backend থেকে বের হয়ে)
cd ..

# Python দিয়ে simple server:
cd frontend
python -m http.server 5500
```

Browser-এ: **http://localhost:5500** → MedFind দেখবে ✅

---

## 🧪 PHASE 4 — Test করো (Local)

### Test 1: AI কাজ করছে কিনা
```bash
curl -X POST http://127.0.0.1:8000/api/v1/ai/chat/ \
  -H "Content-Type: application/json" \
  -d '{"messages":[{"role":"user","content":"Hello, I have fever"}]}'
```
✅ Response পাবে Gemini থেকে

### Test 2: OTP কাজ করছে কিনা
```bash
curl -X POST http://127.0.0.1:8000/api/v1/accounts/send-otp/ \
  -H "Content-Type: application/json" \
  -d '{"email":"তোমার_email@gmail.com"}'
```
✅ Email পাবে 30 সেকেন্ডের মধ্যে

### Test 3: Health check
```bash
curl http://127.0.0.1:8000/api/v1/health/
```
✅ `{"status":"ok","ai":"gemini"}` দেখাবে

---

## 🔥 PHASE 5 — GitHub Push করো

### Step 9: Git initialize ও push

```bash
# root folder-এ যাও
cd .. 

# (যদি এখনো git init না হয়)
git init
git branch -M main
git remote add origin https://github.com/Baborkhan/MedFind-Bangladesh-AI-Healthcare-Platform.git

# সব files add করো
git add -A

# Commit করো
git commit -m "MedFind Bangladesh v3.0 — Production Ready"

# Push করো
git push -u origin main --force
```

> ⚠️ `--force` প্রথমবার লাগবে কারণ GitHub-এ পুরনো files আছে

> 🔑 GitHub username + password চাইবে:
> - Username: `Baborkhan`
> - Password: GitHub Personal Access Token (নিচে দেখো)

**GitHub Token পাওয়ার উপায়:**
1. GitHub → Settings → Developer Settings → Personal Access Tokens → Tokens (classic)
2. Generate new token → Select: `repo`, `workflow` scopes
3. Copy token → এটাই password হিসেবে দাও

---

## ☁️ PHASE 6 — Render Backend Deploy

### Step 10: Render-এ Environment Variables সেট করো

1. https://dashboard.render.com → তোমার service click করো
2. **Environment** tab → **Add Environment Variable**

এই variables গুলো একে একে add করো:

| Key | Value |
|-----|-------|
| `DJANGO_SETTINGS_MODULE` | `medfind_project.settings_render` |
| `GEMINI_API_KEY` | `AIzaSyAJGKkaMB4ixVPmd5r-cRR1e5ea4AxKmwQ` |
| `EMAIL_HOST_USER` | তোমার_gmail@gmail.com |
| `EMAIL_HOST_PASSWORD` | তোমার_16_digit_app_password |
| `SECRET_KEY` | যেকোনো random 50+ character string |
| `DEBUG` | `False` |
| `ALLOWED_HOSTS` | `.onrender.com` |

3. **Save Changes** → Render automatically redeploy করবে ⏳

### Step 11: Render Deploy Status check করো

```bash
# terminal থেকে health check:
curl https://medfind-bangladesh-ai-healthcare-platform.onrender.com/api/v1/health/
```

> ⏳ প্রথমবার 3-5 মিনিট লাগবে (free tier cold start)
> ✅ `{"status":"ok","ai":"gemini"}` দেখলে সফল!

---

## 🔥 PHASE 7 — Firebase Frontend Deploy

### Step 12: Firebase CLI setup

```bash
# Node.js terminal-এ (root folder থেকে):
npm install -g firebase-tools

firebase login
# Browser খুলবে → Google account দিয়ে login করো

# Project connect করো:
firebase use medfind-bangladesh
```

### Step 13: Firebase-এ deploy করো

```bash
firebase deploy --only hosting
```

> ✅ দেখবে: `Hosting URL: https://medfind-bangladesh.web.app`

---

## 🤖 PHASE 8 — GitHub Actions Auto-Deploy Setup

### Step 14: Firebase Token নাও

```bash
firebase login:ci
```
> একটা long token পাবে — copy করে রাখো

### Step 15: GitHub Secrets add করো

1. https://github.com/Baborkhan/MedFind-Bangladesh-AI-Healthcare-Platform/settings/secrets/actions
2. **New repository secret** click করো

এই দুটো secret add করো:

| Name | Value |
|------|-------|
| `FIREBASE_TOKEN` | firebase login:ci থেকে পাওয়া token |
| `RENDER_DEPLOY_HOOK_URL` | Render → Service → Settings → Deploy Hook URL |

> **Render Deploy Hook পাওয়ার উপায়:**
> Render Dashboard → তোমার service → Settings → Deploy Hook → Copy URL

### Step 16: Auto-deploy test করো

```bash
# কোনো ছোট change করো (যেমন README.md update)
echo "# Updated $(date)" >> README.md

git add -A
git commit -m "test: CI/CD auto-deploy"
git push origin main
```

এরপর GitHub → Actions tab-এ দেখো:
- ✅ Lint check pass
- ✅ Backend deployed to Render
- ✅ Frontend deployed to Firebase

---

## 🗄️ PHASE 9 — Database Real-Time Check

### PostgreSQL (Render) — OTP ও AI Data
```bash
# Render logs-এ দেখো:
# Dashboard → Your Service → Logs

# এরকম দেখবে:
# ✅ GEMINI_API_KEY configured
# ✅ EMAIL configured: your@gmail.com
# Applying migrations...
```

### Firestore (Firebase) — Hospital, Patient, Appointment Data
1. https://console.firebase.google.com/project/medfind-bangladesh/firestore
2. Real-time data দেখা যাবে:
   - `hospitals/` collection → bed availability
   - `appointments/` collection → patient appointments
   - `users/` collection → all user profiles
   - `notifications/` collection → realtime alerts

**Real-time test করার উপায়:**
1. Browser-এ Hospital List page খোলো
2. আরেকটি tab-এ Firebase Console → `hospitals` collection
3. কোনো hospital document-এর `availBeds` value change করো
4. প্রথম tab-এ automatically update হবে! ✅

---

## 🔐 PHASE 10 — OTP System Live Test

### Terminal থেকে test:
```bash
# OTP পাঠাও:
curl -X POST https://medfind-bangladesh-ai-healthcare-platform.onrender.com/api/v1/accounts/send-otp/ \
  -H "Content-Type: application/json" \
  -d '{"email":"তোমার@gmail.com"}'

# Response হবে:
# {"success": true, "message": "OTP sent to your email. It expires in 2 minutes."}

# ✅ Gmail inbox দেখো — সুন্দর HTML email আসবে
```

### Browser থেকে test:
1. https://medfind-bangladesh.web.app/pages/login.html
2. OTP tab click করো
3. Email দাও → "Send OTP" click করো
4. Gmail দেখো → 6-digit code নাও → Enter করো
5. ✅ Login হয়ে যাবে

---

## ❗ Common Problems ও Solutions

| Error | Solution |
|-------|----------|
| `ModuleNotFoundError: google.genai` | `pip install google-genai>=1.5.0` |
| `SMTP authentication failed` | Gmail App Password সঠিকভাবে দাও (16 digits, no spaces) |
| AI returns 503 | Render-এ `GEMINI_API_KEY` সেট করা হয়েছে কিনা দেখো |
| Firebase deploy fails | `firebase login` করো আবার, token expired হতে পারে |
| `git push` rejected | `git push -u origin main --force` চালাও |
| Render cold start (30s) | প্রথম request এ স্বাভাবিক — free tier এ হয় |
| OTP not received | Spam folder দেখো / Gmail App Password verify করো |
| CORS error browser | Render-এ `CORS_ALLOWED_ORIGINS` সঠিক আছে কিনা দেখো |

---

## 📱 সব কিছু ঠিকঠাক হলে

| Service | URL | Status |
|---------|-----|--------|
| Frontend | https://medfind-bangladesh.web.app | 🟢 Live |
| Backend | https://medfind-bangladesh-ai-healthcare-platform.onrender.com/api/v1/health/ | 🟢 Live |
| AI Chat | /pages/medfind-ai.html | 🟢 Gemini Powered |
| OTP Login | /pages/login.html | 🟢 Gmail SMTP |
| Hospital List | /pages/hospital/list.html | 🟢 Firestore Realtime |
| Patient Dashboard | /pages/patients/dashboard.html | 🟢 Realtime Updates |

---

## 🔄 Future: কোড Update করার উপায়

```bash
# যেকোনো change করার পরে শুধু:
git add -A
git commit -m "আপনার পরিবর্তনের বিবরণ"
git push origin main

# ✅ GitHub Actions automatically:
# 1. Code check করবে
# 2. Render-এ backend update করবে
# 3. Firebase-এ frontend update করবে
```

---

**🎉 MedFind Bangladesh এখন 100% Production Ready!**
