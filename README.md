<div align="center">

<img src="frontend/assets/medfind-logo.png" alt="MedFind Bangladesh" width="100" height="100" />

# MedFind Bangladesh

### AI-Powered Digital Healthcare Platform

**Find doctors · Book appointments · Get AI health guidance · Donate blood**

<br/>

[![Live Demo](https://img.shields.io/badge/🌐_Live_Demo-medfind--bangladesh.web.app-2563eb?style=for-the-badge)](https://medfind-bangladesh.web.app/)
[![Backend API](https://img.shields.io/badge/Backend_API-Render.com-46E3B7?style=for-the-badge&logo=render&logoColor=white)](https://medfind-bangladesh-ai-healthcare-platform.onrender.com/api/v1/health/)

<br/>

[![Django](https://img.shields.io/badge/Django_4.2-092E20?style=flat-square&logo=django&logoColor=white)](https://djangoproject.com)
[![Python](https://img.shields.io/badge/Python_3.11+-3776AB?style=flat-square&logo=python&logoColor=white)](https://python.org)
[![Firebase](https://img.shields.io/badge/Firebase_Hosting-FFCA28?style=flat-square&logo=firebase&logoColor=black)](https://firebase.google.com)
[![Gemini AI](https://img.shields.io/badge/Gemini_2.0_Flash-4285F4?style=flat-square&logo=google&logoColor=white)](https://ai.google.dev)
[![PostgreSQL](https://img.shields.io/badge/PostgreSQL-4169E1?style=flat-square&logo=postgresql&logoColor=white)](https://postgresql.org)
[![JWT](https://img.shields.io/badge/JWT_Auth-000000?style=flat-square&logo=jsonwebtokens&logoColor=white)](https://jwt.io)
[![License](https://img.shields.io/badge/License-MIT-22c55e?style=flat-square)](LICENSE)
[![Status](https://img.shields.io/badge/Status-Live_&_Active-22c55e?style=flat-square)]()

<br/>

> **MedFind Bangladesh** is a comprehensive AI-powered healthcare platform connecting patients with doctors, hospitals, blood donors, and medical resources across Bangladesh — in Bangla & English.

<br/>

[🌐 Live Website](https://medfind-bangladesh.web.app/) &nbsp;·&nbsp; [📡 API Health](https://medfind-bangladesh-ai-healthcare-platform.onrender.com/api/v1/health/) &nbsp;·&nbsp; [🐛 Report Bug](https://github.com/Baborkhan/MedFind-Bangladesh-AI-Healthcare-Platform/issues) &nbsp;·&nbsp; [✨ Request Feature](https://github.com/Baborkhan/MedFind-Bangladesh-AI-Healthcare-Platform/issues)

</div>

---

## 📋 Table of Contents

- [✨ Features](#-features)
- [🛠 Tech Stack](#-tech-stack)
- [🏗 Architecture](#-architecture)
- [📁 Project Structure](#-project-structure)
- [🚀 Getting Started](#-getting-started)
- [🔑 Environment Variables](#-environment-variables)
- [📡 API Endpoints](#-api-endpoints)
- [🌐 Deployment](#-deployment)
- [🗄 Database](#-database)
- [🗺 Roadmap](#-roadmap)
- [👨‍💻 Author](#-author)
- [📄 License](#-license)

---

## ✨ Features

### 🤖 AI Medical Assistant
- Powered by **Google Gemini 2.0 Flash** with **Anthropic Claude** fallback
- Supports **Bangla & English** conversations
- Symptom analysis, medicine info, health guidance
- Context-aware responses with safety disclaimers

### 🏥 Hospital & Doctor Directory
- **18+ hospitals** across all divisions of Bangladesh
- Real-time **bed availability** (General, ICU, CCU, Private)
- Doctor profiles with specialties, fees, and schedule
- **Online appointment booking** with instant confirmation
- Hospital ratings, reviews, and emergency contacts

### 🔐 Secure OTP Authentication
- **Gmail SMTP** real-time OTP email delivery
- **6-digit OTP** with **2-minute expiry**
- **60-second rate limiting** per email
- **5-attempt brute force** protection
- JWT access + refresh token with role-based redirect

### 🩸 Blood Donation Network
- Register as a blood donor
- Search donors by **blood group & location**
- Real-time donor availability status
- Donation history tracking

### 💊 Pharmacy & Medicine Finder
- Hospital pharmacy integration
- Medicine category search
- Home delivery availability info
- Generic medicine alternatives

### 🏥 Ward & Bed Management
- Real-time bed occupancy per ward type
- Visual bed status charts
- ICU / CCU / General / Private tracking
- Admission process guidance

### 📊 Analytics & Reporting
- Hospital KPI dashboard
- Patient volume analytics
- Doctor performance metrics
- Billing and revenue reports

---

## 🛠 Tech Stack

### Backend
| Technology | Version | Purpose |
|-----------|---------|---------|
| **Django** | 4.2 LTS | Web framework |
| **Django REST Framework** | 3.14+ | RESTful API |
| **SimpleJWT** | 5.3+ | JWT authentication |
| **Google Gemini AI** | 2.0 Flash | AI medical assistant |
| **Anthropic Claude** | Sonnet 4.6 | AI fallback |
| **Gmail SMTP** | TLS 587 | OTP email delivery |
| **Gunicorn** | — | Production WSGI server |
| **WhiteNoise** | — | Static file serving |
| **django-cors-headers** | 4.0+ | CORS management |

### Frontend
| Technology | Purpose |
|-----------|---------|
| **HTML5 / CSS3 / Vanilla JS ES6+** | Core frontend |
| **Firebase Hosting** | CDN + HTTPS + global delivery |
| **Firebase Firestore** | Real-time database sync |
| **Firebase Auth** | Google OAuth login |
| **Font Awesome 6.5** | Icon library |
| **Google Fonts** | Typography |

### Database & Storage
| Technology | Purpose |
|-----------|---------|
| **PostgreSQL** | Primary database (Render production) |
| **SQLite** | Local development database |
| **MongoDB Atlas** | Analytics, logs, audit trails |
| **Firebase Firestore** | Real-time frontend data |

### DevOps & Hosting
| Service | Purpose |
|---------|---------|
| **Render.com** | Django backend hosting |
| **Firebase Hosting** | Frontend static hosting |
| **MongoDB Atlas** | Cloud NoSQL (free tier) |

---

## 🏗 Architecture

```
┌──────────────────────────────────────────────────────────┐
│                     USER BROWSER                          │
│         https://medfind-bangladesh.web.app               │
└─────────────────────┬────────────────────────────────────┘
                      │
         ┌────────────▼────────────┐
         │   Firebase Hosting      │  ◄── HTML / CSS / JS (CDN)
         │   (Frontend)            │
         └────────────┬────────────┘
                      │ HTTPS API calls
         ┌────────────▼────────────┐      ┌──────────────────┐
         │   Render.com            │      │  Google Gemini   │
         │   Django REST API       │◄────►│  2.0 Flash (AI)  │
         │   (Backend)             │      └──────────────────┘
         └────┬──────────────┬─────┘      ┌──────────────────┐
              │              │       ◄───►│  Anthropic Claude│
   ┌──────────▼───┐  ┌───────▼──────┐    │  (AI Fallback)   │
   │  PostgreSQL  │  │  MongoDB     │    └──────────────────┘
   │  (Render)    │  │  Atlas       │
   └──────────────┘  └──────────────┘
              │
   ┌──────────▼──────────┐
   │  Firebase Firestore │  ◄── Real-time hospital & doctor data
   └─────────────────────┘
```

---

## 📁 Project Structure

```
MedFind-Bangladesh/
│
├── 📁 backend/
│   ├── 📁 ai/                         # Gemini AI chat module
│   │   ├── views.py                   # AI proxy endpoint
│   │   └── utils.py                   # Gemini + Claude integration
│   │
│   ├── 📁 otp_auth/                   # OTP authentication system
│   │   ├── models.py                  # EmailOTP model
│   │   ├── services.py                # OTP generate + Gmail send
│   │   ├── views.py                   # Send / Verify / Resend
│   │   └── urls.py
│   │
│   ├── 📁 donate/                     # Blood donation module
│   │
│   ├── 📁 apps/
│   │   ├── 📁 accounts/               # User auth (JWT login/register)
│   │   ├── 📁 hospitals/              # Hospital models & views
│   │   ├── 📁 doctors/                # Doctor profiles
│   │   ├── 📁 patients/               # Patient records
│   │   ├── 📁 appointments/           # Booking system
│   │   ├── 📁 billing/                # Invoices & payments
│   │   ├── 📁 pharmacy/               # Medicine management
│   │   ├── 📁 labs/                   # Lab test management
│   │   ├── 📁 telemedicine/           # Video consultation
│   │   ├── 📁 analytics_api/          # KPI & reporting
│   │   ├── 📁 notifications/          # Push notifications
│   │   ├── 📁 records/                # Medical records
│   │   └── 📁 common/                 # Health check & shared utils
│   │
│   ├── 📁 medfind_project/
│   │   ├── settings.py                # Local development settings
│   │   ├── settings_render.py         # Production (Render) settings
│   │   ├── urls.py                    # Root URL configuration
│   │   └── wsgi.py
│   │
│   ├── .env.example                   # Environment template ← copy to .env
│   ├── manage.py
│   ├── requirements_render.txt        # Production requirements
│   └── render.yaml                    # Render.com deployment config
│
├── 📁 frontend/
│   ├── index.html                     # Landing page
│   ├── telemedicine.html              # Video consultation page
│   ├── 404.html                       # Custom 404 error page
│   │
│   ├── 📁 pages/
│   │   ├── login.html                 # OTP-based login
│   │   ├── register.html              # New user registration
│   │   ├── medfind-ai.html            # AI assistant chat
│   │   ├── 📁 hospital/               # Hospital profile & listing
│   │   ├── 📁 doctors/                # Doctor search & profiles
│   │   ├── 📁 patients/               # Patient dashboard
│   │   ├── 📁 blood-donor/            # Blood donation
│   │   └── 📁 pharmacy/               # Medicine finder
│   │
│   └── 📁 assets/
│       ├── 📁 css/                    # Stylesheets (base, components, responsive)
│       ├── 📁 js/
│       │   ├── config.js              # API base URL auto-detection
│       │   ├── firebase-config.js     # Firebase configuration
│       │   ├── components.js          # Navbar / footer injection
│       │   ├── firestore.js           # Firestore data helpers
│       │   └── main.js                # App entry point
│       └── medfind-logo.png
│
├── firebase.json                      # Firebase hosting + security headers
├── .firebaserc                        # Firebase project binding
├── .gitignore
└── README.md
```

---

## 🚀 Getting Started

### Prerequisites

- **Python 3.11+**
- **Git**
- Gmail account with [App Password](https://myaccount.google.com/apppasswords) enabled
- [Gemini API Key](https://aistudio.google.com/app/apikey) — free

### Step 1 — Clone

```bash
git clone https://github.com/Baborkhan/MedFind-Bangladesh-AI-Healthcare-Platform.git
cd MedFind-Bangladesh-AI-Healthcare-Platform
```

### Step 2 — Backend Setup

```bash
cd backend

# Create virtual environment
python -m venv venv

# Activate — Windows
venv\Scripts\activate

# Activate — Mac/Linux
# source venv/bin/activate

# Install dependencies
pip install -r requirements_render.txt
```

### Step 3 — Configure Environment

```bash
# Windows
copy .env.example .env

# Mac/Linux
cp .env.example .env
```

Edit `.env` and add your real values (see [Environment Variables](#-environment-variables)).

### Step 4 — Database Setup

```bash
python manage.py migrate --settings=medfind_project.settings
python manage.py createsuperuser --settings=medfind_project.settings
```

### Step 5 — Start Server

```bash
python manage.py runserver --settings=medfind_project.settings
```

Backend running at: `http://127.0.0.1:8000`

### Step 6 — Open Frontend

Open `frontend/index.html` with **VS Code Live Server** on port 5500.  
`config.js` auto-detects `localhost` and points to `http://127.0.0.1:8000/api/v1`.

### Step 7 — Test OTP Email *(in a new terminal)*

```bash
curl -X POST http://127.0.0.1:8000/api/v1/accounts/send-otp/ \
  -H "Content-Type: application/json" \
  -d "{\"email\": \"your@gmail.com\"}"
```

**Expected response:**
```json
{"success": true, "message": "OTP sent to your@gmail.com. Valid for 2 minutes."}
```

---

## 🔑 Environment Variables

Create `backend/.env` from `backend/.env.example`:

```env
# ── Django ──────────────────────────────────────────────────
DEBUG=True
SECRET_KEY=your-super-secret-django-key-change-this
ALLOWED_HOSTS=localhost,127.0.0.1

# ── AI — Google Gemini (Primary) ────────────────────────────
# Free key at: https://aistudio.google.com/apikey
GEMINI_API_KEY=AIzaSy...your-key-here
GEMINI_MODEL=gemini-2.0-flash-lite

# ── AI — Anthropic Claude (Fallback, optional) ───────────────
# ANTHROPIC_API_KEY=sk-ant-api03-...

# ── Email OTP via Gmail ──────────────────────────────────────
# Gmail → Account → Security → 2-Step → App passwords → Create
EMAIL_HOST_USER=your@gmail.com
EMAIL_HOST_PASSWORD=xxxx-xxxx-xxxx-xxxx

# ── Database (leave blank to use local SQLite) ───────────────
# DATABASE_URL=postgresql://user:pass@host:5432/medfind

# ── MongoDB (optional — analytics, audit logs) ───────────────
MONGODB_URI=mongodb://127.0.0.1:27017
MONGODB_NAME=medfind
```

> ⚠️ **Never commit `.env` to Git.** It is listed in `.gitignore`.

---

## 📡 API Endpoints

| Base URL | Environment |
|----------|-------------|
| `https://medfind-bangladesh-ai-healthcare-platform.onrender.com` | Production |
| `http://127.0.0.1:8000` | Local |

### 🟢 Health

| Method | Endpoint | Auth | Description |
|--------|----------|------|-------------|
| `GET` | `/` | Public | Root health check |
| `GET` | `/api/v1/health/` | Public | API service status |

### 🔐 Authentication

| Method | Endpoint | Auth | Description |
|--------|----------|------|-------------|
| `POST` | `/api/v1/accounts/register/` | Public | Register new user |
| `POST` | `/api/v1/accounts/login/` | Public | Login → JWT tokens |
| `POST` | `/api/v1/accounts/send-otp/` | Public | Send OTP to email |
| `POST` | `/api/v1/accounts/verify-otp/` | Public | Verify OTP |
| `POST` | `/api/v1/accounts/resend-otp/` | Public | Resend new OTP |
| `GET` | `/api/v1/accounts/profile/` | JWT | Get user profile |

**Login Response:**
```json
{
  "success": true,
  "access": "eyJhbGciOiJIUzI1NiIs...",
  "refresh": "eyJhbGciOiJIUzI1NiIs...",
  "user": { "email": "user@example.com", "role": "patient" },
  "redirect": "/pages/patients/dashboard.html"
}
```

### 🤖 AI Assistant

| Method | Endpoint | Auth | Description |
|--------|----------|------|-------------|
| `POST` | `/api/v1/ai/chat/` | Public | Chat with Gemini AI |
| `GET` | `/api/v1/ai/chat/` | Public | AI service health |

**Request:**
```json
{
  "messages": [
    {"role": "user", "content": "আমার মাথাব্যথা হচ্ছে, কী করব?"}
  ]
}
```

### 🩸 Blood Donation

| Method | Endpoint | Auth | Description |
|--------|----------|------|-------------|
| `POST` | `/api/donate/register/` | Public | Register as donor |
| `GET` | `/api/donate/donors/` | Public | List all donors |
| `GET` | `/api/donate/blood-search/` | Public | Search by blood group |
| `GET` | `/api/donate/stats/` | Public | Donation statistics |

**Blood Search:**
```
GET /api/donate/blood-search/?blood_group=A%2B&district=Dhaka
```

---

## 🌐 Deployment

### Frontend — Firebase Hosting

```bash
# Install Firebase CLI
npm install -g firebase-tools

# Login to Firebase
firebase login

# Deploy frontend
firebase deploy --only hosting
```

**Live URL:** [https://medfind-bangladesh.web.app](https://medfind-bangladesh.web.app/)

---

### Backend — Render.com

Auto-deploys via `render.yaml` on every push to `main`.

**Manual Render Setup:**
1. [render.com](https://render.com) → New → Web Service
2. Connect GitHub repository
3. Root Directory: `backend`
4. Build Command: `pip install -r requirements_render.txt`
5. Start Command: `gunicorn medfind_project.wsgi:application`
6. Add environment variables below

**Render Environment Variables:**

| Key | Value |
|-----|-------|
| `SECRET_KEY` | Your Django secret key |
| `DEBUG` | `False` |
| `ALLOWED_HOSTS` | `localhost,127.0.0.1,.onrender.com` |
| `GEMINI_API_KEY` | Your Gemini API key |
| `EMAIL_HOST_USER` | Your Gmail |
| `EMAIL_HOST_PASSWORD` | Your Gmail App Password |
| `DATABASE_URL` | *(Auto-set by Render PostgreSQL add-on)* |
| `MONGODB_URI` | MongoDB Atlas connection string |
| `CORS_ALLOWED_ORIGINS` | `https://medfind-bangladesh.web.app` |

**Backend URL:** `https://medfind-bangladesh-ai-healthcare-platform.onrender.com`

---

## 🗄 Database

| Database | Environment | Purpose |
|----------|-------------|---------|
| **PostgreSQL** | Production (Render) | Primary relational data |
| **SQLite** | Local development | Zero-config local DB |
| **MongoDB Atlas** | Production (optional) | AI logs, analytics, audits |
| **Firebase Firestore** | Frontend | Real-time hospital & doctor data |

The app auto-selects SQLite locally and PostgreSQL on Render via `DATABASE_URL`.

---

## 🗺 Roadmap

- [x] Gemini AI medical assistant (Bangla + English)
- [x] OTP authentication via Gmail SMTP
- [x] Hospital & doctor directory (18+ hospitals)
- [x] Blood donation network
- [x] Ward & bed management
- [x] JWT auth with role-based dashboards
- [x] Firebase Firestore real-time sync
- [x] Firebase Hosting (live)
- [x] Render.com backend (live)
- [x] PostgreSQL + MongoDB integration
- [ ] SSLCommerz payment gateway (Bangladesh)
- [ ] WebRTC video telemedicine
- [ ] Mobile app (React Native)
- [ ] SMS OTP via Twilio/Infobip
- [ ] Bangla voice input for AI

---

## 🤝 Contributing

Contributions, issues and feature requests are welcome!

1. **Fork** the repository
2. Create your feature branch: `git checkout -b feature/amazing-feature`
3. Commit changes: `git commit -m 'feat: add amazing feature'`
4. Push: `git push origin feature/amazing-feature`
5. Open a **Pull Request**

---

## 👨‍💻 Author

<div align="center">

**Babor Khan**

[![GitHub](https://img.shields.io/badge/GitHub-@Baborkhan-181717?style=flat-square&logo=github)](https://github.com/Baborkhan)
[![Email](https://img.shields.io/badge/Email-baborkhan117085@gmail.com-D14836?style=flat-square&logo=gmail&logoColor=white)](mailto:baborkhan117085@gmail.com)

</div>

---

## 📄 License

This project is licensed under the **MIT License** — see the [LICENSE](LICENSE) file for details.

---

<div align="center">

**🇧🇩 Made with ❤️ for Bangladesh**

*Improving healthcare accessibility for millions of Bangladeshis*

⭐ **Star this repo** if MedFind helped you!

[![Live Demo](https://img.shields.io/badge/🌐_Visit_Live_Site-medfind--bangladesh.web.app-2563eb?style=for-the-badge)](https://medfind-bangladesh.web.app/)

</div>
