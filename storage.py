import json


def load_products(filename: str) -> dict[int, dict]:
    try:
        with open(filename, "r", encoding="utf-8") as file:
            items = json.load(file)
    except FileNotFoundError:
        return {}
    except json.JSONDecodeError:
        print(f"Файл {filename} поврежден, загружен пустой каталог.")
        return {}
    return {item["id"]: item for item in items}


def save_products(filename: str, products: dict[int, dict]) -> None:
    with open(filename, "w", encoding="utf-8") as file:
        json.dump(list(products.values()), file, ensure_ascii=False, indent=2)


def load_categories(filename: str) -> dict[int, dict]:
    try:
        with open(filename, "r", encoding="utf-8") as file:
            items = json.load(file)
    except FileNotFoundError:
        return {}
    except json.JSONDecodeError:
        print(f"Файл {filename} поврежден, загружен пустой список категорий.")
        return {}
    return {item["id"]: item for item in items}


def save_categories(filename: str, categories: dict[int, dict]) -> None:
    with open(filename, "w", encoding="utf-8") as file:
        json.dump(list(categories.values()), file, ensure_ascii=False, indent=2)


def load_manufacturers(filename: str) -> dict[int, dict]:
    try:
        with open(filename, "r", encoding="utf-8") as file:
            items = json.load(file)
    except FileNotFoundError:
        return {}
    except json.JSONDecodeError:
        print(f"Файл {filename} поврежден, загружен пустой список производителей.")
        return {}
    return {item["id"]: item for item in items}


def save_manufacturers(filename: str, manufacturers: dict[int, dict]) -> None:
    with open(filename, "w", encoding="utf-8") as file:
        json.dump(
            list(manufacturers.values()), file, ensure_ascii=False, indent=2
        )


def load_orders(filename: str) -> list[dict]:
    try:
        with open(filename, "r", encoding="utf-8") as file:
            return json.load(file)
    except FileNotFoundError:
        return []
    except json.JSONDecodeError:
        print(f"Файл {filename} поврежден, загружен пустой список заказов.")
        return []


def save_orders(filename: str, orders: list[dict]) -> None:
    with open(filename, "w", encoding="utf-8") as file:
        json.dump(orders, file, ensure_ascii=False, indent=2)
