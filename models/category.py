from typing import List, Optional


class Category:
    def __init__(self, category_id: int, name: str) -> None:
        self.id = category_id
        self.name = name

    def __str__(self) -> str:
        return f"Категория {self.id}: {self.name}"

    @classmethod
    def from_data(cls, data: dict) -> "Category":
        return cls(data["id"], data["name"])


def add_category(categories: List[Category], name: str) -> Category:
    category_id = max((c.id for c in categories), default=0) + 1
    category = Category(category_id, name)
    categories.append(category)
    return category


def find_category_by_name(categories: List[Category], name: str) -> Optional[Category]:
    for category in categories:
        if category.name.lower() == name.lower():
            return category
    return None


def get_category_name(categories: List[Category], category_id: int) -> str:
    for category in categories:
        if category.id == category_id:
            return category.name
    return "Неизвестная категория"
