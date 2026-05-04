from rest_framework.views import APIView
from rest_framework.response import Response
from .models import LabTest, LabBooking
from .serializers import LabTestSerializer, LabBookingSerializer

class LabTestListView(APIView):
    def get(self, request):
        qs = LabTest.objects.filter(is_active=True)
        q = request.query_params.get("q")
        category = request.query_params.get("category")
        hospital = request.query_params.get("hospital")
        home_collection = request.query_params.get("home_collection")
        if q:
            qs = qs.filter(name__icontains=q) | qs.filter(category__icontains=q)
        if category:
            qs = qs.filter(category__icontains=category)
        if hospital:
            qs = qs.filter(hospital_id=hospital)
        if home_collection == "true":
            qs = qs.filter(is_home_collection=True)
        return Response({"success": True, "data": LabTestSerializer(qs, many=True).data, "total": qs.count()})

class LabBookingView(APIView):
    def get(self, request):
        qs = LabBooking.objects.select_related("test").all().order_by("-created_at")
        return Response({"success": True, "data": LabBookingSerializer(qs, many=True).data})

    def post(self, request):
        try:
            test = LabTest.objects.get(pk=request.data.get("test"))
        except LabTest.DoesNotExist:
            return Response({"success": False, "message": "Test not found"}, status=404)
        booking = LabBooking.objects.create(
            test=test,
            patient_name=request.data.get("patient_name", ""),
            patient_phone=request.data.get("patient_phone", ""),
            booking_date=request.data.get("booking_date"),
            is_home_collection=request.data.get("is_home_collection", False),
            address=request.data.get("address", ""),
        )
        return Response({"success": True, "data": LabBookingSerializer(booking).data,
                         "ref_id": booking.ref_id}, status=201)

class LabBookingDetailView(APIView):
    def patch(self, request, pk):
        try:
            booking = LabBooking.objects.get(pk=pk)
            if "status" in request.data:
                booking.status = request.data["status"]
            booking.save()
            return Response({"success": True, "data": LabBookingSerializer(booking).data})
        except LabBooking.DoesNotExist:
            return Response({"success": False, "message": "Not found"}, status=404)
