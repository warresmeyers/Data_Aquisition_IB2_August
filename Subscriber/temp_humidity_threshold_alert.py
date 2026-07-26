import json
import paho.mqtt.client as mqtt

BROKER = "raspberrypi.local"
PORT = 1883
TOPIC = "sensors/temp_humidity"

TEMP_THRESHOLD = 28  # degrees C

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

    temp = data.get("temp")
    if temp is None:
        return

    if temp > TEMP_THRESHOLD:
        if not above_threshold:
            print("\n" + "!" * 40)
            print(f"!!! ALERT: temperature {temp}C exceeded threshold {TEMP_THRESHOLD}C !!!")
            print("!" * 40 + "\n")
            above_threshold = True
    else:
        above_threshold = False

client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message
client.connect(BROKER, PORT, 60)

print("Temp/humidity threshold alert started, waiting for messages...")
client.loop_forever()