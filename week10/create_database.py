"""Create and seed the flyonwheels SQLite database."""

from __future__ import annotations

import hashlib
import sqlite3
from datetime import date, timedelta
from pathlib import Path


DB_PATH = Path(__file__).with_name("flyonwheels.db")


def hash_password(password: str) -> str:
    return hashlib.sha256(password.encode("utf-8")).hexdigest()


def create_schema(connection: sqlite3.Connection) -> None:
    connection.executescript(
        """
        PRAGMA foreign_keys = ON;

        CREATE TABLE user (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            admin INTEGER NOT NULL CHECK (admin IN (0, 1)),
            username TEXT NOT NULL UNIQUE,
            password TEXT NOT NULL
        );

        CREATE TABLE service (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL UNIQUE
        );

        CREATE TABLE bus_model (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL UNIQUE,
            seats INTEGER NOT NULL
        );

        CREATE TABLE run (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            service_id INTEGER NOT NULL,
            run_date TEXT NOT NULL,
            FOREIGN KEY (service_id) REFERENCES service (id)
        );

        CREATE TABLE bus (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            service_id INTEGER NOT NULL,
            bus_model_id INTEGER NOT NULL,
            schedule_type TEXT NOT NULL,
            weekend INTEGER NOT NULL CHECK (weekend IN (0, 1)),
            workday INTEGER NOT NULL CHECK (workday IN (0, 1)),
            FOREIGN KEY (service_id) REFERENCES service (id),
            FOREIGN KEY (bus_model_id) REFERENCES bus_model (id)
        );

        CREATE TABLE ticket (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            run_id INTEGER NOT NULL,
            number INTEGER NOT NULL DEFAULT 1,
            FOREIGN KEY (user_id) REFERENCES user (id),
            FOREIGN KEY (run_id) REFERENCES run (id)
        );
        """
    )


def seed_database(connection: sqlite3.Connection) -> None:
    cursor = connection.cursor()

    cursor.execute(
        "INSERT INTO user (admin, username, password) VALUES (?, ?, ?)",
        (1, "Bob", hash_password("pqr123#!")),
    )
    user_id = cursor.lastrowid

    services = [
        "Dublin to Kilkenny, 7pm",
        "Dublin to Letterkenny, 8am",
        "Dublin to Wicklow, 6pm",
    ]
    service_ids = {}
    for service_name in services:
        cursor.execute("INSERT INTO service (name) VALUES (?)", (service_name,))
        service_ids[service_name] = cursor.lastrowid

    bus_models = [("A", 30), ("B", 50)]
    bus_model_ids = {}
    for model_name, seats in bus_models:
        cursor.execute(
            "INSERT INTO bus_model (name, seats) VALUES (?, ?)",
            (model_name, seats),
        )
        bus_model_ids[model_name] = cursor.lastrowid

    today = date.today()
    run_dates = [today + timedelta(days=offset) for offset in range(7)]
    run_ids = {}
    for service_name, service_id in service_ids.items():
        for run_date in run_dates:
            cursor.execute(
                "INSERT INTO run (service_id, run_date) VALUES (?, ?)",
                (service_id, run_date.isoformat()),
            )
            run_ids[(service_name, run_date.isoformat())] = cursor.lastrowid

    for service_name, service_id in service_ids.items():
        cursor.execute(
            """
            INSERT INTO bus (service_id, bus_model_id, schedule_type, weekend, workday)
            VALUES (?, ?, ?, ?, ?)
            """,
            (service_id, bus_model_ids["A"], "weekends", 1, 0),
        )
        cursor.execute(
            """
            INSERT INTO bus (service_id, bus_model_id, schedule_type, weekend, workday)
            VALUES (?, ?, ?, ?, ?)
            """,
            (service_id, bus_model_ids["B"], "workdays", 0, 1),
        )

    next_day = (today + timedelta(days=1)).isoformat()
    ticket_run_id = run_ids[("Dublin to Letterkenny, 8am", next_day)]
    cursor.execute(
        "INSERT INTO ticket (user_id, run_id, number) VALUES (?, ?, ?)",
        (user_id, ticket_run_id, 1),
    )

    connection.commit()



def create_database() -> None:
    """Create and seed the flyonwheels database."""
    if DB_PATH.exists():
        DB_PATH.unlink()

    with sqlite3.connect(DB_PATH) as connection:
        create_schema(connection)
        seed_database(connection)


def main() -> None:
    """Entry point for creating the database."""
    create_database()



if __name__ == "__main__":
    main()