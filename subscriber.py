import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import paho.mqtt.client as mqtt
from datetime import datetime

# MQTT Configuration
BROKER = "localhost"
PORT = 1883
TOPIC = "Sensor/Temperature"

# Data Storage
timestamps = []
temperatures = []
humidities = []

# MQTT Callback Functions
def on_connect(client, userdata, flags, rc):
    print("Connected to MQTT Broker")
    client.subscribe(TOPIC)

def on_message(client, userdata, msg):
    data = msg.payload.decode()
    print(f"Received: {data}")

    # Parse temperature and humidity
    if "Temperature" in data and "Humidity" in data:
        parts = data.split(", ")
        temp = float(parts[0].split(": ")[1][:-2])
        hum = float(parts[1].split(": ")[1][:-1])

        # Update data
        timestamps.append(datetime.now())
        temperatures.append(temp)
        humidities.append(hum)

# Initialize MQTT Client
client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message

client.connect(BROKER, PORT, 60)
client.loop_start()

# Plot Real-time Data
def update_plot(frame):
    plt.cla()
    plt.plot(timestamps, temperatures, label="Temperature (°C)", color="red")
    plt.plot(timestamps, humidities, label="Humidity (%)", color="blue")
    plt.xlabel("Time")
    plt.ylabel("Values")
    plt.legend(loc="upper left")
    plt.tight_layout()

plt.style.use("seaborn")
ani = FuncAnimation(plt.gcf(), update_plot, interval=1000)

try:
    plt.show()
except KeyboardInterrupt:
    print("Exiting...")
finally:
    client.loop_stop()
    client.disconnect()
