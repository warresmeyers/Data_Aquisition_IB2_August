# Data Acquisition IB2 - August

Local MQTT-based sensor system on a Raspberry Pi 4 with Grove sensors and a self-hosted Mosquitto broker. The Pi reads sensors and publishes over MQTT. A PC subscribes, logs the data, and raises alerts when configured thresholds are crossed.

## Layout

| Path | Purpose |
|---|---|
| `mqtt_test/` | Basic pub/sub connectivity test against the local Mosquitto broker |
| `broker_config/` | Mosquitto broker configuration (listener/network settings) |
| `sensor_publisher_scripts/` | One publisher script per sensor, running on the Pi |
| `Subscriber/` | PC-side logging subscriber and per-sensor threshold alert scripts |

## Setup

```bash
python -m venv .venv
# Pi/Linux:   source .venv/bin/activate
# Windows:    .venv\Scripts\activate

pip install paho-mqtt seeed-python-dht numpy
pip install git+https://github.com/Seeed-Studio/grove.py.git

sudo raspi-config nonint do_i2c 0   # enable I2C for the LCD
sudo reboot
```
To open the virtual environment if it does not automatically load
```bash
cd Data_Aquisition_IB2_August
source .venv/bin/activate
```

## MQTT broker

| Field | Value |
|---|---|
| Host | Raspberry Pi (`raspberrypi.local` or Pi's IP: 192.168.1.10) |
| Port | 1883 |
| Auth | Anonymous (local, isolated network only) |
| Config | `broker_config/local.conf` → copy to `/etc/mosquitto/conf.d/` on the Pi, then `listener 1883 0.0.0.0` |

## Sensors implemented

All publisher scripts run on the Pi and connect to `localhost:1883`. All PC-side scripts (`Subscriber/`) connect to the Pi's address.

| Script | Sensor | Topic |
|---|---|---|
| `moisture_publisher.py` | Grove Moisture Sensor (A0) | `sensors/moisture` |
| `temp_humidity_publisher.py` | Grove Temp & Humidity / DHT11 (D5) | `sensors/temp_humidity` |
| `UltrasonicDistance_publisher.py` | Grove Ultrasonic Ranger (D5) + Servo (D12) | `sensors/distance` |
| `LED_publisher.py` | Grove Red LED Button (D5/D6) | `sensors/led_button` |

## Per-sensor quick reference

**Moisture** - polls every 1s, classifies as `dry` / `moist` / `wet`, displays on LCD.
```bash
python sensor_publisher_scripts/moisture_publisher.py
```

**Temperature & Humidity** - reads DHT11 via `seeed_dht`, publishes every 2s.
```bash
python sensor_publisher_scripts/temp_humidity_publisher.py
```

**Ultrasonic Distance** - closer object → faster servo sweep. publishes raw distance every step.
```bash
python sensor_publisher_scripts/UltrasonicDistance_publisher.py
```

**LED Button** - polls button state (GPIO, no interrupts), toggles LED, publishes on each press.
```bash
python sensor_publisher_scripts/LED_publisher.py
```

## Broker connectivity test

Before running the real sensor scripts, `mqtt_test/` can be used to confirm the broker is reachable:
```bash
python mqtt_test/mqtt_publisher.py
python mqtt_test/mqtt_subscriber.py
```

## Subscribing / alerting (PC side)

```bash
python Subscriber/Subscriber.py                            # all topics, logs to sensor_log.txt
python Subscriber/Subscriber.py sensors/moisture            # single topic

python Subscriber/moisture_threshold_alert.py
python Subscriber/ultrasonic_threshold_alert.py
python Subscriber/temp_humidity_threshold_alert.py
```

Threshold alert scripts are edge-triggered — they fire once on crossing the threshold, not repeatedly while the value stays above/below it. Threshold values are constants at the top of each script.

