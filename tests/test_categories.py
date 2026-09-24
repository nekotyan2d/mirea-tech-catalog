from models import Category
from models.category import add_category, find_category_by_name, get_category_name


def test_category_attributes_and_str():
    category = Category(1, "Ноутбуки")
    assert (category.id, category.name) == (1, "Ноутбуки")
    assert "Ноутбуки" in str(category)


def test_from_data():
    category = Category.from_data({"id": 2, "name": "Мониторы"})
    assert category.id == 2 and category.name == "Мониторы"


def test_add_category():
    categories = []
    category = add_category(categories, "Ноутбуки")
    assert categories == [category]
    assert category.name == "Ноутбуки"


def test_find_category_by_name():
    categories = []
    add_category(categories, "Мониторы")
    assert find_category_by_name(categories, "мониторы") is not None


def test_get_category_name_unknown():
    assert get_category_name([], 99) == "Неизвестная категория"
