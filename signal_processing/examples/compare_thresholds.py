
from pathlib import Path

import numpy as np
from obspy import UTCDateTime, read

from quakeshield_signal.preprocessing import remove_mean, bandpass_filter
from quakeshield_signal.detection import detect_candidates


# Load the existing recording
trace = max(read("data/real_waveform.mseed"), key=lambda tr: tr.stats.npts)
fs = trace.stats.sampling_rate

signal = remove_mean(trace.data.astype(np.float64))
filtered = bandpass_filter(
    signal,
    fs,
    0.5,
    min(10.0, 0.4 * fs),
)

# Theoretical P arrival, converted to recording-relative time
recording_start = trace.stats.starttime
origin_time = UTCDateTime("2010-05-24T16:18:29.090000Z")
predicted_p = (
    origin_time + 510.84 - recording_start
)

print(f"Predicted P arrival: {predicted_p:.2f} s after recording start")
print(f"Sampling rate: {fs} Hz")
print("-" * 72)

settings = [
    (0.5, 5.0, 2.5, 1.2),
    (0.5, 5.0, 3.0, 1.5),
    (0.5, 5.0, 4.0, 2.0),
    (0.5, 5.0, 5.0, 2.5),
]

for sta, lta, on, off in settings:
    try:
        candidates = detect_candidates(
            filtered,
            fs,
            sta_seconds=sta,
            lta_seconds=lta,
            threshold_on=on,
            threshold_off=off,
        )

        # Candidates beginning within 10 seconds of predicted P arrival
        nearby = [
            c for c in candidates
            if abs(c["start_time_seconds"] - predicted_p) <= 10
        ]

        earlier = [
            c for c in candidates
            if c["end_time_seconds"] < predicted_p - 10
        ]

        print(
            f"\nSTA/LTA thresholds: ON={on}, OFF={off}"
        )
        print(f"Total candidate intervals: {len(candidates)}")
        print(f"Earlier candidate intervals (>10 s before P): {len(earlier)}")

        if nearby:
            closest = min(
                nearby,
                key=lambda c: abs(c["start_time_seconds"] - predicted_p),
            )
            latency = closest["start_time_seconds"] - predicted_p

            print(
                "Closest candidate: "
                f"{closest['start_time_seconds']:.2f}–"
                f"{closest['end_time_seconds']:.2f} s"
            )
            print(f"Onset difference from theoretical P: {latency:+.2f} s")
        else:
            print("No candidate within 10 seconds of predicted P arrival.")

    except Exception as exc:
        print(f"\nON={on}, OFF={off}: ERROR: {exc}")

print("\nNote: earlier candidates are potential false alarms, not confirmed ones.")
print("This comparison alone does not establish P-wave detection accuracy.")

