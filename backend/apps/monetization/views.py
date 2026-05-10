from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Subscription
from .serializers import SubscriptionSerializer

class SubscriptionListView(APIView):
    def get(self, request):
        qs = Subscription.objects.filter(is_active=True).select_related("hospital")
        hosp = request.query_params.get("hospital")
        if hosp: qs = qs.filter(hospital_id=hosp)
        return Response({"success":True,"data":SubscriptionSerializer(qs,many=True).data})

    def post(self, request):
        ser = SubscriptionSerializer(data=request.data)
        if ser.is_valid():
            ser.save()
            return Response({"success":True,"data":ser.data},status=201)
        return Response({"success":False,"errors":ser.errors},status=400)
