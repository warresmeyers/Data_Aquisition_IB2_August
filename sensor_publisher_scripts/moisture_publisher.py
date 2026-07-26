import time
import json
from grove.grove_moisture_sensor import GroveMoistureSensor
from grove.display.jhd1802 import JHD1802
import paho.mqtt.client as mqtt

BROKER = "localhost"
PORT = 1883
TOPIC = "sensors/moisture"

lcd = JHD1802()                      # Grove 16x2 LCD, connected to I2C port
sensor = GroveMoistureSensor(0)      # Grove Moisture Sensor, connected to A0

client = mqtt.Client()
client.connect(BROKER, PORT, 60)

print("Moisture publisher started...")

while True:
    mois = sensor.moisture

    if 0 <= mois < 300:
        level = 'dry'
    elif 300 <= mois < 600:
        level = 'moist'
    else:
        level = 'wet'

    payload = json.dumps({"value": mois, "level": level})
    client.publish(TOPIC, payload)
    print(f"Published: {payload}")

    lcd.setCursor(0, 0)
    lcd.write('moisture: {0:>6}'.format(mois))
    lcd.setCursor(1, 0)
    lcd.write('{0:>16}'.format(level))

    time.sleep(1)