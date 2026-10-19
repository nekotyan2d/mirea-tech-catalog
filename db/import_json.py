import json

from db.database import ROOT, create_schema, get_connection

DATA = ROOT / "data"


def load_json(name):
    with open(DATA / name, encoding="utf-8") as file:
        return json.load(file)


def import_all(conn):
    """Пересоздает содержимое таблиц из JSON (порядок важен из-за внешних ключей)."""
    create_schema(conn)
    for table in ("orders", "products", "manufacturers", "categories"):
        conn.execute(f"DELETE FROM {table}")  # имена таблиц заданы кодом, не пользователем

    conn.executemany(
        "INSERT INTO categories (id, name) VALUES (?, ?)",
        [(c["id"], c["name"]) for c in load_json("categories.json")],
    )
    conn.executemany(
        "INSERT INTO manufacturers (id, name, country) VALUES (?, ?, ?)",
        [(m["id"], m["name"], m["country"]) for m in load_json("manufacturers.json")],
    )
    conn.executemany(
        """
        INSERT INTO products (id, name, category_id, manufacturer_id, price, quantity)
        VALUES (?, ?, ?, ?, ?, ?)
        """,
        [
            (p["id"], p["name"], p["category_id"], p["manufacturer_id"], p["price"], p["quantity"])
            for p in load_json("products.json")
        ],
    )
    conn.executemany(
        "INSERT INTO orders (id, product_id, quantity, is_cancelled) VALUES (?, ?, ?, ?)",
        [
            (o["id"], o["product_id"], o["quantity"], int(o["status"] == "cancelled"))
            for o in load_json("orders.json")
        ],
    )


def main():
    conn = get_connection()
    try:
        import_all(conn)
        conn.commit()
    except Exception:
        conn.rollback()
        raise
    finally:
        conn.close()


if __name__ == "__main__":
    main()
