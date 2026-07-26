import json
import paho.mqtt.client as mqtt

BROKER = "raspberrypi.local"   # Pi's address
PORT = 1883
TOPIC = "sensors/moisture"

# --- Configurable threshold ---
MOISTURE_THRESHOLD = 600   # trigger alert if moisture value exceeds this

# Track whether we're currently above threshold, to avoid repeat alerts
above_threshold = False

def on_connect(client, userdata, flags, rc):
    print(f"Connected with result code {rc}")
    client.subscribe(TOPIC)
    print(f"Subscribed to {TOPIC}")

def on_message(client, userdata, msg):
    global above_threshold

    try:
        data = json.loads(msg.payload.decode())
    except json.JSONDecodeError:
        print(f"Could not parse payload: {msg.payload}")
        return

    value = data.get("value")

    if value is None:
        return

    if value > MOISTURE_THRESHOLD:
        if not above_threshold:
            print("\n" + "!" * 40)
            print(f"!!! ALERT: moisture value {value} exceeded threshold {MOISTURE_THRESHOLD} !!!")
            print("!" * 40 + "\n")
            above_threshold = True
    else:
        above_threshold = False

client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message

client.connect(BROKER, PORT, 60)

print("Threshold alert script started, waiting for messages...")
client.loop_forever()