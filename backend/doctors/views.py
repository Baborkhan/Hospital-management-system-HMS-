from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Doctor
from .serializers import DoctorSerializer, DoctorListSerializer

class DoctorListView(APIView):
    def get(self, request):
        qs = Doctor.objects.select_related("user","hospital").all()
        specialty = request.query_params.get("specialty")
        division = request.query_params.get("division")
        hospital = request.query_params.get("hospital")
        q = request.query_params.get("q")
        available = request.query_params.get("available")
        video = request.query_params.get("video")
        if specialty:
            qs = qs.filter(specialty__icontains=specialty)
        if division:
            qs = qs.filter(hospital__division__icontains=division)
        if hospital:
            qs = qs.filter(hospital_id=hospital)
        if q:
            qs = qs.filter(user__full_name__icontains=q) | qs.filter(specialty__icontains=q)
        if available == "true":
            qs = qs.filter(is_available_today=True)
        if video == "true":
            qs = qs.filter(accepts_video_consult=True)
        return Response({"success": True, "data": DoctorListSerializer(qs, many=True).data, "total": qs.count()})

class DoctorDetailView(APIView):
    def get(self, request, pk):
        try:
            doc = Doctor.objects.select_related("user","hospital").get(pk=pk)
            return Response({"success": True, "data": DoctorSerializer(doc).data})
        except Doctor.DoesNotExist:
            return Response({"success": False, "message": "Not found"}, status=404)
