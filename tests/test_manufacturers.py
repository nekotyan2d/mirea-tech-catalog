from models import Manufacturer
from models.manufacturer import (
    add_manufacturer,
    find_manufacturer_by_name,
    get_manufacturer_name,
)


def test_manufacturer_attributes_and_str():
    manufacturer = Manufacturer(1, "HP", "США")
    assert (manufacturer.id, manufacturer.name, manufacturer.country) == (1, "HP", "США")
    assert "HP" in str(manufacturer)


def test_from_data():
    manufacturer = Manufacturer.from_data({"id": 2, "name": "Dell", "country": "США"})
    assert manufacturer.name == "Dell" and manufacturer.country == "США"


def test_add_manufacturer():
    manufacturers = []
    manufacturer = add_manufacturer(manufacturers, "HP", "США")
    assert manufacturers == [manufacturer]
    assert manufacturer.name == "HP"


def test_find_manufacturer_by_name():
    manufacturers = []
    add_manufacturer(manufacturers, "Dell", "США")
    assert find_manufacturer_by_name(manufacturers, "dell") is not None


def test_get_manufacturer_name_unknown():
    assert get_manufacturer_name([], 99) == "Неизвестный производитель"
