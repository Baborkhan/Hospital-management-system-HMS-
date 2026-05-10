from rest_framework.views import APIView
from rest_framework.response import Response
from django.db.models import Avg
from .models import Review
from .serializers import ReviewSerializer

class ReviewListView(APIView):
    def get(self, request):
        qs = Review.objects.select_related("patient__user").filter(is_approved=True)
        doctor = request.query_params.get("doctor")
        hospital = request.query_params.get("hospital")
        review_type = request.query_params.get("type")
        if doctor:
            qs = qs.filter(doctor_id=doctor, review_type="doctor")
        if hospital:
            qs = qs.filter(hospital_id=hospital, review_type="hospital")
        if review_type:
            qs = qs.filter(review_type=review_type)
        avg = qs.aggregate(avg_rating=Avg("rating"))
        return Response({
            "success": True,
            "data": ReviewSerializer(qs[:50], many=True).data,
            "total": qs.count(),
            "avg_rating": round(float(avg["avg_rating"] or 0), 1),
        })

    def post(self, request):
        data = request.data.copy()
        # Validate: patient must not have reviewed same target twice
        doctor_id = data.get("doctor")
        hospital_id = data.get("hospital")
        patient_id = data.get("patient")
        if doctor_id and Review.objects.filter(patient_id=patient_id, doctor_id=doctor_id).exists():
            return Response({"success": False, "message": "Already reviewed this doctor"}, status=400)
        if hospital_id and Review.objects.filter(patient_id=patient_id, hospital_id=hospital_id).exists():
            return Response({"success": False, "message": "Already reviewed this hospital"}, status=400)
        ser = ReviewSerializer(data=data)
        if ser.is_valid():
            review = ser.save()
            # Update doctor/hospital avg rating
            if review.doctor:
                avg = Review.objects.filter(doctor=review.doctor).aggregate(a=Avg("rating"))["a"]
                review.doctor.rating = round(avg, 1)
                review.doctor.rating_count = Review.objects.filter(doctor=review.doctor).count()
                review.doctor.save(update_fields=["rating", "rating_count"])
            if review.hospital:
                avg = Review.objects.filter(hospital=review.hospital).aggregate(a=Avg("rating"))["a"]
                review.hospital.rating = round(avg, 1)
                review.hospital.rating_count = Review.objects.filter(hospital=review.hospital).count()
                review.hospital.save(update_fields=["rating", "rating_count"])
            return Response({"success": True, "data": ReviewSerializer(review).data}, status=201)
        return Response({"success": False, "errors": ser.errors}, status=400)
