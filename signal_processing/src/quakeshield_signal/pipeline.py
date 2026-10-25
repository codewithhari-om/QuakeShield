
from .preprocessing import (
    validate_signal,
    remove_mean,
    bandpass_filter,
)
from .detection import detect_candidates
from .features import extract_event_features


def process_waveform(
    signal,
    sampling_rate,
    low_cutoff=1.0,
    high_cutoff=15.0,
):
    """Preprocess a waveform, detect candidates, and extract features."""

    signal = validate_signal(signal, sampling_rate)
    centered_signal = remove_mean(signal)

    filtered_signal = bandpass_filter(
        centered_signal,
        sampling_rate,
        low_cutoff,
        high_cutoff,
    )

    candidates = detect_candidates(
        filtered_signal,
        sampling_rate,
    )

    features = extract_event_features(
        filtered_signal,
        sampling_rate,
        candidates,
    )

    return {
        "filtered_signal": filtered_signal,
        "candidates": candidates,
        "features": features,
        "sampling_rate": sampling_rate,
    }
