from categories import add_category, find_category_by_name, get_category_name
from manufacturers import (
    add_manufacturer,
    find_manufacturer_by_name,
    get_manufacturer_name,
)
from orders import cancel_order, create_order, get_order_status
from products import (
    add_product,
    check_stock,
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


def get_or_create_category(categories: dict[int, dict], name: str) -> int:
    category_id = find_category_by_name(categories, name)
    if category_id is None:
        category_id = add_category(categories, name)
    return category_id


def get_or_create_manufacturer(
    manufacturers: dict[int, dict], name: str, country: str
) -> int:
    manufacturer_id = find_manufacturer_by_name(manufacturers, name)
    if manufacturer_id is None:
        manufacturer_id = add_manufacturer(manufacturers, name, country)
    return manufacturer_id


def show_products(
    products: dict[int, dict],
    categories: dict[int, dict],
    manufacturers: dict[int, dict],
) -> None:
    if not products:
        print("Каталог пуст.")
        return
    print(
        f"{'ID':<4}{'Название':<22}{'Категория':<15}"
        f"{'Производитель':<15}{'Цена':<10}{'Кол-во':<6}"
    )
    for product in products.values():
        category_name = get_category_name(categories, product["category_id"])
        manufacturer_name = get_manufacturer_name(
            manufacturers, product["manufacturer_id"]
        )
        print(
            f"{product['id']:<4}{product['name']:<22}{category_name:<15}"
            f"{manufacturer_name:<15}{product['price']:<10}"
            f"{product['quantity']:<6}"
        )


def show_orders(orders: list[dict], products: dict[int, dict]) -> None:
    if not orders:
        print("Заказов нет.")
        return
    for order in orders:
        product = products.get(order["product_id"])
        product_name = product["name"] if product else "Неизвестный товар"
        print(
            f"Заказ {order['id']}: {product_name}, "
            f"количество: {order['quantity']}, статус: {order['status']}"
        )


def main() -> None:
    products = load_products(PRODUCTS_FILE)
    orders = load_orders(ORDERS_FILE)
    categories = load_categories(CATEGORIES_FILE)
    manufacturers = load_manufacturers(MANUFACTURERS_FILE)

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
            show_products(products, categories, manufacturers)

        elif choice == "2":
            query = input("Название или часть названия: ")
            found = find_product(products, query)
            show_products(
                {item["id"]: item for item in found}, categories, manufacturers
            )

        elif choice == "3":
            product_id = input_int("ID товара: ")
            quantity = input_int("Требуемое количество: ")
            available = check_stock(products, product_id, quantity)
            print("Товар в наличии" if available else "Недостаточно товара")

        elif choice == "4":
            category_name = input("Категория: ")
            category_id = find_category_by_name(categories, category_name)
            if category_id is None:
                print("Такой категории нет в каталоге.")
            else:
                found = filter_products_by_category(products, category_id)
                show_products(
                    {item["id"]: item for item in found}, categories, manufacturers
                )

        elif choice == "5":
            min_price = input_float("Минимальная цена: ")
            max_price = input_float("Максимальная цена: ")
            found = filter_products_by_price(products, min_price, max_price)
            show_products(
                {item["id"]: item for item in found}, categories, manufacturers
            )

        elif choice == "6":
            by = input("Сортировать по (price/name): ") or "price"
            for product in sort_products(products, by):
                print(f"{product['name']} — {product['price']} руб.")

        elif choice == "7":
            product_id = input_int("ID товара: ")
            quantity = input_int("Количество: ")
            order = create_order(products, orders, product_id, quantity)
            print(get_order_status(order is not None))
            if order is not None:
                print(f"Заказ №{order['id']} создан.")

        elif choice == "8":
            order_id = input_int("ID заказа для отмены: ")
            if cancel_order(orders, order_id):
                print("Заказ отменен.")
            else:
                print("Заказ не найден или уже отменен.")

        elif choice == "9":
            show_orders(orders, products)

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
            category_id = get_or_create_category(categories, category_name)
            manufacturer_id = get_or_create_manufacturer(
                manufacturers, manufacturer_name, country
            )
            product_id = add_product(
                products, name, category_id, manufacturer_id, price, quantity
            )
            print(f"Товар добавлен с ID {product_id}.")

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
