import paho.mqtt.client as mqtt
import time
from datetime import datetime

# MQTT Broker settings
BROKER = "192.168.1.10"
PORT = 1883
TOPIC = "test/topic"

def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print("Connected to broker")
    else:
        print(f"Connection failed with code {rc}")

# Create client and connect
client = mqtt.Client()
client.on_connect = on_connect

print(f"Connecting to broker at {BROKER}...")
client.connect(BROKER, PORT, 60)
client.loop_start()

# Publish messages
try:
    while True:
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        message = f"Hello from PC! Time: {timestamp}"
        client.publish(TOPIC, message)
        print(f"Published: {message}")
        time.sleep(2)
except KeyboardInterrupt:
    print("\nStopping...")
    client.loop_stop()
    client.disconnect()