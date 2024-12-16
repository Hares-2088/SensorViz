import RPi.GPIO as GPIO
import time
from flask import Flask, render_template_string

# GPIO setup
LED_PIN = 18  # You can change this to the pin you are using
GPIO.setmode(GPIO.BCM)
GPIO.setup(LED_PIN, GPIO.OUT)

app = Flask(__name__)

HTML_TEMPLATE = """
<!doctype html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>LED Control</title>
</head>
<body>
    <h1>LED Control</h1>
    <button onclick="fetch('/on')">Turn On</button>
    <button onclick="fetch('/off')">Turn Off</button>
</body>
</html>
"""

def led_on():
    GPIO.output(LED_PIN, GPIO.HIGH)

def led_off():
    GPIO.output(LED_PIN, GPIO.LOW)

@app.route('/')
def home():
    return render_template_string(HTML_TEMPLATE)

@app.route('/on')
def turn_on():
    led_on()
    return "LED is ON"

@app.route('/off')
def turn_off():
    led_off()
    return "LED is OFF"

def main():
    try:
        app.run(host='0.0.0.0', port=5000)
    except KeyboardInterrupt:
        pass
    finally:
        GPIO.cleanup()

# Example usage
if __name__ == "__main__":
    main()
