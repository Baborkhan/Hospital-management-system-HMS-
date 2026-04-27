# MEDFIND Backend - Django + MongoDB

Django ব্যাকএন্ড এবং MongoDB ডাটাবেস সহ Hospital Management System

## 📋 প্রজেক্ট স্ট্রাকচার

```
backend/
├── medfind_backend/         # Main Django Project
│   ├── __init__.py
│   ├── settings.py          # Django Settings with MongoDB config
│   ├── urls.py              # Main URL routing
│   ├── wsgi.py              # WSGI application
│   └── api/                 # API Application
│       ├── models.py        # MongoDB Models (MongoEngine)
│       ├── views.py         # ViewSets for API endpoints
│       ├── serializers.py   # Serializers for data validation
│       ├── urls.py          # API URLs
│       ├── admin.py         # Admin configuration
│       └── utils.py         # Utility functions
├── manage.py                # Django management script
├── requirements.txt         # Python dependencies
├── .env                     # Environment variables
└── README.md               # This file
```

## 🚀 সেটআপ এবং ইনস্টলেশন

### 1. প্রয়োজনীয় সফটওয়্যার

- Python 3.8+ 
- MongoDB (locally hosted)
- pip (Python package manager)

### 2. MongoDB সেটআপ (Windows)

```bash
# MongoDB Community Edition ডাউনলোড করুন
# https://www.mongodb.com/try/download/community

# ইনস্টলেশনের পর, MongoDB সার্ভিস শুরু করুন
# নাহলে command line থেকে:
mongod

# অন্য terminal এ MongoDB shell চালান:
mongosh
```

### 3. Django ব্যাকএন্ড সেটআপ

```bash
# Backend directory তে যান
cd backend

# Virtual Environment তৈরি করুন
python -m venv venv

# Virtual Environment activate করুন
# Windows এ:
venv\Scripts\activate

# Linux/Mac এ:
source venv/bin/activate

# Dependencies ইনস্টল করুন
pip install -r requirements.txt
```

### 4. এনভায়রনমেন্ট ভেরিয়েবল সেটআপ

`.env` ফাইল সম্পাদনা করুন:

```env
DEBUG=True
SECRET_KEY=your-secret-key-here
ALLOWED_HOSTS=127.0.0.1,localhost

MONGO_URI=mongodb://localhost:27017
MONGO_DBNAME=medfind_db
```

### 5. Django Server চালান

```bash
python manage.py runserver
```

সার্ভার শুরু হবে: `http://127.0.0.1:8000`

## 🔌 API Endpoints

### Hospital API
```
GET    /api/hospitals/                 # সব হাসপাতাল লিস্ট
POST   /api/hospitals/                 # নতুন হাসপাতাল তৈরি
GET    /api/hospitals/{id}/            # হাসপাতাল বিবরণ
PUT    /api/hospitals/{id}/            # হাসপাতাল আপডেট
GET    /api/hospitals/{id}/doctors/    # হাসপাতালের ডাক্তার
GET    /api/hospitals/{id}/services/   # হাসপাতালের সেবা
```

### Doctor API
```
GET    /api/doctors/                   # সব ডাক্তার লিস্ট
POST   /api/doctors/                   # নতুন ডাক্তার তৈরি
GET    /api/doctors/{id}/              # ডাক্তার বিবরণ
GET    /api/doctors/{id}/availability/ # ডাক্তারের উপলব্ধতা
```

### Patient API
```
GET    /api/patients/                  # সব রোগী লিস্ট
POST   /api/patients/                  # নতুন রোগী তৈরি
GET    /api/patients/{id}/             # রোগী বিবরণ
GET    /api/patients/{id}/medical_history/  # চিকিৎসা ইতিহাস
GET    /api/patients/{id}/appointments/     # অ্যাপয়েন্টমেন্ট
```

### Appointment API
```
GET    /api/appointments/              # সব অ্যাপয়েন্টমেন্ট
POST   /api/appointments/              # অ্যাপয়েন্টমেন্ট বুকিং
GET    /api/appointments/{id}/         # অ্যাপয়েন্টমেন্ট বিবরণ
GET    /api/appointments/by_patient/?patient_id={id}
GET    /api/appointments/by_doctor/?doctor_id={id}
```

