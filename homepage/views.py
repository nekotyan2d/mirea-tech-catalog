from django.conf import settings
from django.http import HttpResponse
from django.templatetags.static import static
from django.utils.html import escape

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


def page(title, content, status=200):
    html = f"""<!DOCTYPE html>
<html lang="ru">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <title>{escape(title)}</title>
    <link rel="stylesheet" href="{static("css/style.css")}">
</head>
<body>
    <header>
        <nav class="nav">
            <a class="nav__link logo" href="/">
                <svg width="256" height="256" viewBox="0 0 256 256" fill="none" xmlns="http://www.w3.org/2000/svg">
                <path d="M182 58H74C74 168.733 146.581 197 182 197" stroke="#C6AB55" stroke-width="24"/>
                </svg>
            </a>
            <a class="nav__link" href="/products/">Товары</a>
            <a class="nav__link" href="/orders/">Заказы</a>
        </nav>
    </header>
    
    <main class="container">{content}</main>
</body>
</html>"""
    return HttpResponse(html, status=status)


def not_found(what, back_url, back_text):
    content = f"""
    <h1 class="error">{what} не найден</h1>
    <a href="{back_url}" class="btn">← {back_text}</a>
    """
    return page(f"{what} не найден", content, status=404)

def page_not_found(request, exception=None):
    content = f"""
    <h1>Страница не найдена</h1>
    <a class="btn" href="/">На главную</a>
    """
    return page(f"Страница не найдена", content, status=404)

def index(request):
    content = """
    <h1 class="hero__title">TechCat</h1>
    <p class="hero__lead">Учет товаров на складе и заказов.</p>
    <p>Основные разделы:</p>
    <a href="/products/" class="btn btn--primary">Товары</a>
    <a href="/orders/" class="btn">Заказы</a>
    """
    return page("Каталог техники", content)
