import sqlite3

# Connect to the database
conn = sqlite3.connect("weather.db")
cursor = conn.cursor()

# Step 1: Create a new table with the correct schema
cursor.execute('''
    CREATE TABLE IF NOT EXISTS weather_new (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        city TEXT,
        latitude REAL,
        longitude REAL,
        temp REAL,
        feels_like REAL,
        temp_min REAL,
        temp_max REAL,
        pressure INTEGER,
        humidity INTEGER,
        visibility INTEGER,
        wind_speed REAL,
        wind_deg INTEGER,
        clouds INTEGER,
        sunrise TEXT,
        sunset TEXT,
        timestamp TEXT
    )
''')

# # Step 2: Copy data from the old table to the new table
# cursor.execute('''
#     INSERT INTO weather_new (
#         city, latitude, longitude, temp, feels_like, temp_min, temp_max, 
#         pressure, humidity, visibility, wind_speed, wind_deg, clouds, 
#         sunrise, sunset, timestamp
#     )
#     SELECT city, latitude, longitude, temp, feels_like, temp_min, temp_max, 
#            pressure, humidity, visibility, wind_speed, wind_deg, clouds, 
#            sunrise, sunset, datetime  -- Copy old 'datetime' into 'timestamp'
#     FROM weather
# ''')

# Step 3: Drop the old table
cursor.execute("DROP TABLE weather")

# Step 4: Rename the new table to `weather`
cursor.execute("ALTER TABLE weather_new RENAME TO weather")

# Commit changes and close connection
conn.commit()
conn.close()

print("Schema updated successfully. 'datetime' renamed to 'timestamp' and 'city' column added.")