import numpy as np
from scipy.signal import butter, filtfilt,welch
from processing.feature_extractor import extract_features


SAMPLING_RATE = 1000 

def bandpass_filter(data, lowcut=5, highcut=300, fs=SAMPLING_RATE):
    b, a = butter(4, [lowcut, highcut], btype='band', fs=fs)
    return filtfilt(b, a, data)

def compute_rms(data):
    return np.sqrt(np.mean(np.array(data)**2))

def compute_fft_features(data):
    freqs, psd = welch(data, fs=SAMPLING_RATE)
    dominant_freq = freqs[np.argmax(psd)]
    return {
        "dominant_freq": round(float(dominant_freq), 4),
        "rms": round(float(compute_rms(data)), 6)
    }


def process_reading(payload):
    raw = payload.get("vibration_data", [])
    if not raw or len(raw) < 10:
        print("⚠️ Not enough data points")
        return None

    filtered = bandpass_filter(raw)
    dominant_freq, rms = compute_fft_features(filtered).values()
    features = extract_features(filtered, dominant_freq, rms)
    return features