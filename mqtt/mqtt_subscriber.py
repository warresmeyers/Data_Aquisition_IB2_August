import paho.mqtt.client as mqtt

# MQTT Broker settings
BROKER = "192.168.1.10"
PORT = 1883
TOPIC = "test/topic"

def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print("Connected to broker")
        client.subscribe(TOPIC)
        print(f"Subscribed to {TOPIC}")
    else:
        print(f"Connection failed with code {rc}")

def on_message(client, userdata, msg):
    print(f"Received: {msg.payload.decode()} on {msg.topic}")

# Create client and connect
client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message

print(f"Connecting to broker at {BROKER}...")
client.connect(BROKER, PORT, 60)

# Keep listening for messages
client.loop_forever()