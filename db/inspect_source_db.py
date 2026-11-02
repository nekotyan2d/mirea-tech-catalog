import sqlite3
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
SOURCE_DB = BASE_DIR / "data" / "catalog.sqlite"


def inspect_db() -> None:
    if not SOURCE_DB.exists():
        raise FileNotFoundError(f"Исходная база не найдена: {SOURCE_DB}")

    with sqlite3.connect(SOURCE_DB) as connection:
        connection.row_factory = sqlite3.Row
        tables = connection.execute(
            """
            SELECT name
            FROM sqlite_master
            WHERE type = 'table'
              AND name NOT LIKE 'sqlite_%'
            ORDER BY name
            """
        ).fetchall()

        print(f"База данных: {SOURCE_DB}")
        print(f"Всего таблиц: {len(tables)}\n")

        for (table_name,) in tables:
            print(f"--- Таблица: {table_name} ---")
            columns = connection.execute(
                "SELECT name, type, [notnull], pk FROM pragma_table_info(?)",
                (table_name,),
            ).fetchall()
            for col in columns:
                pk = " [PK]" if col["pk"] else ""
                notnull = " NOT NULL" if col["notnull"] else ""
                print(f"  {col['name']}: {col['type']}{notnull}{pk}")

            if table_name == "categories":
                count = connection.execute(
                    "SELECT COUNT(*) FROM categories"
                ).fetchone()[0]
                rows = connection.execute(
                    "SELECT * FROM categories LIMIT 3"
                ).fetchall()
            elif table_name == "manufacturers":
                count = connection.execute(
                    "SELECT COUNT(*) FROM manufacturers"
                ).fetchone()[0]
                rows = connection.execute(
                    "SELECT * FROM manufacturers LIMIT 3"
                ).fetchall()
            elif table_name == "products":
                count = connection.execute(
                    "SELECT COUNT(*) FROM products"
                ).fetchone()[0]
                rows = connection.execute(
                    "SELECT * FROM products LIMIT 3"
                ).fetchall()
            elif table_name == "orders":
                count = connection.execute(
                    "SELECT COUNT(*) FROM orders"
                ).fetchone()[0]
                rows = connection.execute(
                    "SELECT * FROM orders LIMIT 3"
                ).fetchall()
            else:
                count = 0
                rows = []

            print(f"  Всего записей: {count}")
            for r in rows:
                print("   ", dict(r))
            print()


if __name__ == "__main__":
    inspect_db()
