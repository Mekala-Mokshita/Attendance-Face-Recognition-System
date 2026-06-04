import sqlite3

conn = sqlite3.connect("students.db")

cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS students(
    student_id INTEGER PRIMARY KEY,
    name TEXT UNIQUE,
    department TEXT,
    year INTEGER
)
""")

conn.commit()
conn.close()

print("Students table created!")