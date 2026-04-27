"""
Views/ViewSets for API
Handles HTTP requests and returns responses
"""

from rest_framework import viewsets, status, filters
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination
from django.shortcuts import get_object_or_404
from .models import (
    Hospital, Doctor, Patient, Appointment, LabTest,
    Billing, Pharmacy, MedicalHistory
)
from .serializers import (
    HospitalSerializer, DoctorSerializer, PatientSerializer,
    AppointmentSerializer, LabTestSerializer, BillingSerializer,
    PharmacySerializer, MedicalHistorySerializer
)


class CustomPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 100


class HospitalViewSet(viewsets.ModelViewSet):
    """
    ViewSet for Hospital operations
    """
    serializer_class = HospitalSerializer
    pagination_class = CustomPagination
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['name', 'city', 'specialties']
    ordering_fields = ['name', 'rating', 'created_at']

    def get_queryset(self):
        queryset = Hospital.objects(is_active=True)
        
        # Filter by city
        city = self.request.query_params.get('city', None)
        if city:
            queryset = queryset(address__city=city)
        
        # Filter by specialty
        specialty = self.request.query_params.get('specialty', None)
        if specialty:
            queryset = queryset(specialties=specialty)
        
        return queryset

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    def retrieve(self, request, *args, **kwargs):
        hospital = Hospital.objects(pk=kwargs['pk']).first()
        if not hospital:
            return Response(
                {'error': 'Hospital not found'},
                status=status.HTTP_404_NOT_FOUND
            )
        serializer = self.get_serializer(hospital)
        return Response(serializer.data)

    @action(detail=True, methods=['get'])
    def doctors(self, request, pk=None):
        """Get all doctors in this hospital"""
        hospital = Hospital.objects(pk=pk).first()
        if not hospital:
            return Response(
                {'error': 'Hospital not found'},
                status=status.HTTP_404_NOT_FOUND
            )
        doctors = Doctor.objects(hospital=hospital, is_active=True)
        serializer = DoctorSerializer(doctors, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=['get'])
    def services(self, request, pk=None):
        """Get hospital services and specialties"""
        hospital = Hospital.objects(pk=pk).first()
        if not hospital:
            return Response(
                {'error': 'Hospital not found'},
                status=status.HTTP_404_NOT_FOUND
            )
        return Response({
            'specialties': hospital.specialties,
            'bed_count': hospital.bed_count,
            'ambulance_available': hospital.ambulance_available,
            'emergency_services': hospital.emergency_services,
        })


class DoctorViewSet(viewsets.ModelViewSet):
    """
    ViewSet for Doctor operations
    """
    serializer_class = DoctorSerializer
    pagination_class = CustomPagination
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['first_name', 'last_name', 'specialization']
    ordering_fields = ['first_name', 'rating', 'consultation_fee']

    def get_queryset(self):
        queryset = Doctor.objects(is_active=True)
        
        # Filter by specialization
        specialization = self.request.query_params.get('specialization', None)
        if specialization:
            queryset = queryset(specialization=specialization)
        
        # Filter by hospital
        hospital_id = self.request.query_params.get('hospital_id', None)
        if hospital_id:
            queryset = queryset(hospital__pk=hospital_id)
        
        return queryset

    def retrieve(self, request, *args, **kwargs):
        doctor = Doctor.objects(pk=kwargs['pk']).first()
        if not doctor:
            return Response(
                {'error': 'Doctor not found'},
                status=status.HTTP_404_NOT_FOUND
            )
        serializer = self.get_serializer(doctor)
        return Response(serializer.data)

    @action(detail=True, methods=['get'])
    def availability(self, request, pk=None):
        """Get doctor's availability"""
        doctor = Doctor.objects(pk=pk).first()
        if not doctor:
            return Response(
                {'error': 'Doctor not found'},
                status=status.HTTP_404_NOT_FOUND
            )
        return Response({
            'available_days': doctor.available_days,
            'consultation_fee': doctor.consultation_fee,
        })


class PatientViewSet(viewsets.ModelViewSet):
    """
    ViewSet for Patient operations
    """
    serializer_class = PatientSerializer
    pagination_class = CustomPagination

    def get_queryset(self):
        return Patient.objects(is_active=True)

    def retrieve(self, request, *args, **kwargs):
        patient = Patient.objects(pk=kwargs['pk']).first()
        if not patient:
            return Response(
                {'error': 'Patient not found'},
                status=status.HTTP_404_NOT_FOUND
            )
        serializer = self.get_serializer(patient)
        return Response(serializer.data)

    @action(detail=True, methods=['get'])
    def medical_history(self, request, pk=None):
        """Get patient's medical history"""
        patient = Patient.objects(pk=pk).first()
        if not patient:
            return Response(
                {'error': 'Patient not found'},
                status=status.HTTP_404_NOT_FOUND
            )
        history = MedicalHistory.objects(patient=patient)
        serializer = MedicalHistorySerializer(history, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=['get'])
    def appointments(self, request, pk=None):
        """Get patient's appointments"""
        patient = Patient.objects(pk=pk).first()
        if not patient:
            return Response(
                {'error': 'Patient not found'},
                status=status.HTTP_404_NOT_FOUND
            )
        appointments = Appointment.objects(patient=patient)
        serializer = AppointmentSerializer(appointments, many=True)
        return Response(serializer.data)


