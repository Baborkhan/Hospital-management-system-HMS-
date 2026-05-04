"""
Sample data seeding script for MEDFIND
Run this script to populate database with sample data
Usage: python seed_data.py
"""

import os
import sys
import django
from datetime import datetime, timedelta

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'settings')
django.setup()

from api.models import (
    Hospital, Doctor, Patient, Appointment, LabTest,
    Billing, Pharmacy, MedicalHistory
)
from core_app.models import User


def clear_collections():
    """Clear all collections"""
    print("🗑️  Clearing existing data...")
    Hospital.objects.all().delete()
    Doctor.objects.all().delete()
    Patient.objects.all().delete()
    Appointment.objects.all().delete()
    LabTest.objects.all().delete()
    Billing.objects.all().delete()
    Pharmacy.objects.all().delete()
    MedicalHistory.objects.all().delete()
    User.objects.all().delete()
    print("✅ Data cleared successfully!")


def seed_hospitals():
    """Seed hospital data"""
    print("🏥 Seeding hospitals...")
    hospitals_data = [
        {
            "name": "City General Hospital",
            "email": "info@citygeneral.com",
            "phone": "+1-555-0101",
            "license_number": "LIC001",
            "address": {
                "street": "123 Main St",
                "city": "New York",
                "state": "NY",
                "zip_code": "10001",
                "country": "USA"
            },
            "specialties": ["Cardiology", "Neurology", "Orthopedics"],
            "bed_count": 200,
            "rating": 4.5,
            "description": "A leading healthcare facility providing comprehensive medical services."
        },
        {
            "name": "Metro Health Center",
            "email": "contact@metrohealth.com",
            "phone": "+1-555-0102",
            "license_number": "LIC002",
            "address": {
                "street": "456 Health Ave",
                "city": "Los Angeles",
                "state": "CA",
                "zip_code": "90210",
                "country": "USA"
            },
            "specialties": ["Pediatrics", "Dermatology", "Gynecology"],
            "bed_count": 150,
            "rating": 4.2,
            "description": "Specialized in family healthcare and pediatric services."
        }
    ]
    
    hospitals = []
    for data in hospitals_data:
        hospital = Hospital.objects.create(**data)
        hospitals.append(hospital)
        print(f"  ✅ Created hospital: {hospital.name}")
    
    return hospitals


def seed_doctors():
    """Seed doctor data"""
    print("👨‍⚕️ Seeding doctors...")
    hospitals = list(Hospital.objects.all())
    
    doctors_data = [
        {
            "first_name": "Sarah",
            "last_name": "Johnson",
            "email": "sarah.johnson@citygeneral.com",
            "phone": "+1-555-0201",
            "specialization": "Cardiology",
            "license_number": "MD12345",
            "experience_years": 15,
            "qualifications": ["MD from Harvard Medical School"],
            "hospital": hospitals[0],
            "consultation_fee": 200.00,
            "rating": 4.8
        },
        {
            "first_name": "Michael",
            "last_name": "Chen",
            "email": "michael.chen@metrohealth.com",
            "phone": "+1-555-0202",
            "specialization": "Pediatrics",
            "license_number": "MD12346",
            "experience_years": 12,
            "qualifications": ["MD from Johns Hopkins"],
            "hospital": hospitals[1],
            "consultation_fee": 150.00,
            "rating": 4.6
        }
    ]
    
    doctors = []
    for data in doctors_data:
        doctor = Doctor.objects.create(**data)
        doctors.append(doctor)
        print(f"  ✅ Created doctor: {doctor.first_name} {doctor.last_name}")
    
    return doctors


