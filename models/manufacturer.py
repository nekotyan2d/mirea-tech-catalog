from typing import List, Optional


class Manufacturer:
    def __init__(self, manufacturer_id: int, name: str, country: str) -> None:
        self.id = manufacturer_id
        self.name = name
        self.country = country

    def __str__(self) -> str:
        return f"Производитель {self.id}: {self.name} ({self.country})"

    @classmethod
    def from_data(cls, data: dict) -> "Manufacturer":
        return cls(data["id"], data["name"], data["country"])


def add_manufacturer(
    manufacturers: List[Manufacturer], name: str, country: str
) -> Manufacturer:
    manufacturer_id = max((m.id for m in manufacturers), default=0) + 1
    manufacturer = Manufacturer(manufacturer_id, name, country)
    manufacturers.append(manufacturer)
    return manufacturer


def find_manufacturer_by_name(
    manufacturers: List[Manufacturer], name: str
) -> Optional[Manufacturer]:
    for manufacturer in manufacturers:
        if manufacturer.name.lower() == name.lower():
            return manufacturer
    return None


def get_manufacturer_name(manufacturers: List[Manufacturer], manufacturer_id: int) -> str:
    for manufacturer in manufacturers:
        if manufacturer.id == manufacturer_id:
            return manufacturer.name
    return "Неизвестный производитель"
