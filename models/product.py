from typing import List

from .category import Category
from .manufacturer import Manufacturer


class Product:
    def __init__(
        self,
        product_id: int,
        name: str,
        category: Category,
        manufacturer: Manufacturer,
        price: float,
        quantity: int,
    ) -> None:
        self.id = product_id
        self.name = name
        self.category = category
        self.manufacturer = manufacturer
        self.price = price
        self.quantity = quantity

    def is_in_stock(self, min_quantity: int) -> bool:
        return self.quantity >= min_quantity

    def reduce_quantity(self, quantity: int) -> None:
        if quantity > self.quantity:
            raise ValueError("Недостаточно товара на складе")
        self.quantity -= quantity

    def increase_quantity(self, quantity: int) -> None:
        self.quantity += quantity

    @staticmethod
    def validate_price(price: float) -> bool:
        return price >= 0

    def __str__(self) -> str:
        return (
            f"{self.name} ({self.category.name}, {self.manufacturer.name}): "
            f"{self.price} руб., {self.quantity} шт."
        )


def add_product(
    products: List[Product],
    name: str,
    category: Category,
    manufacturer: Manufacturer,
    price: float,
    quantity: int,
) -> Product:
    product_id = max((p.id for p in products), default=0) + 1
    product = Product(product_id, name, category, manufacturer, price, quantity)
    products.append(product)
    return product


def find_product(products: List[Product], query: str) -> List[Product]:
    query = query.lower()
    return [p for p in products if query in p.name.lower()]


def filter_products_by_category(products: List[Product], category_id: int) -> List[Product]:
    return [p for p in products if p.category.id == category_id]


def filter_products_by_manufacturer(
    products: List[Product], manufacturer_id: int
) -> List[Product]:
    return [p for p in products if p.manufacturer.id == manufacturer_id]


def filter_products_by_price(
    products: List[Product], min_price: float, max_price: float
) -> List[Product]:
    return [p for p in products if min_price <= p.price <= max_price]


def sort_products(products: List[Product], by: str = "price") -> List[Product]:
    key_func = (lambda p: p.price) if by == "price" else (lambda p: p.name)
    return sorted(products, key=key_func)


def get_catalog_statistics(products: List[Product]) -> dict:
    if not products:
        return {"total_items": 0, "total_value": 0.0, "average_price": 0.0}
    total_items = sum(p.quantity for p in products)
    total_value = sum(p.price * p.quantity for p in products)
    average_price = sum(p.price for p in products) / len(products)
    return {
        "total_items": total_items,
        "total_value": round(total_value, 2),
        "average_price": round(average_price, 2),
    }
