from flask import Flask, render_template, jsonify
import threading
import paho.mqtt.client as mqtt
import os
import json
from collections import deque
from datetime import datetime


app = Flask(__name__)

# MQTT Configuration
BROKER = "localhost"
PORT = 1883
TOPIC = "sensor/temphum"

# Data Storage (thread-safe)
sensor_data = {
    "temperature": deque(maxlen=20),  # Keep only the last 20 readings
    "humidity": deque(maxlen=20)
}

# MQTT Callback Functions
def on_connect(client, userdata, flags, rc):
    print(f"Connected with result code {rc}")
    print(f"Subscribing to topic: {TOPIC}")
    client.subscribe(TOPIC)

def on_message(client, userdata, msg):
    global sensor_data
    try:
        print(f"Received MQTT message: {msg.payload.decode()}")  # Debugging: Log received message

        # Parse the incoming MQTT message as JSON
        data = json.loads(msg.payload.decode())
        temperature = data.get("temperature", 0)
        humidity = data.get("humidity", 0)

        print(f"Parsed temperature: {temperature}, humidity: {humidity}")  # Debugging: Log parsed values

        # Update live sensor_data
        sensor_data["temperature"].append(temperature)
        sensor_data["humidity"].append(humidity)

        # Save to historical data file
        with open('data/historical_data.txt', 'a') as file:
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")  # Get the current timestamp
            file.write(f"{timestamp},{temperature},{humidity}\n")  # Write data to the file
            print(f"Saved to file: {timestamp}, {temperature}, {humidity}")  # Debugging: Log saved data

    except json.JSONDecodeError as e:
        print(f"JSON decode error: {e}")
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

# historical data
def read_historical_data():
    historical_data = []
    file_path = 'data/historical_data.txt'

    if os.path.exists(file_path):
        with open(file_path, 'r') as file:
            for line in file:
                timestamp, temperature, humidity = line.strip().split(',')
                historical_data.append({
                    "timestamp": timestamp,
                    "temperature": float(temperature),
                    "humidity": float(humidity)
                })
    return historical_data


# Flask Routes
@app.route("/")
def home():
    return render_template("index.html")

@app.route("/live-data")
def live_data_page():
    return render_template("live_data.html")

@app.route("/sensor-data")
def sensor_data_route():
    print("Request received for /sensor-data")
    return jsonify({
        "temperature": list(sensor_data["temperature"]) or [0],
        "humidity": list(sensor_data["humidity"]) or [0]
    })
    
@app.route("/historical-data")
def historical_data():
    data = read_historical_data()
    return jsonify(data)

@app.route("/historical")
def historical_page():
    return render_template("historical_data.html")



if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
