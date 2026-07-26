#!/usr/bin/env python
import time
from grove.grove_servo import GroveServo
from grove.grove_ultrasonic_ranger import GroveUltrasonicRanger

sensor = GroveUltrasonicRanger(5)
servo = GroveServo(12)

MIN_DISTANCE = 5
MAX_DISTANCE = 50
MIN_STEP_DELAY = 0.05   # was 0.01 — raised so it never spins too fast
MAX_STEP_DELAY = 0.3    # was 0.2 — raised slightly so slow end is calmer too

angle = 0
direction = 1

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
        print('raw distance {:.1f} cm, angle {}, step_delay {:.3f}s'.format(raw_distance, angle, step_delay))

        time.sleep(step_delay)

if __name__ == '__main__':
    main()