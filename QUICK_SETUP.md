# ⚡ MedFind Bangladesh — Quick Setup Checklist
## Last Updated: 2026-05-07

---

## ✅ What's Already Done (Code)
- [x] All API URLs fixed (was using /api/v1 relative, now points to Render)
- [x] Firestore realtime: hospital bed availability + patient appointments
- [x] OTP system: send/verify/resend/rate-limit (2 min expiry)  
- [x] CI/CD: GitHub Actions → Render + Firebase auto-deploy
- [x] Gemini AI: SDK → REST fallback chain
- [x] WebSocket URL fixed for production
- [x] Patient dashboard: real-time Firestore notifications

---

## 🔑 Step 1: Add Gemini API Key to Render

1. Go to: https://dashboard.render.com
2. Click your service → **Environment**
3. Add these variables:

```
GEMINI_API_KEY = AIzaSyAJGKkaMB4ixVPmd5r-cRR1e5ea4AxKmwQ
EMAIL_HOST_USER = your-gmail@gmail.com
EMAIL_HOST_PASSWORD = your-gmail-app-password (NOT regular password)
```

> **Gmail App Password**: Gmail → Account → Security → 2-Step Verification → App Passwords

---

## 🔑 Step 2: Add Secrets to GitHub

1. Go to: https://github.com/Baborkhan/MedFind-Bangladesh-AI-Healthcare-Platform/settings/secrets/actions
2. Add these secrets:

| Secret Name | How to Get |
|---|---|
| `FIREBASE_TOKEN` | Run: `firebase login:ci` locally |
| `RENDER_DEPLOY_HOOK_URL` | Render Dashboard → Service → Settings → Deploy Hook |

---

## 🚀 Step 3: Push to GitHub

```bash
cd medfind_FIXED
git push origin main
```

GitHub Actions will automatically:
- ✅ Run syntax checks
- ✅ Deploy backend to Render (~2 min)
- ✅ Deploy frontend to Firebase (~1 min)

---

## 🧪 Test Checklist

| Test | URL | Expected |
|---|---|---|
| Backend health | https://medfind-bangladesh-ai-healthcare-platform.onrender.com/api/v1/health/ | `{"status":"ok"}` |
| Frontend | https://medfind-bangladesh.web.app | Login page loads |
| OTP send | Login page → OTP tab → enter email | Email received in 30s |
| AI chat | index.html → chat bubble | Response from Gemini |
| Hospital list | /pages/hospital/list.html | Hospitals show, beds update live |
| Patient dashboard | Login → patient → dashboard | Appointments update live |

---

## 🔥 Firebase: One-Time Setup

```bash
# Install Firebase CLI
npm install -g firebase-tools

# Login
firebase login

# Get CI token (add to GitHub secrets)
firebase login:ci

# Deploy manually (first time)
firebase deploy --only hosting --project medfind-bangladesh
```

---

## URLs
- 🌐 Frontend: https://medfind-bangladesh.web.app
- ⚙️ Backend: https://medfind-bangladesh-ai-healthcare-platform.onrender.com
- 📊 GitHub Actions: https://github.com/Baborkhan/MedFind-Bangladesh-AI-Healthcare-Platform/actions
