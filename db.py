import sqlite3

def get_connection():
    return sqlite3.connect("app.py", check_same_thread=False)

def create_tables():
    conn = get_connection()
    c = conn.cursor()

    c.execute("""
    CREATE TABLE IF NOT EXISTS projects (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT
    )
    """)

    c.execute("""
    CREATE TABLE IF NOT EXISTS reviews (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT,
        rating INTEGER,
        review TEXT
    )
    """)

    conn.commit()
    conn.close()


def add_project(name):
    conn = get_connection()
    c = conn.cursor()
    c.execute("INSERT INTO projects (name) VALUES (?)", (name,))
    conn.commit()
    conn.close()


def get_projects():
    conn = get_connection()
    c = conn.cursor()
    c.execute("SELECT name FROM projects ORDER BY id DESC")
    data = c.fetchall()
    conn.close()
    return data


def add_review(name, rating, review):
    conn = get_connection()
    c = conn.cursor()
    c.execute(
        "INSERT INTO reviews (name, rating, review) VALUES (?, ?, ?)",
        (name, rating, review)
    )
    conn.commit()
    conn.close()


def get_reviews():
    conn = get_connection()
    c = conn.cursor()
    c.execute("SELECT name, rating, review FROM reviews ORDER BY id DESC")
    data = c.fetchall()
    conn.close()
    return data
