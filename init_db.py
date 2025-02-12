import sqlite3

# Connect to the SQLite database (creates if it doesn't exist)
conn = sqlite3.connect("database/data.db")
cursor = conn.cursor()

# Read and execute the schema SQL file
with open("database/schema.sql", "r") as file:
    cursor.executescript(file.read())

# Commit changes and close the connection
conn.commit()
conn.close()

print("Database initialized successfully.")
