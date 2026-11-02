# pyright: reportAttributeAccessIssue=false, reportGeneralTypeIssues=false
import os
import sqlite3
import sys
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
if str(BASE_DIR) not in sys.path:
    sys.path.insert(0, str(BASE_DIR))

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "catalog.settings")

import django  # noqa: E402
django.setup()

from django.db import transaction  # noqa: E402
from orders.models import Order  # noqa: E402
from products.models import Category, Manufacturer, Product  # noqa: E402

SOURCE_DB = BASE_DIR / "data" / "catalog.sqlite"


def import_data() -> None:
    if not SOURCE_DB.exists():
        raise FileNotFoundError(f"Исходная база не найдена: {SOURCE_DB}")

    with sqlite3.connect(SOURCE_DB) as connection:
        connection.row_factory = sqlite3.Row

        categories = connection.execute(
            "SELECT id, name FROM categories ORDER BY id"
        ).fetchall()
        manufacturers = connection.execute(
            "SELECT id, name, country FROM manufacturers ORDER BY id"
        ).fetchall()
        products = connection.execute(
            """
            SELECT id, name, category_id, manufacturer_id, price, quantity
            FROM products
            ORDER BY id
            """
        ).fetchall()
        orders = connection.execute(
            """
            SELECT id, product_id, quantity, is_cancelled
            FROM orders
            ORDER BY id
            """
        ).fetchall()

    with transaction.atomic():
        cat_count = 0
        for row in categories:
            Category.objects.update_or_create(
                pk=row["id"],
                defaults={"name": row["name"]},
            )
            cat_count += 1

        man_count = 0
        for row in manufacturers:
            Manufacturer.objects.update_or_create(
                pk=row["id"],
                defaults={
                    "name": row["name"],
                    "country": row["country"],
                },
            )
            man_count += 1

        prod_count = 0
        for row in products:
            Product.objects.update_or_create(
                pk=row["id"],
                defaults={
                    "name": row["name"],
                    "category_id": row["category_id"],
                    "manufacturer_id": row["manufacturer_id"],
                    "price": row["price"],
                    "quantity": row["quantity"],
                },
            )
            prod_count += 1

        ord_count = 0
        for row in orders:
            Order.objects.update_or_create(
                pk=row["id"],
                defaults={
                    "product_id": row["product_id"],
                    "quantity": row["quantity"],
                    "is_cancelled": bool(row["is_cancelled"]),
                },
            )
            ord_count += 1

    print("Перенос данных из SQLite в Django ORM успешно завершён:")
    print(f"  Категорий перенесено: {cat_count}")
    print(f"  Производителей перенесено: {man_count}")
    print(f"  Товаров перенесено: {prod_count}")
    print(f"  Заказов перенесено: {ord_count}")


if __name__ == "__main__":
    import_data()
