from django.contrib import admin
from .models import Invoice, InvoiceItem

class InvoiceItemInline(admin.TabularInline):
    model = InvoiceItem
    extra = 0

@admin.register(Invoice)
class InvoiceAdmin(admin.ModelAdmin):
    list_display = ("invoice_number", "patient_name", "invoice_type",
                    "status", "total", "payment_method", "visit_date")
    list_filter = ("invoice_type", "status", "payment_method")
    search_fields = ("invoice_number", "patient_name")
    inlines = [InvoiceItemInline]
    list_editable = ("status",)
