# test_local.py
from processing.signal_processor import process_reading
from processing.feature_extractor import extract_features
import numpy as np

# Simulate what Karma's ESP32 would send
fake_payload = {
    "device_id": "pipe_01",
    "vibration_data": list(np.random.normal(0, 0.5, 1000))  # 1000 sample points
}

print("Testing signal processor...")
features = process_reading(fake_payload)
print(f"✅ Features: {features}")