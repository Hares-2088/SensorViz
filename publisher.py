import adafruit_dht
import board
import paho.mqtt.client as mqtt
import time
import json

# DHT sensor setup
DHT_SENSOR = adafruit_dht.DHT11(board.D4)  # Use GPIO4 (BCM)

# MQTT setup
MQTT_BROKER = "localhost"
MQTT_TOPIC_TEMPHUM = "sensor/temphum"

client = mqtt.Client()

def publish_sensor_data():
    while True:
        try:
            # Read temperature and humidity
            temperature = DHT_SENSOR.temperature
            humidity = DHT_SENSOR.humidity
            if humidity is not None and temperature is not None:
                # Create a JSON payload
                sensor_data = json.dumps({
                    "temperature": round(temperature, 1),
                    "humidity": round(humidity, 1)
                })
                # Publish the JSON payload
                client.publish(MQTT_TOPIC_TEMPHUM, sensor_data)
                print(f"Published: {sensor_data}")
            else:
                print("Failed to read from sensor")
        except RuntimeError as error:
            # Handle occasional sensor read errors
            print(f"Sensor error: {error}")
        time.sleep(5)  # Publish data every 5 seconds

client.connect(MQTT_BROKER, 1883, 60)
client.loop_start()
publish_sensor_data()
