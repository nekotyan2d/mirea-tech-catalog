import sqlite3
from collections.abc import Sequence
from functools import lru_cache
from typing import Any

from db.database import ROOT, get_connection

QUERIES_PATH = ROOT / "sql" / "queries.sql"


@lru_cache(maxsize=1)
def _load() -> dict[str, str]:
    queries: dict[str, list[str]] = {}
    name: str | None = None
    for line in QUERIES_PATH.read_text(encoding="utf-8").splitlines():
        if line.startswith("-- name:"):
            name = line.split(":", 1)[1].strip()
            queries[name] = []
        elif name:
            queries[name].append(line)
    return {key: "\n".join(lines).strip() for key, lines in queries.items()}


def fetch_all(name: str, params: Sequence[Any] = ()) -> list[sqlite3.Row]:
    conn = get_connection()
    try:
        return conn.execute(_load()[name], params).fetchall()
    finally:
        conn.close()


def fetch_one(name: str, params: Sequence[Any] = ()) -> sqlite3.Row | None:
    rows = fetch_all(name, params)
    return rows[0] if rows else None
