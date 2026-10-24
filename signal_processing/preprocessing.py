import numpy as np
from scipy.signal import butter, sosfiltfilt


def remove_mean(signal):
    signal = np.asarray(signal, dtype=float)

    if signal.size == 0:
        raise ValueError("Signal cannot be empty.")

    if not np.all(np.isfinite(signal)):
        raise ValueError("Signal must contain finite values.")

    return signal - np.mean(signal)


def normalize_signal(signal):
    signal = np.asarray(signal, dtype=float)

    if signal.size == 0:
        raise ValueError("Signal cannot be empty.")

    if not np.all(np.isfinite(signal)):
        raise ValueError("Signal must contain finite values.")

    max_value = np.max(np.abs(signal))

    if max_value == 0:
        return signal.copy()

    return signal / max_value


def bandpass_filter(signal, sampling_rate, low_cutoff, high_cutoff):
    signal = np.asarray(signal, dtype=float)

    if signal.size < 2:
        raise ValueError("Signal must contain at least two samples.")

    if not np.all(np.isfinite(signal)):
        raise ValueError("Signal must contain finite values.")

    if sampling_rate <= 0:
        raise ValueError("Sampling rate must be positive.")

    if not 0 < low_cutoff < high_cutoff < sampling_rate / 2:
        raise ValueError("Invalid cutoff frequencies.")

    sos = butter(
        4,
        [low_cutoff, high_cutoff],
        btype="bandpass",
        fs=sampling_rate,
        output="sos"
    )

    return sosfiltfilt(sos, signal)
