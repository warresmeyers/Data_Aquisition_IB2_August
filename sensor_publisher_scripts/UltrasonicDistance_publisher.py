#!/usr/bin/env python
import time
import json
from grove.grove_servo import GroveServo
from grove.grove_ultrasonic_ranger import GroveUltrasonicRanger
import paho.mqtt.client as mqtt

BROKER = "localhost"
PORT = 1883
TOPIC = "sensors/distance"

sensor = GroveUltrasonicRanger(5)
servo = GroveServo(12)

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
        print('raw distance {:.1f} cm, angle {}, step_delay {:.3f}s'.format(raw_distance, angle, step_delay))

        time.sleep(step_delay)

if __name__ == '__main__':
    main()