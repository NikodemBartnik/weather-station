from flask import Flask, request, jsonify
from pymongo import MongoClient
from datetime import datetime
import os

app = Flask(__name__)

# Set up MongoDB client
mongo_uri = f"mongodb://{os.environ['MONGO_INITDB_ROOT_USERNAME']}:{os.environ['MONGO_INITDB_ROOT_PASSWORD']}@mongodb:27017/project?authSource=admin"
client = MongoClient(mongo_uri)
db = client.project


# POST /api/weather - Log weather data
@app.route('/api/weather', methods=['POST'])
def log_weather_data():
    data = request.get_json()
    station_id = data.get('station_id')
    temperature = data.get('temperature')
    humidity = data.get('humidity')
    wind_speed = data.get('wind_speed')
    pressure = data.get('pressure')

    if not all([station_id, temperature, humidity, wind_speed, pressure]):
        return jsonify({"error": "Missing data"}), 400

    weather_data = {
        "station_id": station_id,
        "timestamp": datetime.utcnow(),
        "temperature": temperature,
        "humidity": humidity,
        "wind_speed": wind_speed,
        "pressure": pressure
    }

    db.weather_data.insert_one(weather_data)
    return jsonify({"message": "Weather data logged successfully"}), 201

# GET /api/weather - Retrieve all weather data
@app.route('/api/weather', methods=['GET'])
def get_weather_data():
    weather_data = list(db.weather_data.find({}, {'_id': 0}))
    return jsonify(weather_data), 200

# GET /api/weather/<station_id> - Get data for a specific station
@app.route('/api/weather/<station_id>', methods=['GET'])
def get_weather_data_for_station(station_id):
    weather_data = list(db.weather_data.find({"station_id": station_id}, {'_id': 0}))
    return jsonify(weather_data), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
