from django.contrib import admin, messages

from .models import Order


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "product",
        "product_price",
        "quantity",
        "total_price",
        "status",
    )
    list_display_links = ("id",)
    search_fields = (
        "product__name",
        "product__category__name",
        "product__manufacturer__name",
    )
    list_filter = (
        "status",
        "product__category",
    )
    ordering = ("-id",)
    list_per_page = 20
    readonly_fields = ("id", "total_price")
    list_select_related = ("product", "product__category", "product__manufacturer")
    autocomplete_fields = ("product",)
    actions = ("cancel_orders", "restore_orders")

    @admin.display(description="Цена товара", ordering="product__price")
    def product_price(self, obj: Order) -> str:
        return f"{obj.product.price} руб."

    @admin.display(description="Сумма заказа")
    def total_price(self, obj: Order) -> str:
        return f"{obj.total} руб."

    @admin.action(description="Отменить выбранные заказы")
    def cancel_orders(self, request, queryset):
        count = 0
        for order in queryset:
            order.cancel()
            count += 1
        self.message_user(
            request,
            f"Отменено заказов: {count}.",
            messages.SUCCESS,
        )

    @admin.action(description="Вернуть в активные")
    def restore_orders(self, request, queryset):
        count = 0
        for order in queryset:
            if order.status != Order.Status.ACTIVE:
                order.status = Order.Status.ACTIVE
                order.save(update_fields=["status"])
                count += 1
        self.message_user(
            request,
            f"Возвращено заказов: {count}.",
            messages.SUCCESS,
        )
