from models import Category, Manufacturer, Order, Product
from models.order import cancel_order, create_order, is_product_available


def make_product(quantity: int = 5) -> Product:
    return Product(1, "Ноутбук", Category(1, "Ноутбуки"), Manufacturer(1, "HP", "США"),
                   60000, quantity)


def test_order_attributes_and_str() -> None:
    product = make_product()
    order = Order(1, product, 2)
    assert order.product is product
    assert order.is_cancelled is False
    assert "Ноутбук" in str(order)


def test_is_product_available() -> None:
    assert is_product_available(make_product(), 3)
    assert not is_product_available(make_product(), 6)


def test_order_reduces_availability() -> None:
    product = make_product()
    orders: list[Order] = []
    assert create_order(orders, product, 5) is not None
    assert not is_product_available(product, 1)
    assert create_order(orders, product, 1) is None
    assert len(orders) == 1


def test_cancel_restores_quantity() -> None:
    product = make_product()
    orders: list[Order] = []
    order = create_order(orders, product, 5)
    assert order is not None
    assert cancel_order(orders, order.id)
    assert order.is_cancelled
    assert product.quantity == 5
    assert is_product_available(product, 5)


def test_cancelled_order_stays_and_cannot_be_cancelled_twice() -> None:
    product = make_product()
    orders: list[Order] = []
    order = create_order(orders, product, 2)
    assert order is not None
    cancel_order(orders, order.id)
    assert orders == [order]
    assert not cancel_order(orders, order.id)
    assert product.quantity == 5
