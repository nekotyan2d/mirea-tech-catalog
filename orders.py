def is_product_available(
    products: dict[int, dict],
    orders: list[dict],
    product_id: int,
    quantity: int,
) -> bool:
    product = products.get(product_id)
    if product is None:
        return False
    reserved = sum(
        order["quantity"]
        for order in orders
        if order["product_id"] == product_id and order["status"] == "active"
    )
    return (product["quantity"] - reserved) >= quantity


def create_order(
    products: dict[int, dict],
    orders: list[dict],
    product_id: int,
    quantity: int,
) -> dict | None:
    if not is_product_available(products, orders, product_id, quantity):
        return None
    order_id = max((order["id"] for order in orders), default=0) + 1
    order = {
        "id": order_id,
        "product_id": product_id,
        "quantity": quantity,
        "status": "active",
    }
    orders.append(order)
    return order


def cancel_order(orders: list[dict], order_id: int) -> bool:
    for order in orders:
        if order["id"] == order_id and order["status"] == "active":
            order["status"] = "cancelled"
            return True
    return False


def get_order_status(is_available: bool) -> str:
    if is_available:
        return "Товар доступен для заказа"
    return "Товар недоступен в нужном количестве"
