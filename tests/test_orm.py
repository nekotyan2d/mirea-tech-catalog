# pyright: reportAttributeAccessIssue=false, reportGeneralTypeIssues=false
import os
import django
import pytest

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "catalog.settings")
django.setup()

from django.test import Client  # noqa: E402
from orders.models import Order  # noqa: E402
from products.models import Category, Manufacturer, Product  # noqa: E402


@pytest.fixture(autouse=True)
def setup_data() -> None:
    from db.import_sqlite_to_orm import import_data
    import_data()


def test_category_and_manufacturer_models() -> None:
    cat = Category.objects.get(name="Ноутбуки")
    assert str(cat) == "Ноутбуки"
    assert cat.products.count() >= 1

    man = Manufacturer.objects.get(name="HP")
    assert "HP" in str(man)
    assert man.country == "США"


def test_product_model_methods_and_properties() -> None:
    product = Product.objects.get(name="Ноутбук ProBook 450")
    assert product.is_in_stock(1)
    assert product.in_stock
    assert product.category_name == "Ноутбуки"
    assert product.manufacturer_name == "HP"
    assert product.manufacturer_country == "США"
    assert "Ноутбук ProBook 450" in str(product)

    initial_qty = product.quantity
    product.increase_quantity(5)
    product.refresh_from_db()
    assert product.quantity == initial_qty + 5

    product.reduce_quantity(5)
    product.refresh_from_db()
    assert product.quantity == initial_qty

    with pytest.raises(ValueError):
        product.reduce_quantity(9999)


def test_order_model_methods() -> None:
    product = Product.objects.get(name="Монитор UltraSharp 27")
    initial_stock = product.quantity
    order = Order.objects.create(product=product, quantity=2, is_cancelled=False)

    assert not order.is_cancelled
    assert order.total == product.price * 2
    assert order.product_name == product.name
    assert "Заказ №" in str(order)

    order.cancel()
    order.refresh_from_db()
    product.refresh_from_db()

    assert order.is_cancelled
    assert product.quantity == initial_stock + 2

    order.cancel()
    product.refresh_from_db()
    assert product.quantity == initial_stock + 2

    order.delete()


def test_views_products() -> None:
    client = Client()

    resp = client.get("/products/")
    assert resp.status_code == 200
    assert "Товары" in resp.content.decode("utf-8")

    resp_filtered = client.get("/products/?category=1&sort=name")
    assert resp_filtered.status_code == 200

    resp_detail = client.get("/products/1/")
    assert resp_detail.status_code == 200
    assert "Ноутбук ProBook 450" in resp_detail.content.decode("utf-8")

    resp_404 = client.get("/products/99999/")
    assert resp_404.status_code == 404

    resp_search = client.get("/products/search/?q=keys&min_price=1000")
    assert resp_search.status_code == 200
    assert "MX Keys" in resp_search.content.decode("utf-8")

    resp_stats = client.get("/products/statistics/")
    assert resp_stats.status_code == 200
    assert "Статистика склада" in resp_stats.content.decode("utf-8")


def test_views_orders() -> None:
    client = Client()

    resp = client.get("/orders/")
    assert resp.status_code == 200
    assert "Заказы" in resp.content.decode("utf-8")

    resp_active = client.get("/orders/?status=active&sort=product")
    assert resp_active.status_code == 200

    resp_cancelled = client.get("/orders/?status=cancelled")
    assert resp_cancelled.status_code == 200

    resp_detail = client.get("/orders/1/")
    assert resp_detail.status_code == 200
    assert "Заказ №1" in resp_detail.content.decode("utf-8")

    resp_404 = client.get("/orders/99999/")
    assert resp_404.status_code == 404

    resp_stats = client.get("/orders/statistics/")
    assert resp_stats.status_code == 200
    assert "Статистика заказов" in resp_stats.content.decode("utf-8")
