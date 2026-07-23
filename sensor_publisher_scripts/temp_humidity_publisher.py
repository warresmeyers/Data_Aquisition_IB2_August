import time
import json
import board
import adafruit_dht
import paho.mqtt.client as mqtt

BROKER = "localhost"
PORT = 1883
TOPIC = "sensors/temp_humidity"
PIN = board.D5  # adjust to whichever digital port you wired it to

dht = adafruit_dht.DHT11(PIN)
client = mqtt.Client()
client.connect(BROKER, PORT, 60)

print("Temp/humidity publisher started...")

while True:
    try:
        temp = dht.temperature
        humidity = dht.humidity
        if temp is not None and humidity is not None:
            payload = json.dumps({"temp": temp, "humidity": humidity})
            client.publish(TOPIC, payload)
            print(f"Published: {payload}")
    except RuntimeError as e:
        print(f"DHT read error (normal, will retry): {e}")

    time.sleep(2)