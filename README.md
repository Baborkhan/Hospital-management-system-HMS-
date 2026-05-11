<div align="center">

<img src="./assets/images/medfind-logo.png" alt="MEDFIND Logo" width="220"/>

# 🏥 MEDFIND

### Your Comprehensive Healthcare Discovery Platform

A modern, scalable, and feature-rich healthcare management system that connects patients with hospitals, doctors, laboratories, and medical services across Bangladesh.

<br>

### 🌐 Live Demo
👉 https://medfind-bangladesh.web.app/

<br>

<img src="https://img.shields.io/badge/HTML5-E34F26?style=for-the-badge&logo=html5&logoColor=white" alt="HTML5"/>
<img src="https://img.shields.io/badge/CSS3-1572B6?style=for-the-badge&logo=css3&logoColor=white" alt="CSS3"/>
<img src="https://img.shields.io/badge/Django-092E20?style=for-the-badge&logo=django&logoColor=white" alt="Django"/>
<img src="https://img.shields.io/badge/MongoDB-47A248?style=for-the-badge&logo=mongodb&logoColor=white" alt="MongoDB"/>
<img src="https://img.shields.io/badge/PostgreSQL-316192?style=for-the-badge&logo=postgresql&logoColor=white" alt="PostgreSQL"/>
<img src="https://img.shields.io/badge/Redis-DC382D?style=for-the-badge&logo=redis&logoColor=white" alt="Redis"/>

</div>

---

# 📖 Project Overview

**MEDFIND** is a comprehensive healthcare discovery and hospital management platform designed to simplify healthcare accessibility and digital medical service management.

The platform helps users:

- 🔎 Search hospitals, clinics, and doctors
- 📍 Discover nearby healthcare facilities
- 📅 Book doctor appointments online
- 🎥 Attend video consultations
- 🧾 Manage prescriptions and medical history
- 🛏️ Check bed availability
- 🧪 Upload and manage laboratory reports
- 💳 Handle OPD/IPD billing and payments

---

# ✨ Key Features

- ✅ Smart Location-Based Search
- ✅ Doctor & Hospital Discovery
- ✅ Appointment Booking System
- ✅ Video Consultation Support
- ✅ Advanced Search & Filtering
- ✅ Hospital & Doctor Profiles
- ✅ Prescription Management
- ✅ Bed Availability Monitoring
- ✅ Real-Time Notifications
- ✅ Responsive UI/UX
- ✅ Role-Based Authentication

---

# 🏥 Major Modules

## 👤 Patient Portal
- Appointment booking
- Prescription management
- Medical history access
- Doctor consultation tracking

## 👨‍⚕️ Doctor Portal
- Patient queue management
- Consultation schedules
- Prescription creation
- Medical notes management
- Video consultation system

## 🏢 Admin Panel
- User management
- Hospital verification
- Analytics & reporting
- System monitoring

## 💊 Pharmacy Management
- Medicine inventory
- Stock management
- Expiry alerts
- Sales tracking

## 🧪 Laboratory System
- Test order management
- Diagnostic tracking
- Report uploads

## 💳 Billing System
- OPD/IPD billing
- Invoice generation
- Payment processing

## 🛏️ Ward & Bed Management
- ICU/General/Cabin availability
- Bed allocation system

---

# 🛠️ Technology Stack

| Category | Technologies |
|----------|-------------|
| Frontend | HTML5, CSS3, JavaScript |
| Backend | Django 4.x, Django REST Framework |
| Database | PostgreSQL, MongoDB |
| Authentication | JWT Authentication |
| Real-Time | Django Channels, WebSockets |
| Async Tasks | Celery |
| Caching | Redis |

---

# 📁 Project Structure

```bash
medfind/
│
├── frontend/
│   ├── assets/
│   │   ├── images/
│   │   │   └── medfind-logo.png
│   │   ├── css/
│   │   └── js/
│   │
│   ├── pages/
│   │   ├── patient/
│   │   ├── doctor/
│   │   ├── admin/
│   │   ├── pharmacy/
│   │   ├── lab/
│   │   └── billing/
│   │
│   └── index.html
│
├── backend/
│   ├── apps/
│   ├── config/
│   ├── scripts/
│   ├── requirements.txt
│   ├── manage.py
│   └── .env.example
│
└── README.md
```

---

# 🚀 Getting Started

## Clone Repository

```bash
git clone https://github.com/yourusername/medfind.git
```

## Move to Frontend Directory

```bash
cd medfind/frontend
```

## Start Development Server

```bash
python -m http.server 8000
```

## Open Browser

```text
http://localhost:8000
```

---

# ⚙️ Backend Setup

## Create Virtual Environment

```bash
cd backend
python -m venv venv
```

## Activate Environment

### Linux / macOS

```bash
source venv/bin/activate
```

### Windows

```bash
venv\Scripts\activate
```

## Install Dependencies

```bash
pip install -r requirements.txt
```

## Configure Environment Variables

```bash
cp .env.example .env
```

## Run Database Migrations

```bash
python manage.py migrate --settings=config.settings.dev
```

## Start Development Server

```bash
python manage.py runserver --settings=config.settings.dev
```

---

# 🔒 Security & Production Readiness

- JWT Authentication
- Role-Based Access Control (RBAC)
- HTTPS/SSL Support
- API Rate Limiting
- Automated Backup System
- Dockerized Deployment
- CI/CD with GitHub Actions

---

# 🚀 Production Deployment

## Set Production Environment

```bash
export DJANGO_SETTINGS_MODULE=config.settings.prod
```

## Collect Static Files

```bash
python manage.py collectstatic --noinput
```

## Run Migrations

```bash
python manage.py migrate
```

## Start Gunicorn

```bash
gunicorn config.wsgi:application --workers 4 --bind 0.0.0.0:8000
```

## Start Daphne

```bash
daphne -b 0.0.0.0 -p 8001 config.asgi:application
```

---

# 🌐 Project Links

## 🔗 Live Website
👉 https://medfind-bangladesh.web.app/

## 🔗 GitHub Repository
👉 Replace with your actual GitHub repository link

---

<div align="center">

# ❤️ MEDFIND — Connecting Healthcare with Technology

### Built with dedication for smarter healthcare management.

</div>