def seed_patients():
    """Seed patient data"""
    print("👤 Seeding patients...")
    
    patients_data = [
        {
            "name": "John Smith",
            "email": "john.smith@email.com",
            "phone": "+1-555-0301",
            "date_of_birth": "1985-03-15",
            "gender": "Male",
            "address": {
                "street": "789 Oak St",
                "city": "New York",
                "state": "NY",
                "zip_code": "10002",
                "country": "USA"
            },
            "emergency_contact": {
                "name": "Jane Smith",
                "phone": "+1-555-0302",
                "relationship": "Wife"
            },
            "medical_history": ["Hypertension", "Allergies"],
            "blood_group": "O+",
            "insurance_provider": "Blue Cross",
            "insurance_number": "BC123456"
        },
        {
            "name": "Emily Davis",
            "email": "emily.davis@email.com",
            "phone": "+1-555-0303",
            "date_of_birth": "1990-07-22",
            "gender": "Female",
            "address": {
                "street": "321 Pine St",
                "city": "Los Angeles",
                "state": "CA",
                "zip_code": "90211",
                "country": "USA"
            },
            "emergency_contact": {
                "name": "Robert Davis",
                "phone": "+1-555-0304",
                "relationship": "Husband"
            },
            "medical_history": ["Asthma"],
            "blood_group": "A-",
            "insurance_provider": "Aetna",
            "insurance_number": "AE789012"
        }
    ]
    
    patients = []
    for data in patients_data:
        patient = Patient.objects.create(**data)
        patients.append(patient)
        print(f"  ✅ Created patient: {patient.name}")
    
    return patients


def seed_appointments():
    """Seed appointment data"""
    print("📅 Seeding appointments...")
    doctors = list(Doctor.objects.all())
    patients = list(Patient.objects.all())
    hospitals = list(Hospital.objects.all())
    
    appointments_data = [
        {
            "patient": patients[0],
            "doctor": doctors[0],
            "hospital": hospitals[0],
            "appointment_date": datetime.now() + timedelta(days=1),
            "appointment_time": "10:00:00",
            "reason": "Regular checkup",
            "status": "Scheduled",
            "notes": "Patient reports mild chest pain"
        },
        {
            "patient": patients[1],
            "doctor": doctors[1],
            "hospital": hospitals[1],
            "appointment_date": datetime.now() + timedelta(days=2),
            "appointment_time": "14:30:00",
            "reason": "Child vaccination",
            "status": "Scheduled",
            "notes": "Annual vaccination schedule"
        }
    ]
    
    appointments = []
    for data in appointments_data:
        appointment = Appointment.objects.create(**data)
        appointments.append(appointment)
        print(f"  ✅ Created appointment for: {appointment.patient.name}")
    
    return appointments


def seed_lab_tests():
    """Seed lab test data"""
    print("🧪 Seeding lab tests...")
    patients = list(Patient.objects.all())
    hospitals = list(Hospital.objects.all())
    
    lab_tests_data = [
        {
            "patient": patients[0],
            "hospital": hospitals[0],
            "test_name": "Blood Test",
            "test_code": "BT001",
            "test_date": datetime.now() - timedelta(days=1),
            "results": {
                "hemoglobin": "14.2 g/dL",
                "white_blood_cells": "7500 /μL",
                "platelets": "250000 /μL"
            },
            "status": "Completed",
            "notes": "Normal blood count"
        },
        {
            "patient": patients[1],
            "hospital": hospitals[1],
            "test_name": "X-Ray Chest",
            "test_code": "XR001",
            "test_date": datetime.now() - timedelta(days=2),
            "results": {
                "findings": "Clear lung fields",
                "impression": "No abnormalities detected"
            },
            "status": "Completed",
            "notes": "Routine chest X-ray"
        }
    ]
    
    lab_tests = []
    for data in lab_tests_data:
        lab_test = LabTest.objects.create(**data)
        lab_tests.append(lab_test)
        print(f"  ✅ Created lab test: {lab_test.test_name}")
    
    return lab_tests


def seed_billing():
    """Seed billing data"""
    print("💰 Seeding billing...")
    patients = list(Patient.objects.all())
    hospitals = list(Hospital.objects.all())
    
    billing_data = [
        {
            "patient": patients[0],
            "hospital": hospitals[0],
            "invoice_number": "INV001",
            "invoice_date": datetime.now() - timedelta(days=1),
            "services": [
                {"name": "Consultation", "amount": 200.00},
                {"name": "Blood Test", "amount": 50.00}
            ],
            "total_amount": 250.00,
            "paid_amount": 250.00,
            "payment_status": "Paid",
            "payment_method": "Credit Card",
            "due_date": datetime.now() + timedelta(days=30)
        },
        {
            "patient": patients[1],
            "hospital": hospitals[1],
            "invoice_number": "INV002",
            "invoice_date": datetime.now() - timedelta(days=2),
            "services": [
                {"name": "Consultation", "amount": 150.00},
                {"name": "X-Ray", "amount": 100.00}
            ],
            "total_amount": 250.00,
            "paid_amount": 0.00,
            "payment_status": "Pending",
            "payment_method": "Insurance",
            "due_date": datetime.now() + timedelta(days=30)
        }
    ]
    
    billing_records = []
    for data in billing_data:
        billing = Billing.objects.create(**data)
        billing_records.append(billing)
        print(f"  ✅ Created billing record: {billing.invoice_number}")
    
    return billing_records


