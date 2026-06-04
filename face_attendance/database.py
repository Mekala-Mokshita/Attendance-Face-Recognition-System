import sqlite3

conn = sqlite3.connect("attendance.db")

cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS attendance(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT,
    time TEXT,
    date TEXT
)
""")

conn.commit()
conn.close()

print("Attendance table created!")