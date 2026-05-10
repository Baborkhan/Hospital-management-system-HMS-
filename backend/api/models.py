from django.db import models


class Doctor(models.Model):
    name = models.CharField(max_length=255)
    specialization = models.CharField(max_length=255)
    email = models.EmailField(blank=True)
    phone = models.CharField(max_length=50, blank=True)
    available = models.BooleanField(default=True)

    def __str__(self):
        return self.name


class Patient(models.Model):
    first_name = models.CharField(max_length=150)
    last_name = models.CharField(max_length=150)
    date_of_birth = models.DateField(blank=True, null=True)
    gender = models.CharField(max_length=50, blank=True)
    phone = models.CharField(max_length=50, blank=True)
    email = models.EmailField(blank=True)
    address = models.TextField(blank=True)
    medical_history = models.TextField(blank=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"


class Appointment(models.Model):
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE)
    appointment_date = models.DateTimeField()
    reason = models.TextField(blank=True)
    status = models.CharField(max_length=50, default='Scheduled')

    def __str__(self):
        return f"Appointment {self.id} - {self.patient} with {self.doctor}"


class Admission(models.Model):
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    admitted_at = models.DateTimeField()
    discharged_at = models.DateTimeField(blank=True, null=True)
    ward = models.CharField(max_length=150)
    notes = models.TextField(blank=True)

    def __str__(self):
        return f"Admission {self.id} for {self.patient}"


class Bill(models.Model):
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    description = models.TextField(blank=True)
    paid = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Bill {self.id} for {self.patient}"
