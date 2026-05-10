#!/usr/bin/env python
"""
MedFind - Seed Data Script
⚠️  DEV/STAGING USE ONLY — Never run on production with default passwords!
    Before running on production: change all passwords below or use env vars.
Run: python seed_data.py
"""
import os
import sys
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings.dev")
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
django.setup()

from apps.accounts.models import User
from apps.hospitals.models import Hospital
from apps.doctors.models import Doctor, DoctorSchedule
from apps.patients.models import Patient
from apps.appointments.models import Appointment
from apps.pharmacy.models import Medicine
from apps.analytics_api.models import DailySnapshot
import datetime
import random

print("🌱 Seeding MedFind database...")

# ── Super Admin ──
admin_user, _ = User.objects.get_or_create(
    email="admin@medfind.com",
    defaults={"full_name": "Super Admin", "role": "superadmin",
              "is_staff": True, "is_superuser": True, "is_verified": True}
)
admin_user.set_password(os.getenv("SEED_ADMIN_PASS", "CHANGE-THIS-PASSWORD"))
admin_user.save()
print("✓ Super admin: admin@medfind.com / (password set via SEED_ADMIN_PASS env var)")

# ── Hospitals ──
hospitals_data = [
    {"name": "United Hospital Dhaka", "hospital_type": "private", "division": "Dhaka",
     "district": "Dhaka", "address": "Plot 15, Road 71, Gulshan, Dhaka-1212",
     "latitude": "23.7805", "longitude": "90.4149", "phone": "02-8836000",
     "total_beds": 350, "available_beds": 24, "icu_total": 18, "icu_available": 4,
     "emergency_open": True, "has_icu": True, "has_pharmacy": True, "has_lab": True,
     "specialties": ["Cardiology","Neurology","Orthopedic","Oncology"],
     "rating": 4.8, "is_verified": True, "is_premium": True},

    {"name": "Square Hospital Dhaka", "hospital_type": "private", "division": "Dhaka",
     "district": "Dhaka", "address": "18/F, Panthapath, Dhaka-1205",
     "latitude": "23.7513", "longitude": "90.3751", "phone": "10616",
     "total_beds": 400, "available_beds": 35, "icu_total": 22, "icu_available": 6,
     "emergency_open": True, "has_icu": True, "has_pharmacy": True, "has_lab": True,
     "specialties": ["Cardiology","Gynecology","Pediatric","Gastro"],
     "rating": 4.7, "is_verified": True, "is_premium": True},

    {"name": "Apollo Hospitals Dhaka", "hospital_type": "private", "division": "Dhaka",
     "district": "Dhaka", "address": "Plot 81, Block E, Bashundhara, Dhaka",
     "latitude": "23.8021", "longitude": "90.4308", "phone": "10678",
     "total_beds": 450, "available_beds": 40, "icu_total": 24, "icu_available": 8,
     "emergency_open": True, "has_icu": True, "has_pharmacy": True, "has_lab": True,
     "specialties": ["Oncology","Cardiology","Orthopedic","Transplant"],
     "rating": 4.9, "is_verified": True, "is_premium": True},

    {"name": "Rajshahi Medical College Hospital", "hospital_type": "government",
     "division": "Rajshahi", "district": "Rajshahi",
     "address": "Rajshahi Sadar, Rajshahi-6000",
     "latitude": "24.3745", "longitude": "88.6042", "phone": "0721-774044",
     "total_beds": 850, "available_beds": 112, "icu_total": 45, "icu_available": 8,
     "emergency_open": True, "has_icu": True, "has_pharmacy": True, "has_lab": True,
     "specialties": ["All Departments"],
     "rating": 4.1, "is_verified": True, "is_premium": False},

    {"name": "CMCH Chittagong Medical College Hospital", "hospital_type": "government",
     "division": "Chittagong", "district": "Chittagong",
     "address": "K B Fazlul Kader Road, Panchlaish, Chattogram",
     "latitude": "22.3569", "longitude": "91.7832", "phone": "031-630322",
     "total_beds": 1300, "available_beds": 95, "icu_total": 60, "icu_available": 5,
     "emergency_open": True, "has_icu": True, "has_pharmacy": True, "has_lab": True,
     "specialties": ["All Departments"],
     "rating": 4.3, "is_verified": True, "is_premium": False},

    {"name": "MAG Osmani Medical College Hospital", "hospital_type": "government",
     "division": "Sylhet", "district": "Sylhet",
     "address": "Sylhet Sadar, Sylhet-3100",
     "latitude": "24.8892", "longitude": "91.8817", "phone": "0821-2830170",
     "total_beds": 900, "available_beds": 72, "icu_total": 40, "icu_available": 7,
     "emergency_open": True, "has_icu": True, "has_pharmacy": True, "has_lab": True,
     "specialties": ["All Departments"],
     "rating": 4.2, "is_verified": True, "is_premium": False},

    {"name": "Popular Medical Centre Rajshahi", "hospital_type": "private",
     "division": "Rajshahi", "district": "Rajshahi",
     "address": "Shaheb Bazar, Rajshahi",
     "latitude": "24.3533", "longitude": "88.6254", "phone": "0721-777888",
     "total_beds": 180, "available_beds": 24, "icu_total": 12, "icu_available": 3,
     "emergency_open": False, "has_icu": True, "has_pharmacy": True, "has_lab": True,
     "specialties": ["Cardiology","Gynecology","Diagnostic"],
     "rating": 4.5, "is_verified": True, "is_premium": False},
]

