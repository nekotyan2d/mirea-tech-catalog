from django.utils.html import escape

from homepage.views import load_data, not_found, page
from models.order import is_product_available
from models.product import (
    filter_products_by_category,
    find_product_by_id,
    sort_products,
)


def _option(value, label, selected):
    mark = " selected" if selected else ""
    return f'<option value="{value}"{mark}>{escape(label)}</option>'


def product_list(request):
    categories, products, _ = load_data()

    category_id = request.GET.get("category", "")
    if category_id.isdigit():
        products = filter_products_by_category(products, int(category_id))
    sort = "name" if request.GET.get("sort") == "name" else "price"
    products = sort_products(products, sort)

    category_options = _option("", "Все категории", category_id == "") + "".join(
        _option(c.id, c.name, str(c.id) == category_id) for c in categories
    )
    sort_options = _option("price", "По цене", sort == "price") + _option(
        "name", "По названию", sort == "name"
    )
    items = "".join(
        '<li class="list__item">'
        f'<a href="/products/{p.id}/">{escape(p.name)}</a>'
        f'<span class="price">{p.price} руб.</span></li>'
        for p in products
    )
    content = f"""
    <h1>Товары</h1>
    <form method="get" class="filters">
        <select name="category" class="select">{category_options}</select>
        <select name="sort" class="select">{sort_options}</select>
        <button class="btn btn--primary">Применить</button>
    </form>
    <ul class="list">{items}</ul>
    """
    return page("Каталог – товары", content)


def product_detail(request, product_id):
    _, products, _ = load_data()
    product = find_product_by_id(products, product_id)
    if product is None:
        return not_found("Товар", "/products/", "к списку товаров")

    in_stock = is_product_available(product, 1)
    badge = "badge--ok" if in_stock else "badge--bad"
    status = "в наличии" if in_stock else "нет в наличии"
    content = f"""
    <div class="card">
        <h2 class="card__title">{escape(product.name)}</h2>
        <p><strong>Категория:</strong> {escape(product.category.name)}</p>
        <p>
            <strong>Производитель:</strong>
            {escape(product.manufacturer.name)} ({escape(product.manufacturer.country)})
        </p>
        <p><strong>Цена:</strong> {product.price} руб.</p>
        <p><strong>На складе:</strong> {product.quantity} шт.</p>
        <p>Наличие: <span class="badge {badge}">{status}</span></p>
        <a href="/products/" class="btn">к списку товаров</a>
    </div>
    """
    return page(product.name, content)