def seed_pharmacy():
    """Seed pharmacy data"""
    print("💊 Seeding pharmacy...")
    hospitals = list(Hospital.objects.all())
    
    pharmacy_data = [
        {
            "hospital": hospitals[0],
            "medicine_name": "Aspirin",
            "medicine_code": "ASP001",
            "generic_name": "Acetylsalicylic Acid",
            "dosage": "100mg",
            "manufacturer": "PharmaCorp",
            "batch_number": "BATCH001",
            "expiry_date": datetime.now() + timedelta(days=365),
            "quantity": 100,
            "unit_price": 5.00,
            "category": "Pain Relief"
        },
        {
            "hospital": hospitals[1],
            "medicine_name": "Amoxicillin",
            "medicine_code": "AMX001",
            "generic_name": "Amoxicillin",
            "dosage": "500mg",
            "manufacturer": "MediPharm",
            "batch_number": "BATCH002",
            "expiry_date": datetime.now() + timedelta(days=300),
            "quantity": 50,
            "unit_price": 12.00,
            "category": "Antibiotic"
        }
    ]
    
    pharmacy_items = []
    for data in pharmacy_data:
        item = Pharmacy.objects.create(**data)
        pharmacy_items.append(item)
        print(f"  ✅ Created pharmacy item: {item.medicine_name}")
    
    return pharmacy_items


def seed_medical_history():
    """Seed medical history data"""
    print("📋 Seeding medical history...")
    patients = list(Patient.objects.all())
    doctors = list(Doctor.objects.all())
    hospitals = list(Hospital.objects.all())
    
    medical_history_data = [
        {
            "patient": patients[0],
            "doctor": doctors[0],
            "hospital": hospitals[0],
            "record_date": datetime.now() - timedelta(days=30),
            "diagnosis": "Hypertension",
            "treatment": "Prescribed medication",
            "prescription": "Lisinopril 10mg daily",
            "notes": "Patient shows improvement",
            "follow_up_date": datetime.now() + timedelta(days=30)
        },
        {
            "patient": patients[1],
            "doctor": doctors[1],
            "hospital": hospitals[1],
            "record_date": datetime.now() - timedelta(days=15),
            "diagnosis": "Common Cold",
            "treatment": "Rest and fluids",
            "prescription": "Over-the-counter medications",
            "notes": "Mild symptoms, recovering well",
            "follow_up_date": datetime.now() + timedelta(days=7)
        }
    ]
    
    medical_records = []
    for data in medical_history_data:
        record = MedicalHistory.objects.create(**data)
        medical_records.append(record)
        print(f"  ✅ Created medical record for: {record.patient.name}")
    
    return medical_records


