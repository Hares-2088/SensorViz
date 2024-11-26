from flask import Flask, render_template, jsonify
import threading
import paho.mqtt.client as mqtt
import os
import json
from collections import deque

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

        data = json.loads(msg.payload.decode())
        temperature = data.get("temperature", 0)
        humidity = data.get("humidity", 0)

        print(f"Parsed temperature: {temperature}, humidity: {humidity}")  # Debugging: Log parsed values

        sensor_data["temperature"].append(temperature)
        sensor_data["humidity"].append(humidity)
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


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
