import time
import json
from grove.grove_servo import GroveServo
from grove.grove_ultrasonic_ranger import GroveUltrasonicRanger
from grove.display.jhd1802 import JHD1802
import paho.mqtt.client as mqtt

BROKER = "localhost"
PORT = 1883
TOPIC = "sensors/distance"

sensor = GroveUltrasonicRanger(5) #D5
servo = GroveServo(12) #D12 PWM capable port
lcd = JHD1802() # any I2C port

MIN_DISTANCE = 5
MAX_DISTANCE = 50
MIN_STEP_DELAY = 0.05
MAX_STEP_DELAY = 0.3

angle = 0
direction = 1

client = mqtt.Client()
client.connect(BROKER, PORT, 60)

def main():
    global angle, direction
    while True:
        raw_distance = sensor.get_distance()
        clamped = max(MIN_DISTANCE, min(MAX_DISTANCE, raw_distance))
        ratio = (clamped - MIN_DISTANCE) / (MAX_DISTANCE - MIN_DISTANCE)
        step_delay = MIN_STEP_DELAY + ratio * (MAX_STEP_DELAY - MIN_STEP_DELAY)

        angle += direction * 10
        if angle >= 180:
            angle = 180
            direction = -1
        elif angle <= 0:
            angle = 0
            direction = 1
        servo.setAngle(angle)

        payload = json.dumps({"value": round(raw_distance, 1)})
        client.publish(TOPIC, payload)

        lcd.setCursor(0, 0)
        lcd.write('Distance:       ')
        lcd.setCursor(1, 0)
        lcd.write('{:.1f} cm       '.format(raw_distance))

        print('raw distance {:.1f} cm, angle {}, step_delay {:.3f}s'.format(raw_distance, angle, step_delay))
        time.sleep(step_delay)

if __name__ == '__main__':
    main()