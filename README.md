# 🏥 MedFind Bangladesh — Digital Healthcare Platform

> **Care You Can Trust** — Connecting patients across all 64 districts with doctors, hospitals, blood donors, labs, and AI-powered health tools.

[![Version](https://img.shields.io/badge/version-9.0-blue)](.) [![Pages](https://img.shields.io/badge/pages-38-teal)](.) [![AI](https://img.shields.io/badge/AI-Claude%20Sonnet%204-purple)](.) [![License](https://img.shields.io/badge/license-proprietary-red)](.)

---

## 🚀 Quick Start (VS Code — 2 Steps)

```bash
# 1. Open folder in VS Code
code MEDFIND_FINAL/

# 2. Right-click frontend/index.html → "Open with Live Server"
# → Opens at http://127.0.0.1:5500
```

**That's it! All AI features work immediately** — just add your Anthropic API key when prompted.

---

## ✨ Features

| Feature | Description |
|---------|-------------|
| 🤖 AI Symptom Checker | Differential diagnoses, BD hospitals, BDT costs via Claude AI |
| 💊 AI Drug Directory | 25+ fields, Bangladesh brands, interactions, BDT pricing |
| 🩺 AI Treatment Guide | Clinical protocols, ICD-10, BSMMU/DMCH references |
| 🩸 Blood Donor Network | Search by blood group + district, donor registration, compatibility table |
| 👨‍⚕️ Doctor Search | Find doctors by specialty and district |
| 🏥 Hospital Directory | Hospital profiles, bed availability |
| 🔐 Admin Panel | 3-factor auth (email + phone + OTP) — owner-only access |
| ⚖️ Legal Suite | Privacy Policy, Terms, Medical Disclaimer, Consent Forms, Data Backup Policy |

---

## 🔐 Admin Access

The Admin Dashboard (`pages/admin/dashboard.html`) requires **3-factor authentication**:
1. **Email** — must be in the authorized list in `frontend/assets/js/admin-auth.js`
2. **Phone** — must match registered phone for that email
3. **OTP** — 6-digit code shown in browser DevTools console (F12)

> ⚠️ Only authorized owners can access admin and analytics pages.

---

## 🤖 AI Configuration

AI features call the Anthropic API directly from the browser. To enable:
1. Get your API key: [console.anthropic.com](https://console.anthropic.com)
2. Enter it when prompted by the AI pages
3. For production: route through Django backend to keep key secret

---

## 📁 Structure

```
MEDFIND_FINAL/
├── frontend/
│   ├── index.html                     # Landing page
│   ├── assets/
│   │   ├── medfind-logo.png           # Logo (used on all 38 pages)
│   │   ├── css/                       # Global styles
│   │   └── js/
│   │       ├── components.js          # Shared nav + footer
│   │       └── admin-auth.js          # 3-factor admin guard
│   └── pages/
│       ├── symptoms/index.html        # 🤖 AI Symptom Checker
│       ├── drugs/index.html           # 🤖 AI Drug Directory
│       ├── treatments/index.html      # 🤖 AI Treatment Guide
│       ├── blood-donor/search.html    # Blood Donor Search
│       ├── doctors/search.html        # Doctor Search
│       ├── hospital/list.html         # Hospital Directory
│       ├── admin/dashboard.html       # 🔐 Admin Panel
│       ├── admin/analytics.html       # 🔐 Analytics
│       ├── privacy.html               # Privacy Policy
│       ├── terms.html                 # Terms of Service
│       ├── medical-disclaimer.html    # Medical Disclaimer
│       ├── consent-forms.html         # Patient Consent Forms
│       └── data-backup-policy.html    # Data Backup Policy
├── backend/                           # Django REST API
│   ├── .env.example                   # Copy to .env and configure
│   ├── requirements.txt
│   └── apps/                          # 10 Django apps
├── .gitignore                         # Comprehensive — secrets protected
├── README.md                          # This file
└── MEDFIND_Technical_Guide_v9.docx    # Full technical documentation
```

---

## 🌐 Deploy to GitHub Pages

```bash
git init
git add .
git commit -m "MedFind Bangladesh v9.0"
git remote add origin https://github.com/YOUR_USERNAME/medfind-bangladesh.git
git push -u origin main
# Then: Settings → Pages → Source: main → Save
# Live at: https://YOUR_USERNAME.github.io/medfind-bangladesh/
```

---

## 🔧 Backend Setup (Optional)

```bash
cd backend
python -m venv venv && source venv/bin/activate
pip install -r requirements.txt
cp .env.example .env    # Fill in your values
python manage.py migrate
python manage.py runserver
# → http://127.0.0.1:8000
```

---

## ⚖️ Legal

- **Platform:** MedFind Bangladesh is a patient-doctor connection platform, NOT a medical provider
- **Emergency:** Call 999 (Bangladesh) for medical emergencies — do not use MedFind
- **Privacy:** We never sell user data. Full Privacy Policy at `pages/privacy.html`
- **Disclaimer:** See `pages/medical-disclaimer.html` for full disclaimer

---

## 📞 Contact

| | |
|--|--|
| Email | medfindbd2026@gmail.com |
| Emergency | 01772-172829 |
| DGHS | dghs.gov.bd \| 16430 |

---

*© 2026 MedFind Bangladesh. All rights reserved.*
