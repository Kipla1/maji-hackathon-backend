import json
import csv
import os
from datetime import datetime
import paho.mqtt.client as mqtt
from processing.signal_processor import process_reading

BROKER = "broker.hivemq.com"
PORT = 1883
TOPIC = "maji/sensors/vibration"
DATA_FILE = "data/readings.csv"

def save_to_csv(payload, features):
    """
    Save sensor data to a CSV file.

    This function appends a new row of sensor data to a CSV file, creating the file
    and writing headers if it doesn't already exist.

    Args:
        payload (dict): A dictionary containing device information, expected to have
                        a "device_id" key. If "device_id" is missing, defaults to "unknown".
        features (dict): A dictionary containing extracted feature data, expected to have
                         "dominant_freq" and "rms" keys.

    Returns:
        None

    Line-by-line explanation:
        1. Check if the CSV file already exists to determine whether headers need to be written.
        2. Open the CSV file in append mode ("a") with no extra newlines to allow adding rows.
        3. Create a DictWriter object that maps Python dictionaries to CSV rows using specified field names.
        4. Define the column headers: timestamp, device_id, dominant_freq, and rms.
        5. If the file didn't exist, write the header row to establish column names.
        6. Write a new data row containing the current UTC timestamp in ISO format.
        7. Extract device_id from payload, using "unknown" as fallback if not present.
        8. Include the dominant_freq value from the features dictionary.
        9. Include the rms (root mean square) value from the features dictionary.
    """
    file_exists = os.path.isfile(DATA_FILE)

    fieldnames = [
        "timestamp",
        "device_id",
        "rms",
        "dominant_freq",
        "peak_amplitude",
        "variance",
        "zero_crossing_rate",
    ]

    with open(DATA_FILE, "a", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        if not file_exists:
            writer.writeheader()

        writer.writerow({
            "timestamp": datetime.utcnow().isoformat(),
            "device_id": payload.get("device_id", "unknown"),
            "rms": features["rms"],
            "dominant_freq": features["dominant_freq"],
            "peak_amplitude": features["peak_amplitude"],
            "variance": features["variance"],
            "zero_crossing_rate": features["zero_crossing_rate"],
        })


def on_connect(client, userdata, flags, reason_code, properties):
    """
    Callback function invoked when the MQTT client connects to the broker.
    
    This function is executed upon connection attempt to the MQTT broker and handles
    the connection result. If successful, it subscribes to the specified topic.
    If unsuccessful, it logs the failure reason code.
    
    Args:
        client: The MQTT client instance that initiated the connection.
        userdata: User-defined data passed to the client (typically None if not set).
        flags: Dictionary of connection flags (reserved for future use, typically unused).
        reason_code (int): Connection result code where 0 indicates successful connection,
                          and non-zero values indicate various failure reasons.
        properties: MQTT v5.0 properties object (typically None for MQTT v3.1.1).
    
    Returns:
        None
    
    Raises:
        None
    
    Note:
        Line 1: Checks if reason_code equals 0, which indicates a successful connection.
        Line 2: If connected successfully, prints a confirmation message with a checkmark emoji.
        Line 3: Subscribes the client to the TOPIC (must be defined globally).
        Line 4-5: If connection failed (reason_code != 0), prints an error message
                  displaying the specific reason code for debugging purposes.
    """
    if reason_code == 0:
        print("✅ Connected to MQTT broker")
        client.subscribe(TOPIC)
    else:
        print(f"❌ Connection failed: {reason_code}")

def on_message(client, userdata, msg):
    """
    MQTT message callback handler that processes incoming messages.
    
    This function is triggered whenever a message is received on a subscribed MQTT topic.
    It decodes the JSON payload, processes the reading data, and persists it to a CSV file
    if processing is successful.
    
    Args:
        client: The MQTT client instance that received the message.
        userdata: User-defined data passed to the client (typically None or a dict).
        msg: The MQTT message object containing the topic and payload.
        
    Returns:
        None
        
    Raises:
        Catches and logs any exceptions that occur during JSON parsing, processing,
        or file saving operations.
        
    Line-by-line explanation:
        - Line 1: Attempts to decode the message payload from bytes to UTF-8 string and parse as JSON
        - Line 2: Processes the decoded payload through feature extraction/transformation logic
        - Line 3: Checks if feature processing returned valid data (truthy value)
        - Line 4: Saves both the original payload and extracted features to a CSV file
        - Line 5: Prints a success message with the extracted features
        - Line 6-7: Catches any exceptions and prints an error message with exception details
    """
    try:
        payload = json.loads(msg.payload.decode())
        features = process_reading(payload)
        if features:
            save_to_csv(payload, features)
            print(f"💾 Saved: {features}")
    except Exception as e:
        print(f"⚠️ Error: {e}")

def start_mqtt():
    """
    Initialize and start the MQTT client connection.
    
    This function creates an MQTT client instance configured for the aqua-leak-backend,
    sets up connection and message handling callbacks, connects to the MQTT broker,
    and starts the client's network loop in a separate thread.
    
    Process:
    - Creates an MQTT client with client_id "aqua-leak-backend" using VERSION2 callback API
    - Registers on_connect callback to handle connection events
    - Registers on_message callback to handle incoming messages
    - Establishes connection to the MQTT broker at specified BROKER address and PORT
    - Starts the client's background network loop using loop_start() for non-blocking operation
    
    Returns:
        None
    
    Raises:
        ConnectionRefusedError: If unable to connect to the MQTT broker
        OSError: If network connection fails
    
    Note:
        The client loop runs in a separate daemon thread, allowing the main program
        to continue execution while listening for MQTT messages asynchronously.
    """
    client = mqtt.Client(
        client_id="aqua-leak-backend",
        callback_api_version=mqtt.CallbackAPIVersion.VERSION2
    )
    client.on_connect = on_connect
    client.on_message = on_message
    client.connect(BROKER, PORT)
    client.loop_start()