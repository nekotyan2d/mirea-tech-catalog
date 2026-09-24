import json
from typing import List

from models import Category, Manufacturer, Order, Product


def _load_json(filename: str, what: str) -> list:
    try:
        with open(filename, "r", encoding="utf-8") as file:
            return json.load(file)
    except FileNotFoundError:
        return []
    except json.JSONDecodeError:
        print(f"Файл {filename} поврежден, загружен пустой список ({what}).")
        return []


def _save_json(filename: str, items: list) -> None:
    with open(filename, "w", encoding="utf-8") as file:
        json.dump(items, file, ensure_ascii=False, indent=2)


def load_categories(filename: str) -> List[Category]:
    return [Category.from_data(i) for i in _load_json(filename, "категории")]


def save_categories(filename: str, categories: List[Category]) -> None:
    _save_json(filename, [{"id": c.id, "name": c.name} for c in categories])


def load_manufacturers(filename: str) -> List[Manufacturer]:
    return [Manufacturer.from_data(i) for i in _load_json(filename, "производители")]


def save_manufacturers(filename: str, manufacturers: List[Manufacturer]) -> None:
    _save_json(
        filename,
        [{"id": m.id, "name": m.name, "country": m.country} for m in manufacturers],
    )


def load_products(
    filename: str, categories: List[Category], manufacturers: List[Manufacturer]
) -> List[Product]:
    categories_by_id = {c.id: c for c in categories}
    manufacturers_by_id = {m.id: m for m in manufacturers}
    return [
        Product(
            i["id"],
            i["name"],
            categories_by_id[i["category_id"]],
            manufacturers_by_id[i["manufacturer_id"]],
            i["price"],
            i["quantity"],
        )
        for i in _load_json(filename, "товары")
    ]


def save_products(filename: str, products: List[Product]) -> None:
    _save_json(
        filename,
        [
            {
                "id": p.id,
                "name": p.name,
                "category_id": p.category.id,
                "manufacturer_id": p.manufacturer.id,
                "price": p.price,
                "quantity": p.quantity,
            }
            for p in products
        ],
    )


def load_orders(filename: str, products: List[Product]) -> List[Order]:
    products_by_id = {p.id: p for p in products}
    orders = []
    for i in _load_json(filename, "заказы"):
        order = Order(i["id"], products_by_id[i["product_id"]], i["quantity"])
        # формат файла не менялся: статус хранится строкой
        order.is_cancelled = i["status"] == "cancelled"
        orders.append(order)
    return orders


def save_orders(filename: str, orders: List[Order]) -> None:
    _save_json(
        filename,
        [
            {
                "id": o.id,
                "product_id": o.product.id,
                "quantity": o.quantity,
                "status": "cancelled" if o.is_cancelled else "active",
            }
            for o in orders
        ],
    )