def main():
    """Main seeding function"""
    print("🌱 Starting database seeding...")
    
    try:
        clear_collections()
        hospitals = seed_hospitals()
        doctors = seed_doctors()
        patients = seed_patients()
        appointments = seed_appointments()
        lab_tests = seed_lab_tests()
        billing = seed_billing()
        pharmacy = seed_pharmacy()
        medical_history = seed_medical_history()
        
        print("\n🎉 Database seeding completed successfully!")
        print(f"   Hospitals: {len(hospitals)}")
        print(f"   Doctors: {len(doctors)}")
        print(f"   Patients: {len(patients)}")
        print(f"   Appointments: {len(appointments)}")
        print(f"   Lab Tests: {len(lab_tests)}")
        print(f"   Billing Records: {len(billing)}")
        print(f"   Pharmacy Items: {len(pharmacy)}")
        print(f"   Medical Records: {len(medical_history)}")
        
    except Exception as e:
        print(f"❌ Error during seeding: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()


def create_hospitals():
    """Create sample hospitals"""
    print("\n🏥 Creating hospitals...")
    
    hospitals_data = [
        {
            'name': 'City Central Hospital',
            'email': 'info@citycentral.com',
            'phone': '+1-555-0101',
            'description': 'Leading healthcare provider in the city',
            'address': Address(
                street='123 Medical Avenue',
                city='New York',
                state='NY',
                country='USA',
                postal_code='10001',
                latitude=40.7128,
                longitude=-74.0060
            ),
            'logo': 'https://via.placeholder.com/200',
            'website': 'https://citycentral.com',
            'license_number': 'NYC-HOSP-001',
            'specialties': ['Cardiology', 'Neurology', 'Orthopedics', 'Pediatrics'],
            'bed_count': 500,
            'ambulance_available': True,
            'emergency_services': True,
            'is_active': True,
        },
        {
            'name': 'Sunrise Medical Complex',
            'email': 'contact@sunrise.com',
            'phone': '+1-555-0102',
            'description': 'Specialized medical center for advanced treatments',
            'address': Address(
                street='456 Health Street',
                city='Los Angeles',
                state='CA',
                country='USA',
                postal_code='90001',
                latitude=34.0522,
                longitude=-118.2437
            ),
            'logo': 'https://via.placeholder.com/200',
            'website': 'https://sunrise.com',
            'license_number': 'LAX-HOSP-001',
            'specialties': ['Oncology', 'Cardiology', 'Surgery', 'Internal Medicine'],
            'bed_count': 300,
            'ambulance_available': True,
            'emergency_services': True,
            'is_active': True,
        },
        {
            'name': 'Green Valley Hospital',
            'email': 'admin@greenvalley.com',
            'phone': '+1-555-0103',
            'description': 'Community healthcare facility with modern equipment',
            'address': Address(
                street='789 Wellness Road',
                city='Chicago',
                state='IL',
                country='USA',
                postal_code='60601',
                latitude=41.8781,
                longitude=-87.6298
            ),
            'logo': 'https://via.placeholder.com/200',
            'website': 'https://greenvalley.com',
            'license_number': 'CHI-HOSP-001',
            'specialties': ['General Practice', 'Pediatrics', 'Gynecology', 'Orthopedics'],
            'bed_count': 200,
            'ambulance_available': True,
            'emergency_services': True,
            'is_active': True,
        }
    ]

    hospitals = []
    for data in hospitals_data:
        hospital = Hospital(**data)
        hospital.save()
        hospitals.append(hospital)
        print(f"  ✅ Created: {hospital.name}")
    
    return hospitals


def create_doctors(hospitals):
    """Create sample doctors"""
    print("\n👨‍⚕️  Creating doctors...")
    
    doctors_data = [
        {
            'first_name': 'John',
            'last_name': 'Smith',
            'email': 'john.smith@hospital.com',
            'phone': '+1-555-1001',
            'specialization': 'Cardiology',
            'qualifications': ['MD', 'Board Certified Cardiologist'],
            'experience_years': 15,
            'hospital': hospitals[0],
            'consultation_fee': 150.0,
            'available_days': ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday'],
            'bio': 'Expert cardiologist with 15 years of experience',
            'profile_image': 'https://via.placeholder.com/150',
            'license_number': 'MD-CAR-001',
            'is_active': True,
        },
        {
            'first_name': 'Sarah',
            'last_name': 'Johnson',
            'email': 'sarah.johnson@hospital.com',
            'phone': '+1-555-1002',
            'specialization': 'Neurology',
            'qualifications': ['MD', 'Neurology Specialist'],
            'experience_years': 10,
            'hospital': hospitals[0],
            'consultation_fee': 120.0,
            'available_days': ['Monday', 'Wednesday', 'Friday'],
            'bio': 'Specialized in neurological disorders',
            'profile_image': 'https://via.placeholder.com/150',
            'license_number': 'MD-NEU-001',
            'is_active': True,
        },
        {
            'first_name': 'Michael',
            'last_name': 'Williams',
            'email': 'michael.williams@hospital.com',
            'phone': '+1-555-1003',
            'specialization': 'Orthopedics',
            'qualifications': ['MD', 'Orthopedic Surgeon'],
            'experience_years': 12,
            'hospital': hospitals[1],
            'consultation_fee': 130.0,
            'available_days': ['Tuesday', 'Thursday', 'Friday'],
            'bio': 'Expert orthopedic surgeon',
            'profile_image': 'https://via.placeholder.com/150',
            'license_number': 'MD-ORT-001',
            'is_active': True,
        },
        {
            'first_name': 'Emma',
            'last_name': 'Davis',
            'email': 'emma.davis@hospital.com',
            'phone': '+1-555-1004',
            'specialization': 'Pediatrics',
            'qualifications': ['MD', 'Pediatrician'],
            'experience_years': 8,
            'hospital': hospitals[1],
            'consultation_fee': 100.0,
            'available_days': ['Monday', 'Tuesday', 'Wednesday', 'Thursday'],
            'bio': 'Pediatric specialist focused on child health',
            'profile_image': 'https://via.placeholder.com/150',
            'license_number': 'MD-PED-001',
            'is_active': True,
        }
    ]

    doctors = []
    for data in doctors_data:
        doctor = Doctor(**data)
        doctor.save()
        doctors.append(doctor)
        print(f"  ✅ Created: Dr. {doctor.first_name} {doctor.last_name}")
    
    return doctors


def create_patients():
    """Create sample patients"""
    print("\n👥 Creating patients...")
    
    patients_data = [
        {
            'first_name': 'Robert',
            'last_name': 'Brown',
            'email': 'robert.brown@email.com',
            'phone': '+1-555-2001',
            'date_of_birth': datetime(1980, 5, 15),
            'gender': 'Male',
            'blood_group': 'O+',
            'address': Address(
                street='100 Patient Street',
                city='New York',
                state='NY',
                country='USA',
                postal_code='10002'
            ),
            'emergency_contact': 'Jane Brown',
            'emergency_contact_phone': '+1-555-2002',
            'medical_conditions': ['Hypertension', 'Diabetes'],
            'allergies': ['Penicillin'],
            'medications': ['Lisinopril', 'Metformin'],
            'is_active': True,
        },
        {
            'first_name': 'Lisa',
            'last_name': 'Anderson',
            'email': 'lisa.anderson@email.com',
            'phone': '+1-555-2003',
            'date_of_birth': datetime(1990, 8, 20),
            'gender': 'Female',
            'blood_group': 'A+',
            'address': Address(
                street='200 Health Avenue',
                city='New York',
                state='NY',
                country='USA',
                postal_code='10003'
            ),
            'emergency_contact': 'Mark Anderson',
            'emergency_contact_phone': '+1-555-2004',
            'medical_conditions': ['Asthma'],
            'allergies': ['Latex'],
            'medications': ['Albuterol'],
            'is_active': True,
        },
        {
            'first_name': 'David',
            'last_name': 'Martinez',
            'email': 'david.martinez@email.com',
            'phone': '+1-555-2005',
            'date_of_birth': datetime(1975, 3, 10),
            'gender': 'Male',
            'blood_group': 'B+',
            'address': Address(
                street='300 Wellness Road',
                city='Los Angeles',
                state='CA',
                country='USA',
                postal_code='90002'
            ),
            'emergency_contact': 'Maria Martinez',
            'emergency_contact_phone': '+1-555-2006',
            'medical_conditions': ['Heart Disease'],
            'allergies': ['Aspirin'],
            'medications': ['Atorvastatin', 'Carvedilol'],
            'is_active': True,
        }
    ]

    patients = []
    for data in patients_data:
        patient = Patient(**data)
        patient.save()
        patients.append(patient)
        print(f"  ✅ Created: {patient.first_name} {patient.last_name}")
    
    return patients


def create_appointments(patients, doctors, hospitals):
    """Create sample appointments"""
    print("\n📅 Creating appointments...")
    
    appointments_data = [
        {
            'patient': patients[0],
            'doctor': doctors[0],
            'hospital': hospitals[0],
            'appointment_date': datetime.now() + timedelta(days=5),
            'appointment_type': 'In-Person',
            'reason_for_visit': 'Cardiac Checkup',
            'status': 'Scheduled',
            'notes': 'Regular follow-up for heart condition',
        },
        {
            'patient': patients[1],
            'doctor': doctors[3],
            'hospital': hospitals[1],
            'appointment_date': datetime.now() + timedelta(days=3),
            'appointment_type': 'In-Person',
            'reason_for_visit': 'Pediatric Checkup',
            'status': 'Scheduled',
            'notes': 'Annual pediatric examination',
        },
        {
            'patient': patients[2],
            'doctor': doctors[0],
            'hospital': hospitals[0],
            'appointment_date': datetime.now() + timedelta(days=7),
            'appointment_type': 'Online',
            'reason_for_visit': 'Heart Disease Follow-up',
            'status': 'Scheduled',
            'notes': 'Online consultation for ongoing treatment',
        }
    ]

    appointments = []
    for data in appointments_data:
        appointment = Appointment(**data)
        appointment.save()
        appointments.append(appointment)
        print(f"  ✅ Created appointment for {appointment.patient.first_name}")
    
    return appointments


def create_pharmacy_items(hospitals):
    """Create sample pharmacy items"""
    print("\n💊 Creating pharmacy items...")
    
    pharmacy_data = [
        {
            'medicine_name': 'Aspirin 500mg',
            'medicine_code': 'ASP-500',
            'description': 'Pain reliever and fever reducer',
            'generic_name': 'Acetylsalicylic acid',
            'strength': '500mg',
            'form': 'Tablet',
            'quantity_in_stock': 500,
            'reorder_level': 100,
            'price': 5.0,
            'supplier_name': 'MediSupply Co',
            'manufacturer': 'Pharma Corp',
            'batch_number': 'BATCH-001',
            'expiry_date': datetime.now() + timedelta(days=365),
            'hospital': hospitals[0],
            'is_active': True,
        },
        {
            'medicine_name': 'Amoxicillin 250mg',
            'medicine_code': 'AMX-250',
            'description': 'Antibiotic for bacterial infections',
            'generic_name': 'Amoxicillin',
            'strength': '250mg',
            'form': 'Capsule',
            'quantity_in_stock': 300,
            'reorder_level': 100,
            'price': 3.50,
            'supplier_name': 'MediSupply Co',
            'manufacturer': 'Pharma Corp',
            'batch_number': 'BATCH-002',
            'expiry_date': datetime.now() + timedelta(days=365),
            'hospital': hospitals[1],
            'is_active': True,
        },
        {
            'medicine_name': 'Lisinopril 10mg',
            'medicine_code': 'LIS-10',
            'description': 'Blood pressure medication',
            'generic_name': 'Lisinopril',
            'strength': '10mg',
            'form': 'Tablet',
            'quantity_in_stock': 400,
            'reorder_level': 150,
            'price': 2.50,
            'supplier_name': 'MediSupply Co',
            'manufacturer': 'Pharma Corp',
            'batch_number': 'BATCH-003',
            'expiry_date': datetime.now() + timedelta(days=365),
            'hospital': hospitals[0],
            'is_active': True,
        }
    ]

    pharmacy_items = []
    for data in pharmacy_data:
        item = Pharmacy(**data)
        item.save()
        pharmacy_items.append(item)
        print(f"  ✅ Created: {item.medicine_name}")
    
    return pharmacy_items


def main():
    """Main seeding function"""
    print("=" * 50)
    print("🌱 MEDFIND Database Seeding Started")
    print("=" * 50)
    
    try:
        # Clear existing data
        clear_collections()
        
        # Create data
        hospitals = create_hospitals()
        doctors = create_doctors(hospitals)
        patients = create_patients()
        appointments = create_appointments(patients, doctors, hospitals)
        pharmacy = create_pharmacy_items(hospitals)
        
        print("\n" + "=" * 50)
        print("✅ Database seeding completed successfully!")
        print("=" * 50)
        print(f"""
📊 Summary:
  🏥 Hospitals: {len(hospitals)}
  👨‍⚕️  Doctors: {len(doctors)}
  👥 Patients: {len(patients)}
  📅 Appointments: {len(appointments)}
  💊 Medicines: {len(pharmacy)}

🚀 Next Steps:
  1. Start MongoDB: mongod
  2. Start Django: python manage.py runserver
  3. Visit: http://localhost:8000/api/hospitals/
  4. Try Portal: http://localhost:5500/basics/portal-selection.html
        """)
        
    except Exception as e:
        print(f"\n❌ Error during seeding: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == '__main__':
    main()
