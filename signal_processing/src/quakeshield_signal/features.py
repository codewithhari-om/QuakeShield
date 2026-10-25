
import numpy as np


def extract_event_features(signal, sampling_rate, candidates):
    """
    Calculate basic features for detected waveform candidates.

    Features include peak amplitude, RMS amplitude, and duration.
    These features describe signal characteristics; they do not
    confirm that a candidate is an earthquake or a P-wave.
    """
    signal = np.asarray(signal, dtype=np.float64)

    # Validate the waveform
    if signal.ndim != 1 or signal.size == 0:
        raise ValueError("Signal must be a non-empty 1D array.")

    if not np.all(np.isfinite(signal)):
        raise ValueError("Signal must contain only finite values.")

    # Validate the sampling rate
    if not np.isfinite(sampling_rate) or sampling_rate <= 0:
        raise ValueError("Sampling rate must be positive and finite.")

    results = []

    for candidate in candidates:
        start = candidate["start_sample"]
        end = candidate["end_sample"]

        # Validate candidate boundaries
        if not isinstance(start, (int, np.integer)):
            raise ValueError("Candidate start_sample must be an integer.")

        if not isinstance(end, (int, np.integer)):
            raise ValueError("Candidate end_sample must be an integer.")

        if not (0 <= start < end <= len(signal)):
            raise ValueError("Candidate interval is outside the signal.")

        segment = signal[start:end]

        # Calculate features
        peak_amplitude = float(np.max(np.abs(segment)))
        rms_amplitude = float(np.sqrt(np.mean(segment ** 2)))
        duration = float((end - start) / sampling_rate)

        results.append({
            "start_time_seconds": float(
                candidate["start_time_seconds"]
            ),
            "end_time_seconds": float(
                candidate["end_time_seconds"]
            ),
            "duration_seconds": duration,
            "peak_amplitude": peak_amplitude,
            "rms_amplitude": rms_amplitude,
        })

    return results
