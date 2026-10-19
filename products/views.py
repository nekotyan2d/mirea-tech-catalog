from django.shortcuts import render

from db.queries import fetch_all, fetch_one


def product_list(request):
    category_id = request.GET.get("category", "")
    category = int(category_id) if category_id.isdigit() else None
    sort = "name" if request.GET.get("sort") == "name" else "price"

    context = {
        "categories": fetch_all("category_list"),
        "products": fetch_all("product_list", (category, category, sort)),
        "category_id": category_id,
        "sort": sort,
    }
    return render(request, "products/product_list.html", context)


def product_detail(request, product_id):
    product = fetch_one("product_by_id", (product_id,))
    return render(
        request,
        "products/product_detail.html",
        {"product": product},
        status=404 if product is None else 200,
    )


def _number(value):
    try:
        return float(value)
    except (TypeError, ValueError):
        return None


def product_search(request):
    query = request.GET.get("q", "").strip()
    min_price = _number(request.GET.get("min_price"))
    max_price = _number(request.GET.get("max_price"))
    searched = any(key in request.GET for key in ("q", "min_price", "max_price"))

    context = {
        "searched": searched,
        "products": (
            fetch_all("products_search", (query, min_price, min_price, max_price, max_price))
            if searched
            else []
        ),
        "q": query,
        "min_price": request.GET.get("min_price", ""),
        "max_price": request.GET.get("max_price", ""),
    }
    return render(request, "products/product_search.html", context)


def statistics(request):
    context = {
        "summary": fetch_one("stock_summary"),
        "categories": fetch_all("category_stats"),
    }
    return render(request, "products/statistics.html", context)
