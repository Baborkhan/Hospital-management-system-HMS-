from django.contrib import admin
from .models import Medicine, PharmacyOrder, PharmacyOrderItem

@admin.register(Medicine)
class MedicineAdmin(admin.ModelAdmin):
    list_display = ("name", "generic_name", "company", "medicine_type",
                    "category", "price", "stock_quantity", "is_active")
    list_filter = ("medicine_type", "category", "is_active")
    search_fields = ("name", "generic_name", "company")
    list_editable = ("price", "stock_quantity", "is_active")

class OrderItemInline(admin.TabularInline):
    model = PharmacyOrderItem
    extra = 0

@admin.register(PharmacyOrder)
class PharmacyOrderAdmin(admin.ModelAdmin):
    list_display = ("ref_id", "patient_name", "patient_phone", "status",
                    "total", "payment_method", "created_at")
    list_filter = ("status", "payment_method")
    search_fields = ("ref_id", "patient_name", "patient_phone")
    inlines = [OrderItemInline]
    list_editable = ("status",)
