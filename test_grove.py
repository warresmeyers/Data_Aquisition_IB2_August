import sys
sys.path.insert(0, '/home/pi/Data_Aquisition_IB2_August/.venv/lib/python3.13/site-packages')

from grove.grove_led import GroveLed
import time

led = GroveLed(5)
led.on()
time.sleep(1)
led.off()
print("Grove LED test passed!")
