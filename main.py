from typing import List

from models import Category, Manufacturer, Order, Product
from models.category import add_category, find_category_by_name
from models.manufacturer import add_manufacturer, find_manufacturer_by_name
from models.order import cancel_order, create_order, get_order_status
from models.product import (
    add_product,
    filter_products_by_category,
    filter_products_by_price,
    find_product,
    get_catalog_statistics,
    sort_products,
)
from storage import (
    load_categories,
    load_manufacturers,
    load_orders,
    load_products,
    save_categories,
    save_manufacturers,
    save_orders,
    save_products,
)
from utils import input_float, input_int

PRODUCTS_FILE = "data/products.json"
ORDERS_FILE = "data/orders.json"
CATEGORIES_FILE = "data/categories.json"
MANUFACTURERS_FILE = "data/manufacturers.json"


def get_or_create_category(categories: List[Category], name: str) -> Category:
    return find_category_by_name(categories, name) or add_category(categories, name)


def get_or_create_manufacturer(
    manufacturers: List[Manufacturer], name: str, country: str
) -> Manufacturer:
    return find_manufacturer_by_name(manufacturers, name) or add_manufacturer(
        manufacturers, name, country
    )


def find_product_by_id(products: List[Product], product_id: int) -> Product | None:
    for product in products:
        if product.id == product_id:
            return product
    return None


def show_products(products: List[Product]) -> None:
    if not products:
        print("Каталог пуст.")
        return
    print(
        f"{'ID':<4}{'Название':<22}{'Категория':<15}"
        f"{'Производитель':<15}{'Цена':<10}{'Кол-во':<6}"
    )
    for product in products:
        print(
            f"{product.id:<4}{product.name:<22}{product.category.name:<15}"
            f"{product.manufacturer.name:<15}{product.price:<10}"
            f"{product.quantity:<6}"
        )


def show_orders(orders: List[Order]) -> None:
    if not orders:
        print("Заказов нет.")
        return
    for order in orders:
        print(order)


def main() -> None:
    categories = load_categories(CATEGORIES_FILE)
    manufacturers = load_manufacturers(MANUFACTURERS_FILE)
    products = load_products(PRODUCTS_FILE, categories, manufacturers)
    orders = load_orders(ORDERS_FILE, products)

    menu = """
=== Каталог компьютерной техники ===
1. Показать товары
2. Найти товар по названию
3. Проверить наличие на складе
4. Фильтр по категории
5. Фильтр по цене
6. Сортировать товары
7. Оформить заказ
8. Отменить заказ
9. Показать заказы
10. Статистика каталога
11. Добавить товар
0. Выход
Выберите действие: """

    while True:
        choice = input(menu)

        if choice == "1":
            show_products(products)

        elif choice == "2":
            query = input("Название или часть названия: ")
            show_products(find_product(products, query))

        elif choice == "3":
            product = find_product_by_id(products, input_int("ID товара: "))
            quantity = input_int("Требуемое количество: ")
            available = product is not None and product.is_in_stock(quantity)
            print("Товар в наличии" if available else "Недостаточно товара")

        elif choice == "4":
            category = find_category_by_name(categories, input("Категория: "))
            if category is None:
                print("Такой категории нет в каталоге.")
            else:
                show_products(filter_products_by_category(products, category.id))

        elif choice == "5":
            min_price = input_float("Минимальная цена: ")
            max_price = input_float("Максимальная цена: ")
            show_products(filter_products_by_price(products, min_price, max_price))

        elif choice == "6":
            by = input("Сортировать по (price/name): ") or "price"
            for product in sort_products(products, by):
                print(f"{product.name} — {product.price} руб.")

        elif choice == "7":
            product = find_product_by_id(products, input_int("ID товара: "))
            quantity = input_int("Количество: ")
            order = None
            if product is not None:
                order = create_order(orders, product, quantity)
            print(get_order_status(order is not None))
            if order is not None:
                print(f"Заказ №{order.id} создан.")

        elif choice == "8":
            order_id = input_int("ID заказа для отмены: ")
            if cancel_order(orders, order_id):
                print("Заказ отменен.")
            else:
                print("Заказ не найден или уже отменен.")

        elif choice == "9":
            show_orders(orders)

        elif choice == "10":
            stats = get_catalog_statistics(products)
            print(f"Всего единиц товара: {stats['total_items']}")
            print(f"Суммарная стоимость остатков: {stats['total_value']} руб.")
            print(f"Средняя цена товара: {stats['average_price']} руб.")

        elif choice == "11":
            name = input("Название товара: ")
            category_name = input("Категория: ")
            manufacturer_name = input("Производитель: ")
            country = input("Страна производителя: ")
            price = input_float("Цена: ")
            quantity = input_int("Количество: ")
            category = get_or_create_category(categories, category_name)
            manufacturer = get_or_create_manufacturer(
                manufacturers, manufacturer_name, country
            )
            product = add_product(
                products, name, category, manufacturer, price, quantity
            )
            print(f"Товар добавлен с ID {product.id}.")

        elif choice == "0":
            save_products(PRODUCTS_FILE, products)
            save_orders(ORDERS_FILE, orders)
            save_categories(CATEGORIES_FILE, categories)
            save_manufacturers(MANUFACTURERS_FILE, manufacturers)
            print("Данные сохранены. До свидания!")
            break

        else:
            print("Неизвестный пункт меню, попробуйте снова.")


if __name__ == "__main__":
    main()