hospitals = []
for hd in hospitals_data:
    hosp, _ = Hospital.objects.get_or_create(name=hd["name"], defaults=hd)
    hospitals.append(hosp)
print(f"✓ {len(hospitals)} hospitals seeded")

# ── Doctors ──
doctors_data = [
    {"name": "Ahmed Hossain", "email": "ahmed@medfind.com",
     "specialty": "Cardiologist", "qualification": "MBBS, MD (Cardiology), FRCP",
     "experience": 18, "fee": 800, "video_fee": 600, "hospital_idx": 0,
     "bio": "Senior Cardiologist with 18+ years of experience in interventional cardiology."},
    {"name": "Fatima Begum", "email": "fatima@medfind.com",
     "specialty": "Gynecologist", "qualification": "MBBS, FCPS (Gynae & Obs)",
     "experience": 14, "fee": 700, "video_fee": 500, "hospital_idx": 1,
     "bio": "Expert in maternal health, high-risk pregnancy, and laparoscopic surgery."},
    {"name": "Kamal Uddin", "email": "kamal@medfind.com",
     "specialty": "Neurologist", "qualification": "MBBS, MD (Neurology), PhD",
     "experience": 20, "fee": 1000, "video_fee": 800, "hospital_idx": 2,
     "bio": "Leading neurologist specializing in stroke, epilepsy, and movement disorders."},
    {"name": "Shahidul Islam", "email": "shahidul@medfind.com",
     "specialty": "Orthopedic Surgeon", "qualification": "MBBS, MS (Orthopedics), FRCS",
     "experience": 15, "fee": 900, "video_fee": 700, "hospital_idx": 0,
     "bio": "Specialist in joint replacement, spine surgery, and sports injuries."},
    {"name": "Nasreen Akter", "email": "nasreen@medfind.com",
     "specialty": "Pediatrician", "qualification": "MBBS, DCH, FCPS (Pediatrics)",
     "experience": 12, "fee": 600, "video_fee": 450, "hospital_idx": 1,
     "bio": "Caring pediatrician with expertise in newborn care and child development."},
    {"name": "Rafiqul Rahman", "email": "rafiqul@medfind.com",
     "specialty": "General Physician", "qualification": "MBBS, FCPS (Medicine)",
     "experience": 10, "fee": 500, "video_fee": 350, "hospital_idx": 3,
     "bio": "Experienced general physician at RMCH with expertise in internal medicine."},
]

