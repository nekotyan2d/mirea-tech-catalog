from django.http import HttpRequest

from .models import Product


def catalog_context(request: HttpRequest) -> dict[str, object]:
    products_count = Product.objects.count()
    return {
        "site_name": "Tech Catalog",
        "products_count": products_count,
    }
