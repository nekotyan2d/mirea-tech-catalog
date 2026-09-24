from typing import List, Optional

from .product import Product


class Order:
    def __init__(self, order_id: int, product: Product, quantity: int) -> None:
        self.id = order_id
        self.product = product
        self.quantity = quantity
        self.is_cancelled = False

    def cancel(self) -> None:
        if self.is_cancelled:
            return
        self.is_cancelled = True
        self.product.increase_quantity(self.quantity)

    def __str__(self) -> str:
        status = "отменен" if self.is_cancelled else "активен"
        return f"Заказ {self.id}: {self.product.name}, количество: {self.quantity}, {status}"


def is_product_available(product: Product, quantity: int) -> bool:
    return quantity > 0 and product.is_in_stock(quantity)


def create_order(orders: List[Order], product: Product, quantity: int) -> Optional[Order]:
    if not is_product_available(product, quantity):
        return None
    product.reduce_quantity(quantity)
    order_id = max((o.id for o in orders), default=0) + 1
    order = Order(order_id, product, quantity)
    orders.append(order)
    return order


def cancel_order(orders: List[Order], order_id: int) -> bool:
    for order in orders:
        if order.id == order_id and not order.is_cancelled:
            order.cancel()
            return True
    return False


def get_order_status(is_available: bool) -> str:
    if is_available:
        return "Товар доступен для заказа"
    return "Товар недоступен в нужном количестве"
