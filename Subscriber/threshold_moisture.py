import json
import paho.mqtt.client as mqtt

BROKER = "raspberrypi.local"   # Pi's address
PORT = 1883
TOPIC = "sensors/moisture"

# --- Configurable threshold ---
MOISTURE_THRESHOLD = 600   # trigger alert if moisture value exceeds this

def on_connect(client, userdata, flags, rc):
    print(f"Connected with result code {rc}")
    client.subscribe(TOPIC)
    print(f"Subscribed to {TOPIC}")

def on_message(client, userdata, msg):
    try:
        data = json.loads(msg.payload.decode())
    except json.JSONDecodeError:
        print(f"Could not parse payload: {msg.payload}")
        return

    value = data.get("value")
    print(f"Received: {data}")

    if value is not None and value > MOISTURE_THRESHOLD:
        print("\n" + "!" * 40)
        print(f"!!! ALERT: moisture value {value} exceeds threshold {MOISTURE_THRESHOLD} !!!")
        print("!" * 40 + "\n")

client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message

client.connect(BROKER, PORT, 60)

print("Threshold alert script started, waiting for messages...")
client.loop_forever()