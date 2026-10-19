from django.conf import settings
from django.shortcuts import render

from storage import (
    load_categories,
    load_manufacturers,
    load_orders,
    load_products,
)


def load_data():
    data = settings.BASE_DIR / "data"
    categories = load_categories(str(data / "categories.json"))
    manufacturers = load_manufacturers(str(data / "manufacturers.json"))
    products = load_products(str(data / "products.json"), categories, manufacturers)
    orders = load_orders(str(data / "orders.json"), products)
    return categories, products, orders


def page_not_found(request, exception=None):
    return render(request, "404.html", status=404)


def index(request):
    return render(request, "homepage/index.html")
