import sqlite3

# Connect DB
conn = sqlite3.connect("app_data.db", check_same_thread=False)
cursor = conn.cursor()

# Create table
def create_tables():
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS reviews (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT,
        rating INTEGER,
        review TEXT
    )
    """)
    conn.commit()


# Insert review
def add_review(name, rating, review):
    cursor.execute(
        "INSERT INTO reviews (name, rating, review) VALUES (?, ?, ?)",
        (name, rating, review)
    )
    conn.commit()


# Get reviews
def get_reviews():
    cursor.execute("SELECT name, rating, review FROM reviews ORDER BY id DESC")
    return cursor.fetchall()
