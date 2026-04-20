# Django Backend for Hospital Management System

This backend implements a Django REST-style API with MongoDB as the primary data store.

## Setup

1. Install Python dependencies:

   pip install -r requirements.txt

2. Copy `.env.example` to `.env` and update MongoDB connection settings.

3. Run migrations:

   python manage.py makemigrations
   python manage.py migrate

4. Start the development server:

   python manage.py runserver

## MongoDB

The Django project uses `djongo` to connect to MongoDB. Set `MONGODB_URI` and `MONGODB_NAME` in `.env`.

## API endpoints

- `/api/auth/register/`
- `/api/auth/login/`
- `/api/auth/logout/`
- `/api/patients/`
- `/api/patients/<id>/`
- `/api/doctors/`
- `/api/doctors/<id>/`
- `/api/appointments/`
- `/api/appointments/<id>/`
- `/api/bills/`
- `/api/bills/<id>/`
- `/api/admissions/`
- `/api/admissions/<id>/`
