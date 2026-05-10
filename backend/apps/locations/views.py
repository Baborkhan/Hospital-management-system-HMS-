from rest_framework.views import APIView
from rest_framework.response import Response

BANGLADESH_DIVISIONS = [
    {"name": "Dhaka", "slug": "dhaka", "lat": 23.8103, "lng": 90.4125, "districts": 13},
    {"name": "Chittagong", "slug": "chittagong", "lat": 22.3569, "lng": 91.7832, "districts": 11},
    {"name": "Rajshahi", "slug": "rajshahi", "lat": 24.3745, "lng": 88.6042, "districts": 8},
    {"name": "Sylhet", "slug": "sylhet", "lat": 24.8892, "lng": 91.8817, "districts": 4},
    {"name": "Khulna", "slug": "khulna", "lat": 22.8456, "lng": 89.5403, "districts": 10},
    {"name": "Barisal", "slug": "barisal", "lat": 22.7010, "lng": 90.3535, "districts": 6},
    {"name": "Rangpur", "slug": "rangpur", "lat": 25.7439, "lng": 89.2752, "districts": 8},
    {"name": "Mymensingh", "slug": "mymensingh", "lat": 24.7471, "lng": 90.4203, "districts": 4},
]

class DivisionListView(APIView):
    def get(self, request):
        return Response({"success": True, "data": BANGLADESH_DIVISIONS})
