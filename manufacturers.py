def add_manufacturer(
    manufacturers: dict[int, dict], name: str, country: str
) -> int:
    manufacturer_id = max(manufacturers.keys(), default=0) + 1
    manufacturers[manufacturer_id] = {
        "id": manufacturer_id,
        "name": name,
        "country": country,
    }
    return manufacturer_id


def find_manufacturer_by_name(
    manufacturers: dict[int, dict], name: str
) -> int | None:
    for manufacturer in manufacturers.values():
        if manufacturer["name"].lower() == name.lower():
            return manufacturer["id"]
    return None


def get_manufacturer_name(manufacturers: dict[int, dict], manufacturer_id: int) -> str:
    manufacturer = manufacturers.get(manufacturer_id)
    return manufacturer["name"] if manufacturer else "Неизвестный производитель"
