#!/usr/bin/env python
import time
import json
import RPi.GPIO as GPIO
from grove.display.jhd1802 import JHD1802
import paho.mqtt.client as mqtt

BROKER = "localhost"
PORT = 1883
TOPIC = "sensors/led_button"

LED_PIN = 5      # D5
BUTTON_PIN = 6   # D5 + 1, per Grove-LED Button wiring

GPIO.setmode(GPIO.BCM)
GPIO.setup(LED_PIN, GPIO.OUT)
GPIO.setup(BUTTON_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)

lcd = JHD1802()

client = mqtt.Client()
client.connect(BROKER, PORT, 60)

def main():
    led_state = False
    last_button_state = GPIO.HIGH  # not pressed

    while True:
        button_state = GPIO.input(BUTTON_PIN)

        # Detect press: transition from HIGH (released) to LOW (pressed)
        if last_button_state == GPIO.HIGH and button_state == GPIO.LOW:
            led_state = not led_state
            GPIO.output(LED_PIN, led_state)

            lcd.clear()
            lcd.setCursor(0, 0)
            lcd.write('LED: ON' if led_state else 'LED: OFF')
            print('Button pressed - LED', 'ON' if led_state else 'OFF')

            payload = json.dumps({"led_state": "on" if led_state else "off"})
            client.publish(TOPIC, payload)

        last_button_state = button_state
        time.sleep(0.05)  # simple debounce / polling interval

if __name__ == '__main__':
    main()