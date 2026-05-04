import datetime
from rest_framework.views import APIView
from rest_framework.response import Response

class HealthCheckView(APIView):
    def get(self, request):
        return Response({"status":"ok","service":"MedFind API","version":"1.0.0",
                         "timestamp": datetime.datetime.now().isoformat()})
