# Project ARES Code

This folder contains all Python scripts used to run the internal environment of the ARES habitat.

- `temp_control.py`: Controls the heating system using SHT31-D sensor input and a GPIO relay.
- Future scripts: Humidity control, data logging, camera image capture, etc.

Ensure all required libraries are installed:
pip install adafruit-circuitpython-sht31d RPi.GPIO
import time
import board
import busio
import adafruit_sht31d
import RPi.GPIO as GPIO

# ---- Setup I2C for SHT31-D ----
i2c = busio.I2C(board.SCL, board.SDA)
sensor = adafruit_sht31d.SHT31D(i2c)

# ---- Setup Relay GPIO ----
RELAY_PIN = 17
GPIO.setmode(GPIO.BCM)
GPIO.setup(RELAY_PIN, GPIO.OUT)
GPIO.output(RELAY_PIN, GPIO.HIGH)  # Start with lamp OFF (relay logic is inverted)

# ---- Set temperature limits ----
LOW_TEMP = 20.0  # °C, turn on heat below this
HIGH_TEMP = 22.0  # °C, turn off heat above this

try:
    while True:
        temp = sensor.temperature
        humidity = sensor.relative_humidity
        print(f"Temp: {temp:.1f}°C | Humidity: {humidity:.1f}%")

        # Heat lamp control logic
        if temp < LOW_TEMP:
            GPIO.output(RELAY_PIN, GPIO.LOW)  # Turn ON lamp
            print("Heat lamp: ON")
        elif temp > HIGH_TEMP:
            GPIO.output(RELAY_PIN, GPIO.HIGH)  # Turn OFF lamp
            print("Heat lamp: OFF")

        time.sleep(5)  # Adjust as needed

except KeyboardInterrupt:
    print("Stopping...")

finally:
    GPIO.output(RELAY_PIN, GPIO.HIGH)
    GPIO.cleanup()
