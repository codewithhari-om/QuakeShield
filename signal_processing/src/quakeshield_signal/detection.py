
import numpy as np
from obspy.signal.trigger import classic_sta_lta, trigger_onset

from .preprocessing import validate_signal


def detect_candidates(
    signal,
    sampling_rate,
    sta_seconds=0.5,
    lta_seconds=5.0,
    threshold_on=3.0,
    threshold_off=1.5
):
    """
    Detect candidate waveform disturbances using classic STA/LTA.

    A candidate is not proof of an earthquake or a P-wave arrival.
    """
    signal = validate_signal(signal, sampling_rate)

    if sta_seconds <= 0 or lta_seconds <= sta_seconds:
        raise ValueError("LTA must be longer than a positive STA.")

    if threshold_off < 0 or threshold_on <= threshold_off:
        raise ValueError("Threshold-on must exceed threshold-off.")

    nsta = int(round(sta_seconds * sampling_rate))
    nlta = int(round(lta_seconds * sampling_rate))

    if nsta < 1 or nlta <= nsta or nlta >= len(signal):
        raise ValueError("Waveform is too short for the chosen STA/LTA windows.")

    characteristic = classic_sta_lta(signal, nsta, nlta)

    intervals = trigger_onset(
        characteristic,
        threshold_on,
        threshold_off
    )

    return [
        {
            "start_sample": int(start),
            "end_sample": int(end),
            "start_time_seconds": float(start / sampling_rate),
            "end_time_seconds": float(end / sampling_rate),
        }
        for start, end in intervals
    ]
