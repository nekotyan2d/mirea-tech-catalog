from django.shortcuts import render

from db.queries import fetch_all, fetch_one

STATUSES = {"active": 0, "cancelled": 1}
POPULAR_MIN_QUANTITY = 1


def order_list(request):
    status = request.GET.get("status", "")
    is_cancelled = STATUSES.get(status)

    context = {
        "orders": fetch_all("order_list", (is_cancelled, is_cancelled)),
        "status": status,
    }
    return render(request, "orders/order_list.html", context)


def order_detail(request, order_id):
    order = fetch_one("order_by_id", (order_id,))
    return render(
        request,
        "orders/order_detail.html",
        {"order": order},
        status=404 if order is None else 200,
    )


def statistics(request):
    context = {
        "active_count": fetch_one("active_orders_count")["orders_count"],
        "products": fetch_all("product_orders_stats"),
        "popular": fetch_all("popular_products", (POPULAR_MIN_QUANTITY,)),
        "popular_min": POPULAR_MIN_QUANTITY,
    }
    return render(request, "orders/statistics.html", context)
