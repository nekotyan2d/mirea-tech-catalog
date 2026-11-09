from django.contrib import admin
from django.db.models import Count, Q
from django.utils.html import format_html

from orders.models import Order
from .models import Category, Manufacturer, Product


class OrderInline(admin.TabularInline):
    model = Order
    fields = ("id", "quantity", "status")
    readonly_fields = ("id",)
    extra = 0
    can_delete = False


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "products_count")
    list_display_links = ("name",)
    search_fields = ("name",)
    ordering = ("name",)
    list_per_page = 20
    readonly_fields = ("id",)

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return qs.annotate(products_count=Count("products"))

    @admin.display(description="Количество товаров", ordering="products_count")
    def products_count(self, obj: Category) -> int:
        return getattr(obj, "products_count", 0)


@admin.register(Manufacturer)
class ManufacturerAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "country", "products_count")
    list_display_links = ("name",)
    search_fields = ("name", "country")
    list_filter = ("country",)
    ordering = ("name",)
    list_per_page = 20
    readonly_fields = ("id",)

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return qs.annotate(products_count=Count("products"))

    @admin.display(description="Количество товаров", ordering="products_count")
    def products_count(self, obj: Manufacturer) -> int:
        return getattr(obj, "products_count", 0)


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "name",
        "category",
        "manufacturer",
        "price",
        "quantity",
        "is_large",
        "active_orders_count",
        "site_link",
    )
    list_display_links = ("name",)
    list_editable = ("quantity",)
    search_fields = ("name", "category__name", "manufacturer__name")
    list_filter = ("category", "manufacturer", "is_large")
    ordering = ("name",)
    list_per_page = 20
    readonly_fields = ("id", "slug", "is_large")
    inlines = (OrderInline,)
    view_on_site = True
    list_select_related = ("category", "manufacturer")

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return qs.annotate(
            active_orders_count=Count(
                "orders",
                filter=Q(orders__status=Order.Status.ACTIVE),
            )
        )

    @admin.display(description="Активных заказов", ordering="active_orders_count")
    def active_orders_count(self, obj: Product) -> int:
        return getattr(obj, "active_orders_count", 0)

    @admin.display(description="Страница на сайте")
    def site_link(self, obj: Product) -> str:
        return format_html(
            '<a href="{}" target="_blank">Открыть</a>',
            obj.get_absolute_url(),
        )
