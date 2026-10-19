from db.database import get_connection
from db.import_json import import_all


def test_import_json_to_sqlite():
    conn = get_connection(":memory:")
    import_all(conn)
    for table, count in (("categories", 3), ("manufacturers", 3), ("products", 3), ("orders", 2)):
        assert conn.execute(f"SELECT COUNT(*) FROM {table}").fetchone()[0] == count
    row = conn.execute("SELECT is_cancelled FROM orders WHERE id = 2").fetchone()
    assert row["is_cancelled"] == 1
