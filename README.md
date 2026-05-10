<<<<<<< HEAD
<<<<<<< HEAD
=======
>>>>>>> 58c405af0447997e6cf8a412fa3573bac7007072
<div align="center">

# 🏥 MedFind Bangladesh

**AI-Powered Healthcare Platform for Bangladesh**

[![Django](https://img.shields.io/badge/Django-4.2-092E20?style=flat-square&logo=django&logoColor=white)](https://djangoproject.com)
[![Python](https://img.shields.io/badge/Python-3.11+-3776AB?style=flat-square&logo=python&logoColor=white)](https://python.org)
[![Gemini AI](https://img.shields.io/badge/Gemini-2.0_Flash-4285F4?style=flat-square&logo=google&logoColor=white)](https://ai.google.dev)
[![License](https://img.shields.io/badge/License-MIT-green?style=flat-square)](LICENSE)
[![Status](https://img.shields.io/badge/Status-Active_Development-orange?style=flat-square)]()

*Connecting patients with doctors, medicines, and health resources across Bangladesh*

</div>

---

## 📋 Table of Contents
- [About](#about) · [Features](#features) · [Tech Stack](#tech-stack) · [Project Structure](#project-structure)
- [Getting Started](#getting-started) · [Environment Variables](#environment-variables) · [API Endpoints](#api-endpoints)

---

## 🏥 About

**MedFind Bangladesh** is a comprehensive digital health platform designed specifically for the people of Bangladesh. It combines AI-powered medical assistance, real-time telemedicine, blood donation management, and medicine availability tracking — all in one place.

> Built to solve real healthcare accessibility problems in Bangladesh where millions lack easy access to qualified medical guidance.

---

## ✨ Features

| Feature | Status |
|---------|--------|
| 🤖 **Gemini AI Medical Assistant** — 24/7 health Q&A in Bangla & English | ✅ Live |
| 🩸 **Blood Donation Network** — Find donors by blood group & location | ✅ Live |
| 💊 **Medicine Finder** — Search & locate medicines across pharmacies | ✅ Live |
| 🔐 **OTP Authentication** — Secure Gmail-based 2-minute OTP login | ✅ Live |
| 🏥 **Hospital Directory** — Find nearby hospitals & clinics | ✅ Live |
| 📹 **Telemedicine** — Video consultations with licensed doctors | 🔄 In Progress |
| 💳 **SSLCommerz Payments** — Bangladesh payment gateway integration | 🔄 In Progress |

---

## 🛠 Tech Stack

**Backend:** Django 4.2 · DRF · Google Gemini AI · Gmail SMTP · SQLite/PostgreSQL  
**Frontend:** HTML5 · CSS3 · Vanilla JavaScript ES6+  
**Real-time:** Django Channels · WebSocket  
**Auth:** JWT · Gmail OTP (6-digit, 2-min expiry)  
**DevOps:** Docker · Nginx · Gunicorn

---

## 📁 Project Structure

```
medfind-bangladesh/
├── backend/
│   ├── ai/                    # Gemini AI chat module
│   ├── donate/                # Blood donation module
│   ├── otp_app/               # OTP authentication (send/verify/resend)
│   ├── medfind_project/       # Django settings & URLs
│   ├── .env.example           # Environment template ← copy to .env
│   ├── manage.py
│   └── requirements.txt
│
├── frontend/
│   ├── index.html             # Landing page
│   ├── pages/                 # Inner pages
│   └── assets/                # CSS · JS · Images
│
├── deployment/                # Nginx + Gunicorn production configs
├── Dockerfile
├── START_LOCAL.bat            # Windows one-click start
└── README.md
```

---

## 🚀 Getting Started

### Prerequisites
- Python 3.11+ · Git
- Gmail account with [App Password](https://myaccount.google.com/apppasswords)
- [Gemini API Key](https://aistudio.google.com/app/apikey) (free)

### 1 — Clone

```bash
git clone https://github.com/Baborkhan/medfind-bangladesh.git
cd medfind-bangladesh
```

### 2 — Setup Backend

```bash
cd backend
python -m venv venv
venv\Scripts\activate          # Windows
# source venv/bin/activate     # Mac/Linux
pip install -r requirements-local.txt
```

### 3 — Configure Environment

```bash
copy .env.example .env         # Windows
# cp .env.example .env         # Mac/Linux
# Then edit .env and add your API keys
```

### 4 — Run

```bash
python manage.py migrate
python manage.py runserver
```

### 5 — Open Frontend

Open `frontend/index.html` with VS Code Live Server (port 5500)  
or visit `http://127.0.0.1:8000`

---

## 🔑 Environment Variables

```env
# Django
DEBUG=True
SECRET_KEY=your-secret-key-here

# Gemini AI (free key at aistudio.google.com)
GEMINI_API_KEY=AIzaSy...your-key-here
GEMINI_MODEL=gemini-2.0-flash-lite

# Gmail SMTP (for OTP emails)
GMAIL_USER=your-email@gmail.com
GMAIL_APP_PASSWORD=xxxx-xxxx-xxxx-xxxx

# Optional — SSLCommerz
SSLCOMMERZ_STORE_ID=
SSLCOMMERZ_STORE_PASS=
SSLCOMMERZ_IS_SANDBOX=True
```

> 📌 **Gmail App Password:** Google Account → Security → 2-Step Verification → App Passwords

---

## 📡 API Endpoints

### AI Chat
| Method | Endpoint | Description |
|--------|----------|-------------|
| `POST` | `/api/v1/ai/chat/` | Send message to Gemini AI |
| `GET` | `/api/v1/ai/health/` | Service health check |

### OTP Auth
| Method | Endpoint | Description |
|--------|----------|-------------|
| `POST` | `/api/otp/send/` | Generate + email OTP |
| `POST` | `/api/otp/verify/` | Verify 6-digit OTP |
| `POST` | `/api/otp/resend/` | Cancel old → send new OTP |
| `GET` | `/api/otp/status/?email=` | Countdown timer status |

### Blood Donation
| Method | Endpoint | Description |
|--------|----------|-------------|
| `POST` | `/api/donate/register/` | Register as donor |
| `GET` | `/api/donate/donors/?blood_group=A+` | Find donors |

---

## 👨‍💻 Author

**Babor Khan** · baborkhan117085@gmail.com · [@Baborkhan](https://github.com/Baborkhan)

## 📄 License

MIT License — see [LICENSE](LICENSE)

---

<div align="center">
Made with ❤️ for Bangladesh 🇧🇩 — ⭐ Star this repo if it helped you!
<<<<<<< HEAD
</div>
=======
# MedFind-Bangladesh-AI-Healthcare-Platform
MedFind Bangladesh is an AI-powered healthcare platform built with Django that connects patients with doctors, medicines, and healthcare services across Bangladesh. It includes Gemini AI assistant, blood donation system, medicine finder, OTP authentication, and hospital directory in one smart solution.
>>>>>>> b3dcd5313e4dc8b4aba25c9142e0b63f76f92b39
=======
</div>
>>>>>>> 58c405af0447997e6cf8a412fa3573bac7007072
