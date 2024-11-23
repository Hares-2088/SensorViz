import paho.mqtt.client as mqtt
import Adafruit_DHT
import RPi.GPIO as GPIO
import time

# GPIO setup
GPIO.setmode(GPIO.BCM)
DHT_SENSOR = Adafruit_DHT.DHT22
DHT_PIN = 4  # GPIO pin connected to the DHT sensor
LED_PIN = 18  # GPIO pin connected to the LED
GPIO.setup(LED_PIN, GPIO.OUT)

# MQTT setup
MQTT_BROKER = "localhost"
MQTT_TOPIC_TEMPHUM = "sensor/temphum"
MQTT_TOPIC_LED = "sensor/led"

client = mqtt.Client()

def on_connect(client, userdata, flags, rc):
    print(f"Connected with result code {rc}")
    client.subscribe(MQTT_TOPIC_LED)

def on_message(client, userdata, msg):
    if msg.topic == MQTT_TOPIC_LED:
        if msg.payload.decode() == "ON":
            GPIO.output(LED_PIN, GPIO.HIGH)
        else:
            GPIO.output(LED_PIN, GPIO.LOW)

client.on_connect = on_connect
client.on_message = on_message
client.connect(MQTT_BROKER, 1883, 60)

def publish_sensor_data():
    while True:
        # Read temperature and humidity from DHT sensor
        humidity, temperature = Adafruit_DHT.read_retry(DHT_SENSOR, DHT_PIN)
        if humidity is not None and temperature is not None:
            sensor_data = f"{temperature:.1f},{humidity:.1f}"
            client.publish(MQTT_TOPIC_TEMPHUM, sensor_data)
            print(f"Published: {sensor_data}")
        else:
            print("Failed to read from sensor")
        time.sleep(5)  # Publish every 5 seconds

client.loop_start()
publish_sensor_data()
