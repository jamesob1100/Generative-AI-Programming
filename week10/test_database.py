"""Dump the contents of the flyonwheels SQLite database."""

from __future__ import annotations

import sqlite3
from pathlib import Path


DB_PATH = Path(__file__).with_name("flyonwheels.db")


def dump_tables(database_path: Path = DB_PATH) -> None:
    with sqlite3.connect(database_path) as connection:
        connection.row_factory = sqlite3.Row
        cursor = connection.cursor()

        cursor.execute(
            """
            SELECT name
            FROM sqlite_master
            WHERE type = 'table' AND name NOT LIKE 'sqlite_%'
            ORDER BY name
            """
        )
        tables = [row["name"] for row in cursor.fetchall()]

        for table_name in tables:
            print(f"[{table_name}]")
            rows = cursor.execute(f"SELECT * FROM {table_name}").fetchall()
            if not rows:
                print("<empty>")
                print()
                continue

            columns = rows[0].keys()
            print(" | ".join(columns))
            for row in rows:
                print(" | ".join(str(row[column]) for column in columns))
            print()


if __name__ == "__main__":
    dump_tables()