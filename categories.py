def add_category(categories: dict[int, dict], name: str) -> int:
    category_id = max(categories.keys(), default=0) + 1
    categories[category_id] = {"id": category_id, "name": name}
    return category_id


def find_category_by_name(categories: dict[int, dict], name: str) -> int | None:
    for category in categories.values():
        if category["name"].lower() == name.lower():
            return category["id"]
    return None


def get_category_name(categories: dict[int, dict], category_id: int) -> str:
    category = categories.get(category_id)
    return category["name"] if category else "Неизвестная категория"
