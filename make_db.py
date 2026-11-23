import sqlite3
import pandas as pd

shots = pd.read_csv("shots.csv")
conn = sqlite3.connect("football.db")
shots.to_sql("shots", conn, if_exists="replace", index=False)
conn.close()
print("Database ready")