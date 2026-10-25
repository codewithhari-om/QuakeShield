
import numpy as np
from obspy import Trace


def validate_signal(signal, sampling_rate):
    """Validate a one-dimensional waveform and its sampling rate."""
    signal = np.asarray(signal, dtype=np.float64)

    if signal.ndim != 1 or signal.size < 2:
        raise ValueError("Signal must be a 1D array with at least 2 samples.")

    if not np.all(np.isfinite(signal)):
        raise ValueError("Signal contains invalid values.")

    if sampling_rate <= 0:
        raise ValueError("Sampling rate must be positive.")

    return signal


def remove_mean(signal):
    """Remove the constant offset from a waveform."""
    signal = np.asarray(signal, dtype=np.float64)

    if signal.size == 0 or not np.all(np.isfinite(signal)):
        raise ValueError("Signal must be non-empty and finite.")

    return signal - np.mean(signal)


def bandpass_filter(signal, sampling_rate, low_cutoff, high_cutoff):
    """Apply a causal Butterworth bandpass filter to a waveform."""
    signal = validate_signal(signal, sampling_rate)
    nyquist = sampling_rate / 2

    if not 0 < low_cutoff < high_cutoff < nyquist:
        raise ValueError("Cutoffs must satisfy 0 < low < high < Nyquist.")

    trace = Trace(data=signal.copy())
    trace.stats.sampling_rate = sampling_rate

    trace.filter(
        "bandpass",
        freqmin=low_cutoff,
        freqmax=high_cutoff,
        corners=4,
        zerophase=False
    )

    return trace.data
