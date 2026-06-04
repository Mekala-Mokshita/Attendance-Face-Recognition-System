import sqlite3

conn = sqlite3.connect("students.db")

cursor = conn.cursor()

students = [
    (101, "mokshi", "CSE", 3),
    (102, "arjun", "CSE", 3),
    (103, "sri", "AIDS", 3)
]

cursor.executemany(
    "INSERT OR REPLACE INTO students VALUES(?,?,?,?)",
    students
)

conn.commit()
conn.close()

print("Students added!")