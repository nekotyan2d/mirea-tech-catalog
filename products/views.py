from django.shortcuts import render

from homepage.views import load_data
from models.order import is_product_available
from models.product import (
    filter_products_by_category,
    find_product_by_id,
    sort_products,
)


def product_list(request):
    categories, products, _ = load_data()

    category_id = request.GET.get("category", "")
    if category_id.isdigit():
        products = filter_products_by_category(products, int(category_id))
    sort = "name" if request.GET.get("sort") == "name" else "price"
    products = sort_products(products, sort)

    context = {
        "categories": categories,
        "products": products,
        "category_id": category_id,
        "sort": sort,
    }
    return render(request, "products/product_list.html", context)


def product_detail(request, product_id):
    _, products, _ = load_data()
    product = find_product_by_id(products, product_id)

    context = {
        "product": product,
        "in_stock": product is not None and is_product_available(product, 1),
    }
    return render(
        request,
        "products/product_detail.html",
        context,
        status=404 if product is None else 200,
    )
