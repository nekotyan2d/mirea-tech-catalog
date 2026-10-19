from django.shortcuts import render

from homepage.views import load_data
from models.order import find_order_by_id


def order_list(request):
    _, _, orders = load_data()
    return render(request, "orders/order_list.html", {"orders": orders})


def order_detail(request, order_id):
    _, _, orders = load_data()
    order = find_order_by_id(orders, order_id)
    return render(
        request,
        "orders/order_detail.html",
        {"order": order},
        status=404 if order is None else 200,
    )
