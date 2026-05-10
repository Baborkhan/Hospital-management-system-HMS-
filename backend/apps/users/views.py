from rest_framework.views import APIView
from rest_framework.response import Response
from apps.accounts.models import User
from .serializers import UserProfileSerializer, UserUpdateSerializer

def get_user(request):
    auth = request.headers.get("Authorization","")
    if not auth.startswith("Bearer "): return None
    try:
        uid = int(auth.replace("Bearer ","").split("_")[2])
        return User.objects.get(id=uid, is_active=True)
    except: return None

class UserListView(APIView):
    def get(self, request):
        qs = User.objects.all()
        role = request.query_params.get("role")
        q = request.query_params.get("q")
        if role: qs = qs.filter(role=role)
        if q: qs = qs.filter(full_name__icontains=q) | qs.filter(email__icontains=q)
        page = int(request.query_params.get("page",1))
        limit = int(request.query_params.get("limit",20))
        total = qs.count()
        qs = qs[(page-1)*limit:page*limit]
        return Response({"success":True,"data":UserProfileSerializer(qs,many=True).data,"total":total,"page":page})

class UserDetailView(APIView):
    def get(self, request, pk):
        try:
            user = User.objects.get(pk=pk)
            return Response({"success":True,"data":UserProfileSerializer(user).data})
        except User.DoesNotExist:
            return Response({"success":False,"message":"User not found"},status=404)

    def put(self, request, pk):
        try:
            user = User.objects.get(pk=pk)
            ser = UserUpdateSerializer(user, data=request.data, partial=True)
            if ser.is_valid():
                ser.save()
                return Response({"success":True,"data":UserProfileSerializer(user).data})
            return Response({"success":False,"errors":ser.errors},status=400)
        except User.DoesNotExist:
            return Response({"success":False,"message":"Not found"},status=404)

    def delete(self, request, pk):
        try:
            user = User.objects.get(pk=pk)
            user.is_active = False
            user.save(update_fields=["is_active"])
            return Response({"success":True,"message":"User deactivated"})
        except User.DoesNotExist:
            return Response({"success":False,"message":"Not found"},status=404)
