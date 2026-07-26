import time
import json
from seeed_dht import DHT
from grove.display.jhd1802 import JHD1802
import paho.mqtt.client as mqtt

BROKER = "localhost"
PORT = 1883
TOPIC = "sensors/temp_humidity"

lcd = JHD1802()          # Grove 16x2 LCD, connected to I2C port
sensor = DHT('11', 5)    # DHT11 sensor, connected to D5

client = mqtt.Client()
client.connect(BROKER, PORT, 60)

print("Temp/humidity publisher started...")

while True:
    try:
        humi, temp = sensor.read()
        if humi is not None and temp is not None:
            payload = json.dumps({"temp": temp, "humidity": humi})
            client.publish(TOPIC, payload)
            print(f"Published: {payload}")

            lcd.setCursor(0, 0)
            lcd.write('temperature: {0:2}C'.format(temp))
            lcd.setCursor(1, 0)
            lcd.write('humidity: {0:5}%'.format(humi))
    except Exception as e:
        print(f"DHT read error (normal, will retry): {e}")

    time.sleep(2)