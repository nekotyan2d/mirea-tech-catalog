from django.http import HttpRequest, HttpResponse
from django.shortcuts import render

from db.queries import fetch_all, fetch_one

STATUSES = {"active": 0, "cancelled": 1}
POPULAR_MIN_QUANTITY = 1


def order_list(request: HttpRequest) -> HttpResponse:
    status = request.GET.get("status", "")
    is_cancelled = STATUSES.get(status)

    context = {
        "orders": fetch_all("order_list", (is_cancelled, is_cancelled)),
        "status": status,
    }
    return render(request, "orders/order_list.html", context)


def order_detail(request: HttpRequest, order_id: int) -> HttpResponse:
    order = fetch_one("order_by_id", (order_id,))
    return render(
        request,
        "orders/order_detail.html",
        {"order": order},
        status=404 if order is None else 200,
    )


def statistics(request: HttpRequest) -> HttpResponse:
    context = {
        "active_count": fetch_all("active_orders_count")[0]["orders_count"],
        "products": fetch_all("product_orders_stats"),
        "popular": fetch_all("popular_products", (POPULAR_MIN_QUANTITY,)),
        "popular_min": POPULAR_MIN_QUANTITY,
    }
    return render(request, "orders/statistics.html", context)
