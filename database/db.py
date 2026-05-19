import sqlite3
import os
from werkzeug.security import generate_password_hash

DB_PATH = os.path.join(os.path.dirname(__file__), "moneygoes.db")


def get_db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON")
    return conn


def init_db():
    conn = get_db()
    conn.executescript("""
        CREATE TABLE IF NOT EXISTS users (
            id            INTEGER PRIMARY KEY AUTOINCREMENT,
            name          TEXT    NOT NULL,
            email         TEXT    NOT NULL UNIQUE,
            password_hash TEXT    NOT NULL,
            created_at    TEXT    NOT NULL DEFAULT (datetime('now'))
        );

        CREATE TABLE IF NOT EXISTS expenses (
            id          INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id     INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE,
            amount      REAL    NOT NULL,
            category    TEXT    NOT NULL,
            date        TEXT    NOT NULL,
            description TEXT,
            created_at  TEXT    NOT NULL DEFAULT (datetime('now'))
        );
    """)
    conn.commit()
    conn.close()


def seed_db():
    conn = get_db()
    existing = conn.execute(
        "SELECT id FROM users WHERE email = ?", ("demo@moneygoes.com",)
    ).fetchone()
    if existing:
        conn.close()
        return

    conn.execute(
        "INSERT INTO users (name, email, password_hash) VALUES (?, ?, ?)",
        ("Demo User", "demo@moneygoes.com", generate_password_hash("demo123"))
    )
    conn.commit()

    user_id = conn.execute(
        "SELECT id FROM users WHERE email = ?", ("demo@moneygoes.com",)
    ).fetchone()["id"]

    expenses = [
        (user_id, 2500.00, "Food",          "2026-05-01", "Weekly groceries"),
        (user_id,  650.00, "Transport",     "2026-05-02", "Uber to office"),
        (user_id, 3200.00, "Bills",         "2026-05-03", "Electricity bill"),
        (user_id,  850.00, "Health",        "2026-05-05", "Pharmacy"),
        (user_id,  450.00, "Entertainment", "2026-05-08", "Netflix subscription"),
        (user_id, 4200.00, "Shopping",      "2026-05-10", "Shoes"),
        (user_id, 1100.00, "Food",          "2026-05-12", "Restaurant dinner"),
        (user_id,  300.00, "Other",         "2026-05-14", "Miscellaneous"),
    ]
    conn.executemany(
        "INSERT INTO expenses (user_id, amount, category, date, description) VALUES (?, ?, ?, ?, ?)",
        expenses
    )
    conn.commit()
    conn.close()