doctors = []
for dd in doctors_data:
    user, _ = User.objects.get_or_create(
        email=dd["email"],
        defaults={"full_name": f"Dr. {dd['name']}", "role": "doctor", "is_verified": True}
    )
    user.set_password(os.getenv("SEED_DOCTOR_PASS", "CHANGE-THIS-PASSWORD"))
    user.save()
    doc, _ = Doctor.objects.get_or_create(user=user, defaults={
        "hospital": hospitals[dd["hospital_idx"]],
        "specialty": dd["specialty"],
        "qualification": dd["qualification"],
        "experience_years": dd["experience"],
        "consultation_fee": dd["fee"],
        "video_fee": dd["video_fee"],
        "bio": dd["bio"],
        "available_days": ["Saturday","Sunday","Monday","Tuesday","Wednesday"],
        "is_available_today": True,
        "accepts_video_consult": True,
        "is_verified": True,
        "rating": round(random.uniform(4.0, 4.9), 1),
        "rating_count": random.randint(50, 400),
        "total_patients": random.randint(200, 2000),
    })
    doctors.append(doc)
print(f"✓ {len(doctors)} doctors seeded")

# ── Patients ──
patients_data = [
    {"name": "Rahim Uddin", "email": "rahim@gmail.com", "phone": "01711111111",
     "gender": "male", "blood_group": "A+", "division": "Rajshahi"},
    {"name": "Sumaiya Khatun", "email": "sumaiya@gmail.com", "phone": "01722222222",
     "gender": "female", "blood_group": "B+", "division": "Dhaka"},
    {"name": "Habib Rahman", "email": "habib@gmail.com", "phone": "01733333333",
     "gender": "male", "blood_group": "O+", "division": "Chittagong"},
    {"name": "Moriam Begum", "email": "moriam@gmail.com", "phone": "01744444444",
     "gender": "female", "blood_group": "AB+", "division": "Sylhet"},
]

patients = []
for pd_data in patients_data:
    user, _ = User.objects.get_or_create(
        email=pd_data["email"],
        defaults={"full_name": pd_data["name"], "phone": pd_data["phone"],
                  "role": "patient", "is_verified": True}
    )
    user.set_password(os.getenv("SEED_PATIENT_PASS", "CHANGE-THIS-PASSWORD"))
    user.save()
    pat, _ = Patient.objects.get_or_create(user=user, defaults={
        "gender": pd_data["gender"],
        "blood_group": pd_data["blood_group"],
        "division": pd_data["division"],
        "date_of_birth": datetime.date(1990, random.randint(1,12), random.randint(1,28)),
    })
    patients.append(pat)
print(f"✓ {len(patients)} patients seeded")

# ── Medicines ──
medicines_data = [
    {"name": "Napa 500mg", "generic_name": "Paracetamol", "company": "Beximco",
     "medicine_type": "otc", "category": "pain", "price": 8, "unit": "strip/10",
     "stock_quantity": 500},
    {"name": "Napa Extra", "generic_name": "Paracetamol + Caffeine", "company": "Beximco",
     "medicine_type": "otc", "category": "pain", "price": 12, "unit": "strip/10",
     "stock_quantity": 300},
    {"name": "Amoxicillin 500mg", "generic_name": "Amoxicillin Trihydrate", "company": "ACI",
     "medicine_type": "rx", "category": "antibiotic", "price": 85, "unit": "strip/10",
     "stock_quantity": 200},
    {"name": "Metformin 500mg", "generic_name": "Metformin HCl", "company": "Square",
     "medicine_type": "rx", "category": "diabetes", "price": 45, "unit": "strip/14",
     "stock_quantity": 150},
    {"name": "Cetirizine 10mg", "generic_name": "Cetirizine HCl", "company": "Opsonin",
     "medicine_type": "otc", "category": "allergy", "price": 20, "unit": "strip/10",
     "stock_quantity": 400},
    {"name": "Vitamin C 500mg", "generic_name": "Ascorbic Acid", "company": "Renata",
     "medicine_type": "otc", "category": "vitamin", "price": 65, "unit": "bottle/30",
     "stock_quantity": 250},
    {"name": "Omeprazole 20mg", "generic_name": "Omeprazole", "company": "Eskayef",
     "medicine_type": "rx", "category": "gastro", "price": 55, "unit": "strip/14",
     "stock_quantity": 18},
    {"name": "Amlodipine 5mg", "generic_name": "Amlodipine Besilate", "company": "Drug Intl",
     "medicine_type": "rx", "category": "cardiac", "price": 35, "unit": "strip/14",
     "stock_quantity": 100},
    {"name": "Zinc 20mg", "generic_name": "Zinc Sulphate", "company": "ACI",
     "medicine_type": "otc", "category": "vitamin", "price": 30, "unit": "strip/10",
     "stock_quantity": 180},
    {"name": "Betadine Solution", "generic_name": "Povidone Iodine", "company": "Eskayef",
     "medicine_type": "otc", "category": "skin", "price": 85, "unit": "bottle/100ml",
     "stock_quantity": 90},
    {"name": "Vitamin D3 1000IU", "generic_name": "Cholecalciferol", "company": "Square",
     "medicine_type": "otc", "category": "vitamin", "price": 120, "unit": "bottle/30",
     "stock_quantity": 220},
    {"name": "Atorvastatin 10mg", "generic_name": "Atorvastatin Calcium", "company": "Incepta",
     "medicine_type": "rx", "category": "cardiac", "price": 95, "unit": "strip/10",
     "stock_quantity": 75},
    {"name": "Salbutamol Inhaler", "generic_name": "Salbutamol Sulphate", "company": "GSK",
     "medicine_type": "rx", "category": "respiratory", "price": 220, "unit": "inhaler",
     "stock_quantity": 0},
    {"name": "Neopeptine Drops", "generic_name": "Simethicone", "company": "Renata",
     "medicine_type": "otc", "category": "child", "price": 110, "unit": "bottle/15ml",
     "stock_quantity": 15},
    {"name": "Optive Eye Drops", "generic_name": "Carboxymethylcellulose", "company": "Allergan",
     "medicine_type": "otc", "category": "eye", "price": 185, "unit": "bottle/10ml",
     "stock_quantity": 0},
    {"name": "Cough Syrup DM", "generic_name": "Dextromethorphan", "company": "Beximco",
     "medicine_type": "otc", "category": "respiratory", "price": 75, "unit": "bottle/100ml",
     "stock_quantity": 120},
]

