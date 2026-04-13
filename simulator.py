import json
import time
import random
import numpy as np
import paho.mqtt.client as mqtt

BROKER = "broker.hivemq.com"   # or localhost if using local mosquitto
PORT = 1883
TOPIC = "maji/sensors/vibration"

client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)
client.connect(BROKER, PORT)
client.loop_start()

for i in range(20):
    payload = {
        "device_id": "pipe_01",
        "vibration_data": list(np.random.normal(0, 0.5, 1000))
    }
    result = client.publish(TOPIC, json.dumps(payload))
    result.wait_for_publish()
    print(f"Sent sample {i+1}")
    time.sleep(1)

client.loop_stop()
client.disconnect()