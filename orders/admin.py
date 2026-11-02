from django.contrib import admin

from .models import Order


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ("id", "product", "quantity", "is_cancelled")
    list_filter = ("is_cancelled",)
    search_fields = ("product__name",)
