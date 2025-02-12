import os
import sqlite3
import requests
from datetime import datetime, timedelta, timezone
from dotenv import load_dotenv

# Load API key from .env
load_dotenv()
API_KEY = os.getenv("OPENWEATHER_API_KEY")
CITY = "Los Angeles"
BASE_URL = "https://api.openweathermap.org/data/2.5/weather"

# Database setup
DB_FILE = "weather.db"
conn = sqlite3.connect(DB_FILE)
cursor = conn.cursor()

# Create table with additional fields
cursor.execute('''
    CREATE TABLE IF NOT EXISTS weather (
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
        datetime TEXT
    )
''')
conn.commit()

def fetch_weather():
    params = {"q": CITY, "appid": API_KEY, "units": "metric"}
    response = requests.get(BASE_URL, params=params)
    data = response.json()

    if response.status_code == 200:
        # Extract relevant fields
        latitude = data["coord"]["lat"]
        longitude = data["coord"]["lon"]
        temp = data["main"]["temp"]
        feels_like = data["main"]["feels_like"]
        temp_min = data["main"]["temp_min"]
        temp_max = data["main"]["temp_max"]
        pressure = data["main"]["pressure"]
        humidity = data["main"]["humidity"]
        visibility = data.get("visibility", 0)
        wind_speed = data["wind"]["speed"]
        wind_deg = data["wind"]["deg"]
        clouds = data["clouds"]["all"]
        
        # Convert timestamps
        sunrise = datetime.fromtimestamp(data["sys"]["sunrise"], timezone.utc).strftime('%Y-%m-%d %H:%M:%S')
        sunset = datetime.fromtimestamp(data["sys"]["sunset"], timezone.utc).strftime('%Y-%m-%d %H:%M:%S')
        timestamp = datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M:%S')

        # Insert data into database
        cursor.execute('''
            INSERT INTO weather (city, latitude, longitude, temp, feels_like, temp_min, temp_max, pressure, humidity, visibility, wind_speed, wind_deg, clouds, sunrise, sunset, timestamp)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (CITY, latitude, longitude, temp, feels_like, temp_min, temp_max, pressure, humidity, visibility, wind_speed, wind_deg, clouds, sunrise, sunset, timestamp))
        conn.commit()
    else:
        print("Error fetching weather data:", data)

fetch_weather()

# Cleanup old data (older than 1 year)
def cleanup_old_data():
    one_year_ago = datetime.now(timezone.utc) - timedelta(days=365)
    cursor.execute("DELETE FROM weather WHERE timestamp < ?", (one_year_ago.strftime('%Y-%m-%d %H:%M:%S'),))
    conn.commit()

cleanup_old_data()
conn.close()


 
# TODO: Feature: Weather Data: Base Information - Map of world with weather and/or other information
# TODO: Feature: Weather Data: Base Information - Local weather map

# TODO: Feature: Statistics and Trends - World Bank API
# TODO: Feature: Statistics and Trends - COVID-19 Data API
# TODO: Feature: Statistics and Trends - US Government Open Data


# TODO: Feature: Local Traffic
# TODO: Feature: Statistics and Trends - Air Flights
# TODO: Feature: Statistics and Trends - Trains
# TODO: Feature: Statistics and Trends - Buses

# TODO: Feature: News and Events - NewsAPI
# TODO: Feature: News and Events - Reddit/Google Trends

# TODO: Feature: Planting and Harvesting - Almanac information - General
# TODO: Feature: Planting and Harvesting - Almanac information - Zone planning
# TODO: Feature: Planting and Harvesting - Almanac information - Yearly, monthly schedule recommendation and notes

# TODO: Feature: Astronomy Events - Meteor showers Phases of the moon, etc

# TODO: Feature: Personal Metrics - Authentication

# TODO: Feature: Personal Metrics - Food Menu
# TODO: Feature: Personal Metrics - Calorie Tracker
# TODO: Feature: Personal Metrics - Maintenance Chart
# TODO: Feature: Personal Metrics - Exercise Schedule
# TODO: Feature: Personal Metrics - Calendar Schedule

# TODO: Feature: Dynamic Checklists

# TODO: Security: Check in to what security should be implemented
