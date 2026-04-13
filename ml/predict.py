import os
import joblib
import pandas as pd

BASE_DIR = os.path.dirname(os.path.dirname(__file__))
MODEL_FILE = os.path.join(BASE_DIR, "ml", "model.pk1")
SCALER_FILE = os.path.join(BASE_DIR, "ml", "scaler.pk1")

FEATURE_COLUMNS = [
    "rms",
    "dominant_freq",
    "peak_amplitude",
    "variance",
    "zero_crosiing_rate"
]

model = None
scaler = None

def load_artifacts():
    global model, scaler
    
    if model is None:
        model = joblib.load(MODEL_FILE)
    if scaler is None:
        scaler = joblib.load(SCALER_FILE)    
        
def predict_one(feature_dict):    
    load_artifacts()
    
    row = pd.DataFrame([feature_dict], columns=FEATURE_COLUMNS)
    X_scaled = scaler.transform(row)
    
    pred = int(model.predict(X_scaled)[0])
    score = float(model.score_samples(X_scaled)[0])
    
    return {
        "prediction": pred,
        "status": "Leak suspected" if pred == -1 else "Normal",
        "anomaly_score": score
    }