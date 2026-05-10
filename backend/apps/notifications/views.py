from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Notification
from .serializers import NotificationSerializer

def get_user(request):
    auth = request.headers.get("Authorization","")
    if not auth.startswith("Bearer "): return None
    try:
        from apps.accounts.models import User
        uid = int(auth.replace("Bearer ","").split("_")[2])
        return User.objects.get(id=uid, is_active=True)
    except: return None

class NotificationListView(APIView):
    def get(self, request):
        user = get_user(request)
        if not user:
            return Response({"success":False,"message":"Unauthorized"},status=401)
        qs = Notification.objects.filter(user=user)
        unread_only = request.query_params.get("unread")
        if unread_only: qs = qs.filter(is_read=False)
        return Response({"success":True,"data":NotificationSerializer(qs,many=True).data,"unread_count":qs.filter(is_read=False).count()})

    def put(self, request):
        user = get_user(request)
        if not user: return Response({"success":False,"message":"Unauthorized"},status=401)
        notif_id = request.data.get("id")
        if notif_id:
            Notification.objects.filter(user=user, id=notif_id).update(is_read=True)
        else:
            Notification.objects.filter(user=user).update(is_read=True)
        return Response({"success":True,"message":"Marked as read"})
