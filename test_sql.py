"""SQL-тесты на SQLite: выборки, агрегаты и проверки целостности данных.

Каждый тест получает свежую базу в памяти (изоляция данных): таблицы
пользователей и рендеров с внешним ключом и ограничением на баланс.
"""
import sqlite3
import pytest


@pytest.fixture()
def db():
    conn = sqlite3.connect(":memory:")
    conn.execute("PRAGMA foreign_keys = ON")
    cur = conn.cursor()

    cur.execute("""
        CREATE TABLE users (
            id      INTEGER PRIMARY KEY,
            name    TEXT NOT NULL,
            credits INTEGER NOT NULL CHECK (credits >= 0),
            lang    TEXT NOT NULL
        )""")
    cur.execute("""
        CREATE TABLE renders (
            id      INTEGER PRIMARY KEY,
            user_id INTEGER NOT NULL,
            preset  TEXT NOT NULL,
            status  TEXT NOT NULL,
            FOREIGN KEY (user_id) REFERENCES users(id)
        )""")

    cur.executemany("INSERT INTO users VALUES (?,?,?,?)", [
        (1, "Анна", 10, "ru"),
        (2, "Bob",   0, "en"),
        (3, "Олег",  5, "ru"),
    ])
    cur.executemany("INSERT INTO renders VALUES (?,?,?,?)", [
        (1, 1, "noir_bw",   "ok"),
        (2, 1, "cinematic", "ok"),
        (3, 1, "cold",      "failed"),
        (4, 3, "noir_bw",   "ok"),
    ])
    conn.commit()
    yield conn
    conn.close()


def test_count_users(db):
    assert db.execute("SELECT COUNT(*) FROM users").fetchone()[0] == 3


def test_where_filter(db):
    rows = db.execute("SELECT name FROM users WHERE lang = 'ru'").fetchall()
    assert [r[0] for r in rows] == ["Анна", "Олег"]


def test_join_user_and_renders(db):
    rows = db.execute("""
        SELECT users.name, renders.preset
        FROM renders
        JOIN users ON users.id = renders.user_id
        WHERE renders.status = 'ok'
        ORDER BY renders.id
    """).fetchall()
    assert rows == [("Анна", "noir_bw"), ("Анна", "cinematic"), ("Олег", "noir_bw")]


def test_group_by_count(db):
    rows = db.execute("""
        SELECT user_id, COUNT(*) FROM renders GROUP BY user_id ORDER BY user_id
    """).fetchall()
    assert dict(rows) == {1: 3, 3: 1}


def test_aggregate_sum(db):
    assert db.execute("SELECT SUM(credits) FROM users").fetchone()[0] == 15


def test_order_by_limit_top_user(db):
    top = db.execute(
        "SELECT name FROM users ORDER BY credits DESC LIMIT 1").fetchone()[0]
    assert top == "Анна"


def test_no_negative_balance(db):
    bad = db.execute("SELECT COUNT(*) FROM users WHERE credits < 0").fetchone()[0]
    assert bad == 0


def test_no_orphan_renders(db):
    # каждый рендер ссылается на существующего пользователя
    orphans = db.execute("""
        SELECT COUNT(*) FROM renders WHERE user_id NOT IN (SELECT id FROM users)
    """).fetchone()[0]
    assert orphans == 0


def test_db_blocks_negative_balance(db):
    # ограничение CHECK не должно допустить отрицательный баланс
    with pytest.raises(sqlite3.IntegrityError):
        db.execute("INSERT INTO users VALUES (99, 'X', -5, 'ru')")
