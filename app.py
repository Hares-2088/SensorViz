from flask import Flask, render_template, jsonify
import threading
import paho.mqtt.client as mqtt
import os
from datetime import datetime, timedelta

app = Flask(__name__)

# MQTT Configuration
BROKER = "localhost"
PORT = 1883
TOPIC = "sensor/temperature"

# Data Storage
sensor_data = {"temperature": [], "humidity": []}

# MQTT Callback Functions
def on_connect(client, userdata, flags, rc):
    print(f"Connected with result code {rc}")
    client.subscribe(TOPIC)

def on_message(client, userdata, msg):
    global sensor_data
    try:
        data = msg.payload.decode().split(",")
        temperature, humidity = float(data[0]), float(data[1])
        sensor_data["temperature"].append(temperature)
        sensor_data["humidity"].append(humidity)
    except Exception as e:
        print(f"Error processing message: {e}")

# Start MQTT Client in a Separate Thread
def start_mqtt():
    client = mqtt.Client()
    client.on_connect = on_connect
    client.on_message = on_message
    client.connect(BROKER, PORT, 60)
    client.loop_forever()

threading.Thread(target=start_mqtt, daemon=True).start()

# Function to Read Historical Data from a File
def read_historical_data():
    historical_data = []
    file_path = 'data/historical_data.txt'

    if os.path.exists(file_path):
        with open(file_path, 'r') as file:
            for line in file:
                timestamp, value = line.strip().split(',')
                historical_data.append({
                    "timestamp": timestamp,
                    "value": float(value)
                })
    return historical_data

# Flask Routes
@app.route("/")
def home():
    return render_template("index.html")

@app.route("/live-data")
def live_data_page():
    return render_template("live_data.html")

@app.route("/historical")
def historical_page():
    return render_template("historicaldata.html")

@app.route("/api/live-data")
def get_live_data():
    # Limit the data returned to avoid overloading the frontend
    latest_data = {
        "temperature": sensor_data["temperature"][-20:],  # Last 20 readings
        "humidity": sensor_data["humidity"][-20:]
    }
    return jsonify(latest_data)

@app.route("/historical-data")
def historical_data():
    data = read_historical_data()
    return jsonify(data)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
