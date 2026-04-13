import numpy as np

def extract_features(filtered_signal, dominant_freq, rms):
    signal = np.array(filtered_signal)

    return {
        "rms": rms,
        "dominant_freq": dominant_freq,
        "peak_amplitude": float(np.max(np.abs(signal))),
        "variance": float(np.var(signal)),
        "zero_crossing_rate": float(
            np.sum(np.diff(np.sign(signal)) != 0) / len(signal)
        )
    }