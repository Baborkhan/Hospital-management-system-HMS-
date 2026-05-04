from rest_framework.views import APIView
from rest_framework.response import Response
from .models import LoyaltyTransaction
from .serializers import LoyaltyTransactionSerializer

def get_user(request):
    auth = request.headers.get("Authorization","")
    if not auth.startswith("Bearer "): return None
    try:
        from apps.accounts.models import User
        uid = int(auth.replace("Bearer ","").split("_")[2])
        return User.objects.get(id=uid, is_active=True)
    except: return None

class LoyaltyView(APIView):
    def get(self, request):
        user = get_user(request)
        if not user: return Response({"success":False,"message":"Unauthorized"},status=401)
        txns = LoyaltyTransaction.objects.filter(user=user)
        return Response({
            "success":True,
            "balance": user.loyalty_points,
            "data":LoyaltyTransactionSerializer(txns,many=True).data
        })
