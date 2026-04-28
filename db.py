import sqlite3

conn = sqlite3.connect("app.db", check_same_thread=False)
c = conn.cursor()

def create_tables():
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


# ---------------- PROJECTS ----------------
def add_project(name):
    c.execute("INSERT INTO projects (name) VALUES (?)", (name,))
    conn.commit()

def get_projects():
    c.execute("SELECT name FROM projects ORDER BY id DESC")
    return c.fetchall()


# ---------------- REVIEWS ----------------
def add_review(name, rating, review):
    c.execute(
        "INSERT INTO reviews (name, rating, review) VALUES (?, ?, ?)",
        (name, rating, review)
    )
    conn.commit()

def get_reviews():
    c.execute("SELECT name, rating, review FROM reviews ORDER BY id DESC")
    return c.fetchall()
