import json
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
from django.forms.models import model_to_dict
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import Appointment, Admission, Bill, Doctor, Patient


def parse_body(request):
    try:
        return json.loads(request.body.decode('utf-8') or '{}')
    except json.JSONDecodeError:
        return {}


def serialize_instance(instance, extra=None):
    data = model_to_dict(instance)
    if extra:
        data.update(extra)
    return data


def handle_list(model, request, allowed_fields=None):
    if request.method == 'GET':
        items = [serialize_instance(item) for item in model.objects.all()]
        return JsonResponse({'results': items}, status=200)

    if request.method == 'POST':
        payload = parse_body(request)
        if allowed_fields is not None:
            payload = {key: payload[key] for key in payload if key in allowed_fields}
        instance = model.objects.create(**payload)
        return JsonResponse(serialize_instance(instance), status=201)

    return JsonResponse({'error': 'Method not allowed'}, status=405)


def handle_detail(model, request, pk, allowed_fields=None):
    try:
        instance = model.objects.get(pk=pk)
    except ObjectDoesNotExist:
        return JsonResponse({'error': 'Not found'}, status=404)

    if request.method == 'GET':
        return JsonResponse(serialize_instance(instance), status=200)

    if request.method in ('PUT', 'PATCH'):
        payload = parse_body(request)
        for key, value in payload.items():
            if allowed_fields is None or key in allowed_fields:
                setattr(instance, key, value)
        instance.save()
        return JsonResponse(serialize_instance(instance), status=200)

    if request.method == 'DELETE':
        instance.delete()
        return JsonResponse({'deleted': True}, status=204)

    return JsonResponse({'error': 'Method not allowed'}, status=405)


@csrf_exempt
def register_user(request):
    if request.method != 'POST':
        return JsonResponse({'error': 'Method not allowed'}, status=405)

    data = parse_body(request)
    username = data.get('username')
    password = data.get('password')
    email = data.get('email', '')

    if not username or not password:
        return JsonResponse({'error': 'username and password are required'}, status=400)

    if User.objects.filter(username=username).exists():
        return JsonResponse({'error': 'Username already exists'}, status=400)

    user = User.objects.create_user(username=username, email=email, password=password)
    return JsonResponse({'id': user.id, 'username': user.username}, status=201)


@csrf_exempt
def login_user(request):
    if request.method != 'POST':
        return JsonResponse({'error': 'Method not allowed'}, status=405)

    data = parse_body(request)
    username = data.get('username')
    password = data.get('password')
    user = authenticate(request, username=username, password=password)
    if user is None:
        return JsonResponse({'error': 'Invalid credentials'}, status=401)

    login(request, user)
    return JsonResponse({'id': user.id, 'username': user.username}, status=200)


@csrf_exempt
def logout_user(request):
    if request.method != 'POST':
        return JsonResponse({'error': 'Method not allowed'}, status=405)

    logout(request)
    return JsonResponse({'logged_out': True}, status=200)


@csrf_exempt
def patient_list(request):
    return handle_list(Patient, request, allowed_fields=[
        'first_name', 'last_name', 'date_of_birth', 'gender', 'phone', 'email', 'address', 'medical_history'
    ])


@csrf_exempt
def patient_detail(request, pk):
    return handle_detail(Patient, request, pk, allowed_fields=[
        'first_name', 'last_name', 'date_of_birth', 'gender', 'phone', 'email', 'address', 'medical_history'
    ])


@csrf_exempt
def doctor_list(request):
    return handle_list(Doctor, request, allowed_fields=['name', 'specialization', 'email', 'phone', 'available'])


@csrf_exempt
def doctor_detail(request, pk):
    return handle_detail(Doctor, request, pk, allowed_fields=['name', 'specialization', 'email', 'phone', 'available'])


@csrf_exempt
def appointment_list(request):
    return handle_list(Appointment, request, allowed_fields=['patient', 'doctor', 'appointment_date', 'reason', 'status'])


@csrf_exempt
def appointment_detail(request, pk):
    return handle_detail(Appointment, request, pk, allowed_fields=['patient', 'doctor', 'appointment_date', 'reason', 'status'])


@csrf_exempt
def admission_list(request):
    return handle_list(Admission, request, allowed_fields=['patient', 'admitted_at', 'discharged_at', 'ward', 'notes'])


@csrf_exempt
def admission_detail(request, pk):
    return handle_detail(Admission, request, pk, allowed_fields=['patient', 'admitted_at', 'discharged_at', 'ward', 'notes'])


@csrf_exempt
def bill_list(request):
    return handle_list(Bill, request, allowed_fields=['patient', 'amount', 'description', 'paid'])


@csrf_exempt
def bill_detail(request, pk):
    return handle_detail(Bill, request, pk, allowed_fields=['patient', 'amount', 'description', 'paid'])
