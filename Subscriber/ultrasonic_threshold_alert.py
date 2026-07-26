import json
import paho.mqtt.client as mqtt

BROKER = "raspberrypi.local"
PORT = 1883
TOPIC = "sensors/distance"

DISTANCE_THRESHOLD = 10  # cm — alert if something is closer than this

below_threshold = False

def on_connect(client, userdata, flags, rc):
    print(f"Connected with result code {rc}")
    client.subscribe(TOPIC)
    print(f"Subscribed to {TOPIC}")

def on_message(client, userdata, msg):
    global below_threshold

    try:
        data = json.loads(msg.payload.decode())
    except json.JSONDecodeError:
        print(f"Could not parse payload: {msg.payload}")
        return

    value = data.get("value")
    if value is None:
        return

    if value < DISTANCE_THRESHOLD:
        if not below_threshold:
            print("\n" + "!" * 40)
            print(f"!!! ALERT: object at {value} cm, closer than {DISTANCE_THRESHOLD} cm !!!")
            print("!" * 40 + "\n")
            below_threshold = True
    else:
        below_threshold = False

client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message
client.connect(BROKER, PORT, 60)

print("Distance threshold alert started, waiting for messages...")
client.loop_forever()