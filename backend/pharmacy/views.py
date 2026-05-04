from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Medicine, PharmacyOrder, PharmacyOrderItem
from .serializers import MedicineSerializer, PharmacyOrderSerializer


class MedicineListView(APIView):
    def get(self, request):
        qs = Medicine.objects.filter(is_active=True)
        q = request.query_params.get("q")
        category = request.query_params.get("category")
        med_type = request.query_params.get("type")
        max_price = request.query_params.get("max_price")
        in_stock = request.query_params.get("in_stock")
        if q:
            qs = qs.filter(name__icontains=q) | qs.filter(generic_name__icontains=q)
        if category:
            qs = qs.filter(category=category)
        if med_type:
            qs = qs.filter(medicine_type=med_type)
        if max_price:
            qs = qs.filter(price__lte=max_price)
        if in_stock == "true":
            qs = qs.filter(stock_quantity__gt=0)
        return Response({"success": True, "data": MedicineSerializer(qs, many=True).data, "total": qs.count()})


class PharmacyOrderView(APIView):
    def get(self, request):
        qs = PharmacyOrder.objects.prefetch_related("items__medicine").all()
        status_f = request.query_params.get("status")
        if status_f:
            qs = qs.filter(status=status_f)
        return Response({"success": True, "data": PharmacyOrderSerializer(qs, many=True).data})

    def post(self, request):
        items_data = request.data.pop("items", [])
        subtotal = 0
        for item in items_data:
            try:
                med = Medicine.objects.get(id=item["medicine_id"])
                subtotal += float(med.price) * int(item.get("quantity", 1))
            except Medicine.DoesNotExist:
                return Response({"success": False, "message": f"Medicine {item.get('medicine_id')} not found"}, status=400)
        delivery = 0 if subtotal >= 500 else 50
        discount = float(request.data.get("discount", 0))
        total = subtotal + delivery - discount
        order = PharmacyOrder.objects.create(
            patient_name=request.data.get("patient_name", "Guest"),
            patient_phone=request.data.get("patient_phone", ""),
            delivery_address=request.data.get("delivery_address", ""),
            payment_method=request.data.get("payment_method", "cash"),
            subtotal=subtotal, delivery_charge=delivery,
            discount=discount, total=total,
        )
        for item in items_data:
            med = Medicine.objects.get(id=item["medicine_id"])
            qty = int(item.get("quantity", 1))
            PharmacyOrderItem.objects.create(order=order, medicine=med, quantity=qty, unit_price=med.price)
            med.stock_quantity = max(0, med.stock_quantity - qty)
            med.save()
        return Response({"success": True, "data": PharmacyOrderSerializer(order).data, "ref_id": order.ref_id}, status=201)


class PharmacyOrderDetailView(APIView):
    def get(self, request, pk):
        try:
            order = PharmacyOrder.objects.prefetch_related("items__medicine").get(pk=pk)
            return Response({"success": True, "data": PharmacyOrderSerializer(order).data})
        except PharmacyOrder.DoesNotExist:
            return Response({"success": False, "message": "Not found"}, status=404)

    def patch(self, request, pk):
        try:
            order = PharmacyOrder.objects.get(pk=pk)
            if "status" in request.data:
                order.status = request.data["status"]
            order.save()
            return Response({"success": True, "data": PharmacyOrderSerializer(order).data})
        except PharmacyOrder.DoesNotExist:
            return Response({"success": False, "message": "Not found"}, status=404)