### Lab Test API
```
GET    /api/lab-tests/                 # সব ল্যাব টেস্ট
POST   /api/lab-tests/                 # নতুন টেস্ট তৈরি
GET    /api/lab-tests/{id}/            # টেস্ট বিবরণ
GET    /api/lab-tests/by_patient/?patient_id={id}
```

### Billing API
```
GET    /api/billing/                   # সব বিল
POST   /api/billing/                   # নতুন বিল তৈরি
GET    /api/billing/{id}/              # বিল বিবরণ
GET    /api/billing/by_patient/?patient_id={id}
POST   /api/billing/{id}/mark_as_paid/ # বিল পেমেন্ট মার্ক করুন
```

## 📚 ডেটা মডেল (MongoDB Collections)

### Hospital Collection
```javascript
{
    _id: ObjectId,
    name: String,
    email: String,
    phone: String,
    address: {
        street: String,
        city: String,
        state: String,
        postal_code: String,
        latitude: Float,
        longitude: Float
    },
    specialties: [String],
    bed_count: Integer,
    ambulance_available: Boolean,
    emergency_services: Boolean,
    rating: Float,
    created_at: DateTime
}
```

### Doctor Collection
```javascript
{
    _id: ObjectId,
    first_name: String,
    last_name: String,
    email: String,
    specialization: String,
    hospital: ObjectId (Reference to Hospital),
    consultation_fee: Float,
    rating: Float,
    created_at: DateTime
}
```

### Patient Collection
```javascript
{
    _id: ObjectId,
    first_name: String,
    last_name: String,
    email: String,
    phone: String,
    date_of_birth: DateTime,
    blood_group: String,
    medical_conditions: [String],
    allergies: [String],
    created_at: DateTime
}
```

### Appointment Collection
```javascript
{
    _id: ObjectId,
    patient: ObjectId (Reference to Patient),
    doctor: ObjectId (Reference to Doctor),
    hospital: ObjectId (Reference to Hospital),
    appointment_date: DateTime,
    appointment_type: String,
    status: String,
    created_at: DateTime
}
```

## 🛠️ ডেভেলপমেন্ট

### নতুন API Endpoint যোগ করুন

1. **Model তৈরি করুন** (`api/models.py`)
2. **Serializer তৈরি করুন** (`api/serializers.py`)
3. **ViewSet তৈরি করুন** (`api/views.py`)
4. **URL Router এ যোগ করুন** (`medfind_backend/urls.py`)

### টেস্টিং

```bash
# সব টেস্ট চালান
python manage.py test

# নির্দিষ্ট টেস্ট চালান
python manage.py test api.tests.HospitalAPITestCase
```

## 🔒 নিরাপত্তা

- `.env` ফাইলে সংবেদনশীল তথ্য রাখুন
- প্রোডাকশনে `DEBUG=False` সেট করুন
- একটি শক্তিশালী `SECRET_KEY` ব্যবহার করুন
- CORS সেটিংস কনফিগার করুন

## 📱 Frontend Integration

Frontend থেকে API ব্যবহার করুন:

```javascript
// হাসপাতাল লিস্ট ফেচ করুন
fetch('http://localhost:8000/api/hospitals/')
    .then(response => response.json())
    .then(data => console.log(data));

// নতুন অ্যাপয়েন্টমেন্ট বুকিং করুন
fetch('http://localhost:8000/api/appointments/', {
    method: 'POST',
    headers: {
        'Content-Type': 'application/json',
    },
    body: JSON.stringify({
        patient: 'patient_id',
        doctor: 'doctor_id',
        hospital: 'hospital_id',
        appointment_date: '2024-01-15T10:00:00',
        appointment_type: 'In-Person',
        status: 'Scheduled'
    })
})
.then(response => response.json())
.then(data => console.log(data));
```

## 🐛 ট্রাবলশুটিং

### MongoDB Connection Error
```
সমাধান: MongoDB সার্ভিস চালু আছে কিনা চেক করুন
mongod
```

### Port already in use
```
python manage.py runserver 8001
```

### ModuleNotFoundError
```
pip install -r requirements.txt
```

## 📞 সহায়তা

কোনো সমস্যা হলে, backend ডিরেক্টরি থেকে এই কমান্ড চালান:

```bash
python manage.py check
```

## 📄 লাইসেন্স

এই প্রজেক্ট MIT লাইসেন্স এর অধীন।

---

**Happy Coding! 🎉**
