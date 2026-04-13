# simulate_sensor.py  (run in a second terminal)
import paho.mqtt.client as mqtt
import json
import numpy as np
import time
from mqtt_client import save_to_csv

BROKER = "broker.hivemq.com"
TOPIC = "maji/sensors/vibration"

client = mqtt.Client(
    client_id="fake-sensor",
    callback_api_version=mqtt.CallbackAPIVersion.VERSION2
)
client.connect(BROKER, 1883)

for i in range(5):   # send 5 fake readings
    payload = {
        "device_id": "pipe_01",
        "vibration_data": list(np.random.normal(0, 0.5, 1000))
    }
    client.publish(TOPIC, json.dumps(payload))
    print(f"📤 Sent reading {i+1}")
    time.sleep(2)

client.disconnect()