import time
import json
from grove.adc import ADC
import paho.mqtt.client as mqtt

BROKER = "localhost"  # running on the Pi itself, next to the broker
PORT = 1883
TOPIC = "sensors/moisture"
ADC_PORT = 0  # adjust to whichever Grove ADC port you wired it to

adc = ADC()
client = mqtt.Client()
client.connect(BROKER, PORT, 60)

print("Moisture publisher started...")

while True:
    try:
        moisture = adc.read(ADC_PORT)
        payload = json.dumps({"value": moisture})
        client.publish(TOPIC, payload)
        print(f"Published: {payload}")
    except Exception as e:
        print(f"Moisture read error: {e}")

    time.sleep(2)