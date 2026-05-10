from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Invoice, InvoiceItem
from .serializers import InvoiceSerializer

class InvoiceListView(APIView):
    def get(self, request):
        qs = Invoice.objects.prefetch_related("items").all()
        hospital = request.query_params.get("hospital")
        status_f = request.query_params.get("status")
        invoice_type = request.query_params.get("type")
        if hospital:
            qs = qs.filter(hospital_id=hospital)
        if status_f:
            qs = qs.filter(status=status_f)
        if invoice_type:
            qs = qs.filter(invoice_type=invoice_type)
        return Response({"success": True, "data": InvoiceSerializer(qs[:100], many=True).data, "total": qs.count()})

    def post(self, request):
        items_data = request.data.pop("items", [])
        subtotal = sum(float(i.get("unit_price", 0)) * int(i.get("quantity", 1)) for i in items_data)
        discount = float(request.data.get("discount", 0))
        total = subtotal - discount
        invoice = Invoice.objects.create(
            patient_name=request.data.get("patient_name",""),
            patient_phone=request.data.get("patient_phone",""),
            patient_age=request.data.get("patient_age"),
            patient_gender=request.data.get("patient_gender",""),
            invoice_type=request.data.get("invoice_type","opd"),
            payment_method=request.data.get("payment_method","cash"),
            hospital_id=request.data.get("hospital"),
            doctor_id=request.data.get("doctor"),
            subtotal=subtotal, discount=discount, total=total,
        )
        for item in items_data:
            qty = int(item.get("quantity", 1))
            price = float(item.get("unit_price", 0))
            InvoiceItem.objects.create(
                invoice=invoice,
                description=item.get("description",""),
                quantity=qty,
                unit_price=price,
                total=qty * price,
            )
        return Response({"success": True, "data": InvoiceSerializer(invoice).data,
                         "invoice_number": invoice.invoice_number}, status=201)

class InvoiceDetailView(APIView):
    def get(self, request, pk):
        try:
            inv = Invoice.objects.prefetch_related("items").get(pk=pk)
            return Response({"success": True, "data": InvoiceSerializer(inv).data})
        except Invoice.DoesNotExist:
            return Response({"success": False, "message": "Not found"}, status=404)

    def patch(self, request, pk):
        try:
            inv = Invoice.objects.get(pk=pk)
            if "status" in request.data:
                inv.status = request.data["status"]
            if "payment_method" in request.data:
                inv.payment_method = request.data["payment_method"]
            inv.save()
            return Response({"success": True, "data": InvoiceSerializer(inv).data})
        except Invoice.DoesNotExist:
            return Response({"success": False, "message": "Not found"}, status=404)
