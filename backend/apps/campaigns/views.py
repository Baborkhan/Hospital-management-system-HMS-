from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Campaign
from .serializers import CampaignSerializer

class CampaignListView(APIView):
    def get(self, request):
        qs = Campaign.objects.filter(is_active=True).select_related("hospital")
        ctype = request.query_params.get("type")
        if ctype: qs = qs.filter(campaign_type=ctype)
        return Response({"success":True,"data":CampaignSerializer(qs,many=True).data})

    def post(self, request):
        ser = CampaignSerializer(data=request.data)
        if ser.is_valid():
            ser.save()
            return Response({"success":True,"data":ser.data},status=201)
        return Response({"success":False,"errors":ser.errors},status=400)
