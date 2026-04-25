import sqlite3

conn = sqlite3.connect("library.db")
cur = conn.cursor()


cur.execute("""
CREATE TABLE IF NOT EXISTS users (
    username TEXT PRIMARY KEY,
    password TEXT,
    role TEXT
)
""")


cur.execute("""
CREATE TABLE IF NOT EXISTS books (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT,
    status TEXT,
    lender TEXT,
    issue_date TEXT,
    due_date TEXT,
    return_date TEXT,
    fine INTEGER DEFAULT 0
)
""")


cur.execute("""
CREATE TABLE IF NOT EXISTS history (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    book_title TEXT,
    username TEXT,
    action TEXT,
    date TEXT
)
""")


cur.execute("""
INSERT OR IGNORE INTO users(username, password, role)
VALUES ('admin', 'admin', 'admin')
""")

conn.commit()
conn.close()

print("Database Ready ✔")