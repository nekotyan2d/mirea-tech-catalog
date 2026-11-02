# pyright: reportAttributeAccessIssue=false, reportArgumentType=false
from decimal import Decimal
from django.core.paginator import Paginator
from django.db.models import Avg, Count, DecimalField, F, Max, Min, Q, Sum
from django.db.models.functions import Coalesce
from django.http import HttpRequest, HttpResponse
from django.shortcuts import get_object_or_404, render

from .models import Category, Product


def product_list(request: HttpRequest) -> HttpResponse:
    category_id = str(request.GET.get("category", "")).strip()
    category = None
    if category_id.isdigit():
        try:
            category = int(category_id)
        except ValueError:
            category = None
    sort = str(request.GET.get("sort", "price"))

    categories = Category.objects.all().order_by("name")
    products = Product.objects.select_related("category", "manufacturer")

    if category is not None:
        products = products.filter(category_id=category)

    sort_fields = {
        "price": "price",
        "name": "name",
    }
    sort_field = sort_fields.get(sort, "price")
    products = products.order_by(sort_field, "id")

    paginator = Paginator(products, 5)
    page_obj = paginator.get_page(request.GET.get("page"))

    context = {
        "categories": categories,
        "products": page_obj,
        "page_obj": page_obj,
        "category_id": category_id,
        "sort": sort,
    }
    return render(request, "products/product_list.html", context)


def product_detail(request: HttpRequest, product_id: int) -> HttpResponse:
    product = get_object_or_404(
        Product.objects.select_related("category", "manufacturer"),
        pk=product_id,
    )
    return render(
        request,
        "products/product_detail.html",
        {"product": product},
    )


def _number(value: object) -> float | None:
    if value is None:
        return None
    try:
        return float(str(value))
    except (TypeError, ValueError):
        return None


def product_search(request: HttpRequest) -> HttpResponse:
    query = str(request.GET.get("q", "")).strip()
    min_price = _number(request.GET.get("min_price"))
    max_price = _number(request.GET.get("max_price"))
    searched = any(key in request.GET for key in ("q", "min_price", "max_price"))

    if searched:
        products_qs = Product.objects.select_related("category", "manufacturer")
        if query:
            products_qs = products_qs.filter(
                Q(name__icontains=query) | Q(manufacturer__name__icontains=query)
            )
        if min_price is not None:
            products_qs = products_qs.filter(price__gte=Decimal(str(min_price)))
        if max_price is not None:
            products_qs = products_qs.filter(price__lte=Decimal(str(max_price)))
        products = products_qs.order_by("price", "id")
    else:
        products = []

    context = {
        "searched": searched,
        "products": products,
        "q": query,
        "min_price": request.GET.get("min_price", ""),
        "max_price": request.GET.get("max_price", ""),
    }
    return render(request, "products/product_search.html", context)


def statistics(request: HttpRequest) -> HttpResponse:
    summary = Product.objects.aggregate(
        products_count=Count("id"),
        total_quantity=Coalesce(Sum("quantity"), 0),
        total_value=Coalesce(
            Sum(F("price") * F("quantity"), output_field=DecimalField()),
            Decimal(0),
        ),
        avg_price=Avg("price"),
        min_price=Min("price"),
        max_price=Max("price"),
    )
    categories = (
        Category.objects.annotate(
            category_name=F("name"),
            products_count=Count("products"),
            total_quantity=Coalesce(Sum("products__quantity"), 0),
        )
        .order_by("-products_count", "name")
    )
    context = {
        "summary": summary,
        "categories": categories,
    }
    return render(request, "products/statistics.html", context)
