# pyright: reportAttributeAccessIssue=false, reportArgumentType=false
from django.core.paginator import Paginator
from django.db.models import Count, F, Q, Sum
from django.db.models.functions import Coalesce
from django.http import HttpRequest, HttpResponse
from django.shortcuts import get_object_or_404, render

from products.models import Product
from .models import Order

POPULAR_MIN_QUANTITY = 1


def order_list(request: HttpRequest) -> HttpResponse:
    status = str(request.GET.get("status", "")).strip()
    sort = str(request.GET.get("sort", "id")).strip()

    orders = Order.objects.select_related("product")

    if status == "active":
        orders = orders.active()
    elif status == "cancelled":
        orders = orders.cancelled()
    elif status == "completed":
        orders = orders.completed()

    sort_fields = {
        "id": "id",
        "product": "product__name",
    }
    sort_field = sort_fields.get(sort, "id")
    orders = orders.order_by(sort_field)

    paginator = Paginator(orders, 5)
    page_obj = paginator.get_page(request.GET.get("page"))

    context = {
        "orders": page_obj,
        "page_obj": page_obj,
        "status": status,
        "sort": sort,
    }
    return render(request, "orders/order_list.html", context)


def order_detail(request: HttpRequest, order_id: int) -> HttpResponse:
    order = get_object_or_404(
        Order.objects.select_related(
            "product",
            "product__category",
            "product__manufacturer",
        ),
        pk=order_id,
    )
    return render(
        request,
        "orders/order_detail.html",
        {"order": order},
    )


def statistics(request: HttpRequest) -> HttpResponse:
    stats = Order.objects.aggregate(
        total_orders=Count("id"),
        active_orders=Count("id", filter=Q(status=Order.Status.ACTIVE)),
        cancelled_orders=Count("id", filter=Q(status=Order.Status.CANCELLED)),
        completed_orders=Count("id", filter=Q(status=Order.Status.COMPLETED)),
    )
    active_count = stats["active_orders"]

    products = (
        Product.objects.annotate(
            product_name=F("name"),
            orders_count=Count(
                "orders",
                filter=Q(orders__status=Order.Status.ACTIVE),
            ),
            ordered_quantity=Coalesce(
                Sum(
                    "orders__quantity",
                    filter=Q(orders__status=Order.Status.ACTIVE),
                ),
                0,
            ),
        )
        .order_by("-ordered_quantity", "name")
    )

    popular = (
        Product.objects.filter(orders__status=Order.Status.ACTIVE)
        .annotate(
            product_name=F("name"),
            ordered_quantity=Sum("orders__quantity"),
        )
        .filter(ordered_quantity__gte=POPULAR_MIN_QUANTITY)
        .order_by("-ordered_quantity", "name")
    )

    context = {
        "stats": stats,
        "active_count": active_count,
        "products": products,
        "popular": popular,
        "popular_min": POPULAR_MIN_QUANTITY,
    }
    return render(request, "orders/statistics.html", context)
