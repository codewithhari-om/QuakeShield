from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
from obspy import UTCDateTime, read

from quakeshield_signal.detection import detect_candidates
from quakeshield_signal.preprocessing import bandpass_filter, remove_mean


DATA_FILE = Path("data/real_waveform.mseed")

# Catalog event information
origin_time = UTCDateTime("2010-05-24T16:18:29.090000Z")
predicted_p_travel_time = 510.84

# Candidate detected previously, in seconds from recording start
candidate_start_seconds = 512.2
candidate_end_seconds = 515.0

stream = read(str(DATA_FILE))
trace = max(stream, key=lambda tr: tr.stats.npts)

sampling_rate = trace.stats.sampling_rate
recording_start = trace.stats.starttime

signal = remove_mean(trace.data.astype(np.float64))
filtered = bandpass_filter(
    signal,
    sampling_rate,
    0.5,
    min(10.0, 0.4 * sampling_rate),
)

predicted_p_utc = origin_time + predicted_p_travel_time
predicted_p_recording_seconds = (
    predicted_p_utc - recording_start
)

print("Trace:", trace.id)
print("Recording start:", recording_start)
print("Predicted P arrival:", predicted_p_utc)
print(
    "Predicted P relative to recording start:",
    round(predicted_p_recording_seconds, 3),
    "seconds",
)
print(
    "Detected candidate:",
    candidate_start_seconds,
    "to",
    candidate_end_seconds,
    "seconds after recording start",
)

# Plot a 20-second window around the predicted arrival.
window_start = max(0.0, predicted_p_recording_seconds - 10.0)
window_end = min(
    len(filtered) / sampling_rate,
    predicted_p_recording_seconds + 10.0,
)

first = int(window_start * sampling_rate)
last = int(window_end * sampling_rate)

times = np.arange(first, last) / sampling_rate
times_utc = [
    recording_start + float(t)
    for t in times
]

fig, ax = plt.subplots(figsize=(12, 5))

ax.plot(times, filtered[first:last], linewidth=0.8)

ax.axvline(
    predicted_p_recording_seconds,
    linestyle="--",
    label="Theoretical P arrival",
)

ax.axvspan(
    candidate_start_seconds,
    candidate_end_seconds,
    alpha=0.2,
    label="Detected candidate",
)

ax.set_title("QuakeShield: Predicted P Arrival vs. Detected Signal")
ax.set_xlabel("Seconds after recording start")
ax.set_ylabel("Filtered amplitude (instrument counts)")
ax.grid(True, alpha=0.3)
ax.legend()

plt.tight_layout()
plt.show()