for md in medicines_data:
    Medicine.objects.get_or_create(name=md["name"], defaults=md)
print(f"✓ {len(medicines_data)} medicines seeded")

# ── Sample Appointments ──
statuses = ["confirmed", "confirmed", "confirmed", "pending", "completed", "cancelled"]
if patients and doctors:
    for i in range(min(6, len(patients) * len(doctors))):
        pat = patients[i % len(patients)]
        doc = doctors[i % len(doctors)]
        date = datetime.date.today() + datetime.timedelta(days=random.randint(-5, 10))
        Appointment.objects.get_or_create(
            patient=pat, doctor=doc, appointment_date=date,
            time_slot=f"{9+i}:00 AM",
            defaults={
                "hospital": doc.hospital,
                "visit_type": "in_person",
                "status": statuses[i % len(statuses)],
                "fee": doc.consultation_fee,
                "commission_amount": float(doc.consultation_fee) * 0.05,
                "chief_complaint": "General consultation",
                "is_paid": random.choice([True, False]),
            }
        )
print(f"✓ Sample appointments seeded")

# ── Daily Snapshots (last 30 days) ──
today = datetime.date.today()
for i in range(30):
    snap_date = today - datetime.timedelta(days=29-i)
    DailySnapshot.objects.get_or_create(date=snap_date, defaults={
        "total_appointments": random.randint(40, 120),
        "confirmed_appointments": random.randint(30, 100),
        "cancelled_appointments": random.randint(2, 15),
        "new_patients": random.randint(5, 30),
        "new_doctors": random.randint(0, 2),
        "new_hospitals": 0,
        "pharmacy_orders": random.randint(10, 50),
        "pharmacy_revenue": random.uniform(2000, 8000),
        "booking_commission": random.uniform(1000, 4000),
        "total_revenue": random.uniform(5000, 20000),
    })
print(f"✓ 30-day analytics snapshots seeded")

print("\n✅ SEEDING COMPLETE!")
print("=" * 50)
print("Login credentials:")
print("  Admin:   admin@medfind.com  / (see SEED_ADMIN_PASS env var)")
print("  Doctor:  ahmed@medfind.com  / Doctor@1234")
print("  Patient: rahim@gmail.com    / Patient@1234")
print("=" * 50)
