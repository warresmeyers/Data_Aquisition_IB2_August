import sys
import time
import json
import paho.mqtt.client as mqtt

BROKER = "localhost"   # use the Pi's IP if running this on your PC instead
PORT = 1883
LOG_FILE = "sensor_log.txt"

ALL_TOPICS = ["sensors/moisture", "sensors/temp_humidity"]

# Use topic from command-line argument, or subscribe to all if not given
if len(sys.argv) > 1:
    TOPICS = [sys.argv[1]]
else:
    TOPICS = ALL_TOPICS

def on_connect(client, userdata, flags, rc):
    print(f"Connected with result code {rc}")
    for topic in TOPICS:
        client.subscribe(topic)
        print(f"Subscribed to {topic}")

def on_message(client, userdata, msg):
    timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
    try:
        data = json.loads(msg.payload.decode())
    except json.JSONDecodeError:
        data = msg.payload.decode()

    line = f"[{timestamp}] {msg.topic}: {data}"
    print(line)

    with open(LOG_FILE, "a") as f:
        f.write(line + "\n")

client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message

client.connect(BROKER, PORT, 60)

print("Subscriber started, waiting for messages...")
client.loop_forever()