class AppointmentViewSet(viewsets.ModelViewSet):
    """
    ViewSet for Appointment operations
    """
    serializer_class = AppointmentSerializer
    pagination_class = CustomPagination

    def get_queryset(self):
        return Appointment.objects()

    def retrieve(self, request, *args, **kwargs):
        appointment = Appointment.objects(pk=kwargs['pk']).first()
        if not appointment:
            return Response(
                {'error': 'Appointment not found'},
                status=status.HTTP_404_NOT_FOUND
            )
        serializer = self.get_serializer(appointment)
        return Response(serializer.data)

    @action(detail=False, methods=['get'])
    def by_patient(self, request):
        """Get appointments for a specific patient"""
        patient_id = request.query_params.get('patient_id')
        if not patient_id:
            return Response(
                {'error': 'patient_id is required'},
                status=status.HTTP_400_BAD_REQUEST
            )
        appointments = Appointment.objects(patient__pk=patient_id)
        serializer = self.get_serializer(appointments, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'])
    def by_doctor(self, request):
        """Get appointments for a specific doctor"""
        doctor_id = request.query_params.get('doctor_id')
        if not doctor_id:
            return Response(
                {'error': 'doctor_id is required'},
                status=status.HTTP_400_BAD_REQUEST
            )
        appointments = Appointment.objects(doctor__pk=doctor_id)
        serializer = self.get_serializer(appointments, many=True)
        return Response(serializer.data)


class LabTestViewSet(viewsets.ModelViewSet):
    """
    ViewSet for Lab Test operations
    """
    serializer_class = LabTestSerializer
    pagination_class = CustomPagination

    def get_queryset(self):
        return LabTest.objects()

    def retrieve(self, request, *args, **kwargs):
        lab_test = LabTest.objects(pk=kwargs['pk']).first()
        if not lab_test:
            return Response(
                {'error': 'Lab test not found'},
                status=status.HTTP_404_NOT_FOUND
            )
        serializer = self.get_serializer(lab_test)
        return Response(serializer.data)

    @action(detail=False, methods=['get'])
    def by_patient(self, request):
        """Get lab tests for a specific patient"""
        patient_id = request.query_params.get('patient_id')
        if not patient_id:
            return Response(
                {'error': 'patient_id is required'},
                status=status.HTTP_400_BAD_REQUEST
            )
        tests = LabTest.objects(patient__pk=patient_id)
        serializer = self.get_serializer(tests, many=True)
        return Response(serializer.data)


class BillingViewSet(viewsets.ModelViewSet):
    """
    ViewSet for Billing operations
    """
    serializer_class = BillingSerializer
    pagination_class = CustomPagination

    def get_queryset(self):
        return Billing.objects()

    def retrieve(self, request, *args, **kwargs):
        billing = Billing.objects(pk=kwargs['pk']).first()
        if not billing:
            return Response(
                {'error': 'Billing record not found'},
                status=status.HTTP_404_NOT_FOUND
            )
        serializer = self.get_serializer(billing)
        return Response(serializer.data)

    @action(detail=False, methods=['get'])
    def by_patient(self, request):
        """Get billing records for a specific patient"""
        patient_id = request.query_params.get('patient_id')
        if not patient_id:
            return Response(
                {'error': 'patient_id is required'},
                status=status.HTTP_400_BAD_REQUEST
            )
        bills = Billing.objects(patient__pk=patient_id)
        serializer = self.get_serializer(bills, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=['post'])
    def mark_as_paid(self, request, pk=None):
        """Mark a billing record as paid"""
        billing = Billing.objects(pk=pk).first()
        if not billing:
            return Response(
                {'error': 'Billing record not found'},
                status=status.HTTP_404_NOT_FOUND
            )
        billing.payment_status = 'Paid'
        billing.save()
        serializer = self.get_serializer(billing)
        return Response(serializer.data)


class PharmacyViewSet(viewsets.ModelViewSet):
    """
    ViewSet for Pharmacy operations
    """
    serializer_class = PharmacySerializer
    pagination_class = CustomPagination
    filter_backends = [filters.SearchFilter]
    search_fields = ['medicine_name', 'medicine_code']

    def get_queryset(self):
        return Pharmacy.objects(is_active=True)

    def retrieve(self, request, *args, **kwargs):
        pharmacy = Pharmacy.objects(pk=kwargs['pk']).first()
        if not pharmacy:
            return Response(
                {'error': 'Medicine not found'},
                status=status.HTTP_404_NOT_FOUND
            )
        serializer = self.get_serializer(pharmacy)
        return Response(serializer.data)


class MedicalHistoryViewSet(viewsets.ModelViewSet):
    """
    ViewSet for Medical History operations
    """
    serializer_class = MedicalHistorySerializer
    pagination_class = CustomPagination

    def get_queryset(self):
        return MedicalHistory.objects()

    def retrieve(self, request, *args, **kwargs):
        history = MedicalHistory.objects(pk=kwargs['pk']).first()
        if not history:
            return Response(
                {'error': 'Medical history not found'},
                status=status.HTTP_404_NOT_FOUND
            )
        serializer = self.get_serializer(history)
        return Response(serializer.data)
