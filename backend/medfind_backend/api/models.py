"""
Models for MEDFIND - Hospital Management System
Using MongoEngine for MongoDB ORM
"""

from mongoengine import (
    Document, StringField, EmailField, IntField, ListField,
    BooleanField, DateTimeField, FloatField, ReferenceField,
    ImageField, URLField, DictField, EmbeddedDocument,
    EmbeddedDocumentField, DynamicField, NotUniqueError, ValidationError
)
from datetime import datetime


class Address(EmbeddedDocument):
    """Embedded document for address"""
    street = StringField(required=True)
    city = StringField(required=True)
    state = StringField()
    country = StringField()
    postal_code = StringField()
    latitude = FloatField()
    longitude = FloatField()


class WorkingHours(EmbeddedDocument):
    """Embedded document for working hours"""
    day = StringField(required=True)
    opening_time = StringField()  # Format: HH:MM
    closing_time = StringField()  # Format: HH:MM
    is_closed = BooleanField(default=False)


class Hospital(Document):
    """Hospital Model"""
    name = StringField(required=True, unique=True)
    email = EmailField(required=True)
    phone = StringField(required=True)
    description = StringField()
    address = EmbeddedDocumentField(Address, required=True)
    logo = URLField()
    website = URLField()
    license_number = StringField(unique=True)
    
    # Features and facilities
    specialties = ListField(StringField())  # e.g., ['Cardiology', 'Neurology']
    bed_count = IntField()
    ambulance_available = BooleanField(default=True)
    emergency_services = BooleanField(default=True)
    
    # Rating and reviews
    rating = FloatField(default=0.0)
    review_count = IntField(default=0)
    
    # Operating hours
    working_hours = ListField(EmbeddedDocumentField(WorkingHours))
    
    # Metadata
    created_at = DateTimeField(default=datetime.utcnow)
    updated_at = DateTimeField(default=datetime.utcnow)
    is_active = BooleanField(default=True)
    
    meta = {
        'collection': 'hospitals',
        'indexes': [
            'name',
            'city',
            'email',
            ('address.city', 'specialties'),  # Compound index
        ]
    }

    def __str__(self):
        return self.name


class Doctor(Document):
    """Doctor Model"""
    first_name = StringField(required=True)
    last_name = StringField(required=True)
    email = EmailField(unique=True, required=True)
    phone = StringField(required=True)
    specialization = StringField(required=True)
    qualifications = ListField(StringField())
    experience_years = IntField()
    
    # Hospital association
    hospital = ReferenceField(Hospital, required=True)
    
    # Availability and schedule
    consultation_fee = FloatField(required=True)
    available_days = ListField(StringField())  # e.g., ['Monday', 'Tuesday']
    working_hours = EmbeddedDocumentField(WorkingHours)
    
    # Rating
    rating = FloatField(default=0.0)
    review_count = IntField(default=0)
    
    # Additional info
    bio = StringField()
    profile_image = URLField()
    license_number = StringField(unique=True)
    
    # Metadata
    created_at = DateTimeField(default=datetime.utcnow)
    updated_at = DateTimeField(default=datetime.utcnow)
    is_active = BooleanField(default=True)
    
    meta = {
        'collection': 'doctors',
        'indexes': [
            'email',
            'specialization',
            ('hospital', 'specialization'),  # Compound index
        ]
    }

    def __str__(self):
        return f"Dr. {self.first_name} {self.last_name}"


class Patient(Document):
    """Patient Model"""
    first_name = StringField(required=True)
    last_name = StringField(required=True)
    email = EmailField(unique=True, required=True)
    phone = StringField(required=True)
    password_hash = StringField()  # Store hashed password
    
    # Personal info
    date_of_birth = DateTimeField()
    gender = StringField(choices=['Male', 'Female', 'Other'])
    blood_group = StringField(choices=['A+', 'A-', 'B+', 'B-', 'AB+', 'AB-', 'O+', 'O-'])
    
    # Contact details
    address = EmbeddedDocumentField(Address)
    emergency_contact = StringField()
    emergency_contact_phone = StringField()
    
    # Medical history
    medical_conditions = ListField(StringField())
    allergies = ListField(StringField())
    medications = ListField(StringField())
    
    # Account info
    created_at = DateTimeField(default=datetime.utcnow)
    updated_at = DateTimeField(default=datetime.utcnow)
    is_active = BooleanField(default=True)
    
    meta = {
        'collection': 'patients',
        'indexes': [
            'email',
            'phone',
        ]
    }

    def __str__(self):
        return f"{self.first_name} {self.last_name}"


