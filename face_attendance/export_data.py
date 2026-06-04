import sqlite3
import pandas as pd

conn = sqlite3.connect("attendance.db")

df = pd.read_sql_query(
    "SELECT * FROM attendance",
    conn
)

conn.close()

df.to_csv(
    "attendance_data.csv",
    index=False
)

print("attendance_data.csv updated successfully!")