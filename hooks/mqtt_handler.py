import json
import paho.mqtt.client as mqtt
from processing.signal_processor import process_reading

BROKER = "localhost"
PORT = 1883
TOPIC = "sensors/water/vibration"

def on_connect(client, userdata, flags, reason_code, properties):
    if reason_code == 0:
        print("✅ Connected to MQTT broker")
        client.subscribe(TOPIC)
    else:
        print(f"❌ Failed to connect, code: {reason_code}")

def on_message(client, userdata, msg):
    try:
        payload = json.loads(msg.payload.decode())
        process_reading(payload)
    except Exception as e:
        print(f"Error processing message: {e}")

def start_mqtt():
    client = mqtt.Client(
        client_id="MajiVibrator API",
        callback_api_version=mqtt.CallbackAPIVersion.VERSION2  # required in 2.0+
    )
    client.on_connect = on_connect
    client.on_message = on_message
    client.connect(BROKER, PORT)
    client.loop_start()  # runs in background thread, doesn't block FastAPI