class Appointment(Document):
    """Appointment Model"""
    patient = ReferenceField(Patient, required=True)
    doctor = ReferenceField(Doctor, required=True)
    hospital = ReferenceField(Hospital, required=True)
    
    appointment_date = DateTimeField(required=True)
    appointment_type = StringField(required=True, choices=['In-Person', 'Online', 'Phone'])
    
    reason_for_visit = StringField()
    status = StringField(required=True, choices=['Scheduled', 'Completed', 'Cancelled', 'No-Show'])
    
    notes = StringField()
    prescription = StringField()
    
    created_at = DateTimeField(default=datetime.utcnow)
    updated_at = DateTimeField(default=datetime.utcnow)
    
    meta = {
        'collection': 'appointments',
        'indexes': [
            ('patient', 'appointment_date'),
            ('doctor', 'appointment_date'),
            'status',
        ]
    }

    def __str__(self):
        return f"Appointment: {self.patient.first_name} with Dr. {self.doctor.first_name}"


class LabTest(Document):
    """Laboratory Test Model"""
    patient = ReferenceField(Patient, required=True)
    hospital = ReferenceField(Hospital, required=True)
    
    test_name = StringField(required=True)
    test_code = StringField(unique=True, required=True)
    description = StringField()
    category = StringField(required=True)  # e.g., 'Blood', 'X-Ray', 'Ultrasound'
    cost = FloatField(required=True)
    
    test_date = DateTimeField()
    result_date = DateTimeField()
    status = StringField(required=True, choices=['Pending', 'Completed', 'Cancelled'])
    
    result = DictField()  # Store test results as dictionary
    report_file = URLField()
    
    created_at = DateTimeField(default=datetime.utcnow)
    updated_at = DateTimeField(default=datetime.utcnow)
    
    meta = {
        'collection': 'lab_tests',
        'indexes': [
            ('patient', 'test_date'),
            'status',
        ]
    }

    def __str__(self):
        return f"{self.test_name} - {self.patient.first_name}"


class Billing(Document):
    """Billing/Invoice Model"""
    patient = ReferenceField(Patient, required=True)
    hospital = ReferenceField(Hospital, required=True)
    
    invoice_number = StringField(unique=True, required=True)
    invoice_date = DateTimeField(default=datetime.utcnow)
    
    # Line items
    services = ListField(DictField())  # List of services with cost
    total_amount = FloatField(required=True)
    discount = FloatField(default=0.0)
    tax = FloatField(default=0.0)
    payable_amount = FloatField(required=True)
    
    # Payment info
    payment_method = StringField(choices=['Cash', 'Card', 'Cheque', 'Online Transfer'])
    payment_status = StringField(required=True, choices=['Pending', 'Paid', 'Failed', 'Refunded'])
    paid_date = DateTimeField()
    
    description = StringField()
    notes = StringField()
    
    created_at = DateTimeField(default=datetime.utcnow)
    updated_at = DateTimeField(default=datetime.utcnow)
    
    meta = {
        'collection': 'billing',
        'indexes': [
            'invoice_number',
            ('patient', 'invoice_date'),
            'payment_status',
        ]
    }

    def __str__(self):
        return f"Invoice: {self.invoice_number}"


class Pharmacy(Document):
    """Medicine/Pharmacy Model"""
    medicine_name = StringField(required=True, unique=True)
    medicine_code = StringField(unique=True, required=True)
    description = StringField()
    
    # Medical details
    generic_name = StringField()
    strength = StringField()  # e.g., '500mg'
    form = StringField(choices=['Tablet', 'Capsule', 'Liquid', 'Injection', 'Cream', 'Other'])
    
    # Inventory
    quantity_in_stock = IntField(default=0)
    reorder_level = IntField()
    price = FloatField(required=True)
    
    # Supplier info
    supplier_name = StringField()
    manufacturer = StringField()
    batch_number = StringField()
    expiry_date = DateTimeField()
    
    # Hospital association
    hospital = ReferenceField(Hospital, required=True)
    
    created_at = DateTimeField(default=datetime.utcnow)
    updated_at = DateTimeField(default=datetime.utcnow)
    is_active = BooleanField(default=True)
    
    meta = {
        'collection': 'pharmacy',
        'indexes': [
            'medicine_name',
            'medicine_code',
            ('hospital', 'medicine_name'),
        ]
    }

    def __str__(self):
        return self.medicine_name


class MedicalHistory(Document):
    """Medical History Record Model"""
    patient = ReferenceField(Patient, required=True)
    doctor = ReferenceField(Doctor)
    hospital = ReferenceField(Hospital, required=True)
    
    record_date = DateTimeField(default=datetime.utcnow)
    visit_type = StringField()  # e.g., 'Check-up', 'Follow-up', 'Emergency'
    
    symptoms = ListField(StringField())
    diagnosis = StringField()
    prescription = StringField()
    notes = StringField()
    
    # Vital signs
    vital_signs = DictField()  # e.g., {'blood_pressure': '120/80', 'temperature': '98.6'}
    
    # Follow-up
    follow_up_date = DateTimeField()
    follow_up_notes = StringField()
    
    created_at = DateTimeField(default=datetime.utcnow)
    updated_at = DateTimeField(default=datetime.utcnow)
    
    meta = {
        'collection': 'medical_history',
        'indexes': [
            ('patient', 'record_date'),
            ('hospital', 'record_date'),
        ]
    }

    def __str__(self):
        return f"Medical Record: {self.patient.first_name} - {self.record_date}"
