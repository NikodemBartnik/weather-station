import streamlit as st
import pymongo
from datetime import datetime

# MongoDB connection
client = pymongo.MongoClient("mongodb://admin:password@mongodb:27017/")
db = client["project"]
collection = db["weather_data"]

# Page configuration
st.set_page_config(page_title="Weather Data", layout="centered")

# Title and description
st.title("Weather Station Dashboard")
st.markdown("A clean and simple interface to display live weather data.")

# Get the latest weather data
def get_latest_data():
    latest_data = list(collection.find().sort("timestamp", -1).limit(10))
    return latest_data

# Display the data
weather_data = get_latest_data()

st.write("### Recent Weather Data")
for data in weather_data:
    st.write(f"**Station ID**: {data['station_id']}")
    st.write(f"**Timestamp**: {data['timestamp'].strftime('%Y-%m-%d %H:%M:%S')}")
    st.write(f"**Temperature**: {data['temperature']}°C")
    st.write(f"**Humidity**: {data['humidity']}%")
    st.write(f"**Wind Speed**: {data['wind_speed']} m/s")
    st.write(f"**Pressure**: {data['pressure']} hPa")
    st.markdown("---")

# Add a chart (for temperature trend)
import pandas as pd

df = pd.DataFrame(weather_data)
df['timestamp'] = pd.to_datetime(df['timestamp'])
df.set_index('timestamp', inplace=True)

st.line_chart(df['temperature'], width=700, height=400)

# Footer
st.markdown("Weather data visualized from Raspberry Pi-powered stations.")

