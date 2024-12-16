# 🌡️ IoT Dashboard with Flask and MQTT 🌟

Welcome to the **IoT Dashboard** project! This application provides real-time and historical data visualization for temperature and humidity using Flask, MQTT, and a DHT sensor. 📊

## 🚀 Features
- 🌍 **Live Data Monitoring**: Real-time temperature and humidity data displayed with dynamic charts.
- 🕰️ **Historical Data**: Persistent storage of sensor readings for future analysis.
- 🔗 **Interactive Web Interface**: Beautiful, responsive UI powered by Flask and Chart.js.
- 📡 **MQTT Integration**: Seamless communication between the Raspberry Pi and the web application.
- 🚨 **Motion Sensor Alerts**: Receive alerts when motion is detected in the house.
- 💡 **LED Control**: Control LEDs from the web application to indicate motion detection or manually turn them on/off.

## 🎥 Demo

Check out the demo of the IoT Dashboard in action:

[![IoT Dashboard Demo](https://img.youtube.com/vi/pNull4OindU/0.jpg)](https://youtu.be/pNull4OindU)


---

## 🛠️ Requirements
Before you begin, ensure you have the following:
- 🥧 Raspberry Pi with Python3 installed
- 📡 MQTT Broker (e.g., Mosquitto)
- 🌡️ DHT11 or DHT22 sensor
- 🚨 Motion sensor (e.g., PIR sensor)
- 💡 LEDs and appropriate resistors
- 📋 Installed Python libraries:
  - Flask
  - paho-mqtt
  - adafruit-circuitpython-dht
  - Chart.js
  - flask-cors (if needed for cross-origin requests)

---

## 🚦 How to Run the App

### 1️⃣ Clone the Repository
   ```bash
    git clone <your-repository-url>
    cd project
   ```

### 2️⃣ Install Required Libraries
  ```bash
    pip3 install flask paho-mqtt adafruit-circuitpython-dht flask-cors
   ```
### 3️⃣ Start the MQTT Broker
If using Mosquitto, start the service:

  ```bash
    sudo systemctl start mosquito
  ```
### 4️⃣ Run the MQTT Publisher
Open a terminal and run:

  ```bash
    sudo python3 publisher.py
  ```
### 5️⃣ Run the Flask App
In another terminal, run:

  ```bash
    sudo python3 app.py
  ```
### 6️⃣ Access the Web Interface 🌐

  ```bash
    [sudo python3 publisher.py](http://<your_raspberry_pi_ip>:5000)
   ```
Replace <your_raspberry_pi_ip> with the actual IP of your Raspberry Pi.

---

## 🌟 Usage

### Live Data
- Navigate to the **Live Data** page by clicking the link in the navigation bar or visiting:

  ```bash
  http://<your_raspberry_pi_ip>:5000/live-data
- Monitor real-time temperature and humidity data displayed on dynamic charts. 📈

### Historical Data
- Navigate to the **Historical Data** page by clicking the link in the navigation bar or visiting:

  ```yaml
  http://<your_raspberry_pi_ip>:5000/historical
- View historical temperature and humidity data stored in the `data/historical_data.txt` file. 🕰️
- Charts will display data points based on timestamps for easy analysis.

### Motion Sensor Alerts
- Receive alerts on the web interface when motion is detected in the house.
- The motion sensor can trigger an LED to blink, indicating that someone has entered the house and needs to turn off the security system.

### LED Control
- Control LEDs from the web application to indicate motion detection or manually turn them on/off.
- Navigate to the **LED Control** page by clicking the link in the navigation bar or visiting:

  ```bash
  http://<your_raspberry_pi_ip>:5000/led-control
- Use the interface to turn LEDs on or off as needed.

---

## 🛡️ Troubleshooting

### Common Issues and Solutions

#### **Port Conflict**
- If you encounter a "Port already in use" error when starting the Flask app:
1. Identify the process using the port:
   ```bash
   sudo lsof -i :5000
   ```
2. Kill the process:
   ```bash
   sudo kill -9 <PID>
   ```

#### **Sensor Issues**
- If the DHT sensor fails to provide readings:
- Ensure the sensor is correctly connected to GPIO4.
- Confirm that the sensor type (`DHT11` or `DHT22`) matches your setup in the `publisher.py` script.

#### **No Data on Charts**
- If charts are empty:
1. Verify that `publisher.py` is running and publishing data.
2. Use `mosquitto_sub` to confirm data is being sent to the correct topic:
   ```bash
   mosquitto_sub -h localhost -t sensor/temphum
   ```
3. Check the `/sensor-data` endpoint:
   ```bash
   curl http://<your_raspberry_pi_ip>:5000/sensor-data
   ```

---

## 👨‍💻 Contributions
We welcome contributions! 🎉 To contribute:
1. Fork the repository.
2. Create a new branch for your feature or bug fix.
3. Submit a pull request describing your changes.

Feel free to open issues for questions or feature requests! 💡

---

## 📜 License
This project is licensed under the [MIT License](LICENSE). Feel free to use, modify, and distribute it as needed.

---

Thank you for exploring the **IoT Dashboard** project! 🌟 If you have any questions or suggestions, feel free to reach out or open an issue. Happy coding! 😊




