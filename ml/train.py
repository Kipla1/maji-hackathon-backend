import os
import joblib
import pandas as pd
from sklearn.ensemble import IsolationForest
from sklearn.preprocessing import StandardScaler

BASE_DIR = os.path.dirname(os.path.dirname(__file__))
DATA_FILE = os.path.join(BASE_DIR, "data", "readings.csv")
MODEL_FILE =os.path.join(BASE_DIR, "ml", "model.pk1")
SCALER_FILE = os.path.join(BASE_DIR, "ml", "scalar.pk1")

FEATURE_COLUMNS =[
    "rms",
    "dominant_freq",
    "peak_amplitude",
    "variance",
    "zero_crossing_rate"
]

def train_model():
    if not os.path.isfile(DATA_FILE):
        raise FileNotFoundError(f"Dataset not found: {DATA_FILE}")
    
    df = pd.read_csv(DATA_FILE)
    missing = [col for col in FEATURE_COLUMNS if col not in df.columns]
    if missing:
        raise ValueError(f"Missing required column: {missing}")
    
    df = df.dropna(subset=FEATURE_COLUMNS)
    if len(df) < 20:
        raise ValueError("Need at least 20 rows to start training.")
    
    X = df[FEATURE_COLUMNS]
    
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)
    
    model = IsolationForest(
        n_estimators=100,
        contamination=0.1,
        random_state=42,
        n_jobs=-1
    )
    
    joblib.dump(model, MODEL_FILE)
    joblib.dump(scaler, SCALER_FILE)
    
    return {
        "rows_used": len(df),
        "model_path": MODEL_FILE,
        "scaler_path": SCALER_FILE
    }
    
if __name__ == "__main__":
    result = train_model()
    print(result)