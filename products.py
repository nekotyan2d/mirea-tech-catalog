def add_product(
    products: dict[int, dict],
    name: str,
    category_id: int,
    manufacturer_id: int,
    price: float,
    quantity: int,
) -> int:
    product_id = max(products.keys(), default=0) + 1
    products[product_id] = {
        "id": product_id,
        "name": name,
        "category_id": category_id,
        "manufacturer_id": manufacturer_id,
        "price": price,
        "quantity": quantity,
    }
    return product_id


def find_product(products: dict[int, dict], query: str) -> list[dict]:
    query = query.lower()
    return [
        product
        for product in products.values()
        if query in product["name"].lower()
    ]


def check_stock(
    products: dict[int, dict], product_id: int, min_quantity: int
) -> bool:
    product = products.get(product_id)
    if product is None:
        return False
    return product["quantity"] >= min_quantity


def filter_products_by_category(
    products: dict[int, dict], category_id: int
) -> list[dict]:
    return [
        product
        for product in products.values()
        if product["category_id"] == category_id
    ]


def filter_products_by_manufacturer(
    products: dict[int, dict], manufacturer_id: int
) -> list[dict]:
    return [
        product
        for product in products.values()
        if product["manufacturer_id"] == manufacturer_id
    ]


def filter_products_by_price(
    products: dict[int, dict], min_price: float, max_price: float
) -> list[dict]:
    return list(
        product
        for product in products.values()
        if min_price <= product["price"] <= max_price
    )


def sort_products(products: dict[int, dict], by: str = "price") -> list[dict]:
    key_func = (lambda p: p["price"]) if by == "price" else (lambda p: p["name"])
    return sorted(products.values(), key=key_func)


def get_catalog_statistics(products: dict[int, dict]) -> dict:
    if not products:
        return {"total_items": 0, "total_value": 0.0, "average_price": 0.0}
    total_items = sum(p["quantity"] for p in products.values())
    total_value = sum(p["price"] * p["quantity"] for p in products.values())
    average_price = sum(p["price"] for p in products.values()) / len(products)
    return {
        "total_items": total_items,
        "total_value": round(total_value, 2),
        "average_price": round(average_price, 2),
    }
