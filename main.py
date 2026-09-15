from datetime import date

product_name = "Ноутбук ProBook 450"
category = "Ноутбуки"
manufacturer = "HP"
price_input = "65000"
price = float(price_input)
quantity = 5
arrival_date = date(2026, 9, 15)


def is_in_stock(quantity):
    return quantity > 0


def get_stock_status(quantity):
    if is_in_stock(quantity):
        return "Товар в наличии"
    return "Товара нет в наличии"


def calculate_total_value(price, quantity):
    return price * quantity


print(f"Товар: {product_name}")
print(f"Категория: {category}")
print(f"Производитель: {manufacturer}")
print(f"Цена: {price} руб.")
print(f"Количество: {quantity} шт.")
print(f"Дата поступления: {arrival_date}")
print(get_stock_status(quantity))
print(f"Суммарная стоимость остатка: {calculate_total_value(price, quantity)} руб.")
