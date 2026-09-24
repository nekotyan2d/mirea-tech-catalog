import pytest

from models import Category, Manufacturer, Product
from models.product import (
    add_product,
    filter_products_by_category,
    filter_products_by_price,
    find_product,
    get_catalog_statistics,
    sort_products,
)

LAPTOPS = Category(1, "Ноутбуки")
PERIPHERY = Category(3, "Периферия")
HP = Manufacturer(1, "HP", "США")


def make_products():
    products = []
    add_product(products, "Мышь", PERIPHERY, HP, 2000, 20)
    add_product(products, "Ноутбук ProBook", LAPTOPS, HP, 60000, 3)
    return products


def test_product_holds_objects():
    product = Product(1, "Ноутбук", LAPTOPS, HP, 60000, 3)
    assert product.category is LAPTOPS
    assert product.manufacturer is HP
    assert "Ноутбук" in str(product)


def test_add_product():
    products = []
    product = add_product(products, "Ноутбук", LAPTOPS, HP, 60000, 3)
    assert products == [product] and product.id == 1


def test_find_product():
    assert find_product(make_products(), "probook")


def test_is_in_stock():
    product = Product(1, "Монитор", LAPTOPS, HP, 30000, 10)
    assert product.is_in_stock(5)
    assert not product.is_in_stock(11)


def test_reduce_and_increase_quantity():
    product = Product(1, "Монитор", LAPTOPS, HP, 30000, 10)
    product.reduce_quantity(4)
    assert product.quantity == 6
    product.increase_quantity(2)
    assert product.quantity == 8
    with pytest.raises(ValueError):
        product.reduce_quantity(9)


def test_validate_price():
    assert Product.validate_price(0)
    assert not Product.validate_price(-1)


def test_filter_products_by_category():
    result = filter_products_by_category(make_products(), category_id=3)
    assert len(result) == 1 and result[0].name == "Мышь"


def test_filter_products_by_price():
    result = filter_products_by_price(make_products(), 1000, 5000)
    assert [p.name for p in result] == ["Мышь"]


def test_sort_products():
    assert [p.price for p in sort_products(make_products())] == [2000, 60000]
    assert [p.name for p in sort_products(make_products(), "name")] == [
        "Мышь", "Ноутбук ProBook"
    ]


def test_catalog_statistics():
    stats = get_catalog_statistics(make_products())
    assert stats["total_items"] == 23
    assert get_catalog_statistics([])["total_items"] == 0
