
import csv
from pathlib import Path

import numpy as np
from obspy import read

from quakeshield_signal.detection import detect_candidates
from quakeshield_signal.preprocessing import (
    remove_mean,
    bandpass_filter,
)

INPUT = Path("data/real_waveform.mseed")
OUTPUT = Path("data/streaming_events.csv")

CHUNK_SECONDS = 1.0
BUFFER_SECONDS = 10.0
MERGE_GAP_SECONDS = 5.0
THRESHOLD_ON = 4.0
THRESHOLD_OFF = 2.0

trace = max(read(str(INPUT)), key=lambda tr: tr.stats.npts)
fs = trace.stats.sampling_rate

# Offline replay: filtering is performed before chunk processing.
# Live deployment must preserve filter state between incoming chunks.
signal = remove_mean(trace.data.astype(np.float64))
filtered = bandpass_filter(
    signal,
    fs,
    0.5,
    min(10.0, 0.4 * fs),
)

chunk_size = max(1, int(round(CHUNK_SECONDS * fs)))
buffer_size = max(chunk_size, int(round(BUFFER_SECONDS * fs)))

rolling_buffer = []
detected_onsets = set()

for offset in range(0, len(filtered), chunk_size):
    chunk = filtered[offset:offset + chunk_size]
    chunk_start = offset / fs
    chunk_end = (offset + len(chunk)) / fs

    rolling_buffer.extend(chunk.tolist())
    if len(rolling_buffer) > buffer_size:
        rolling_buffer = rolling_buffer[-buffer_size:]

    current = np.asarray(rolling_buffer)

    # The LTA needs enough history before detection is meaningful.
    if len(current) < int(5.0 * fs) + 2:
        continue

    candidates = detect_candidates(
        current,
        fs,
        sta_seconds=0.5,
        lta_seconds=5.0,
        threshold_on=THRESHOLD_ON,
        threshold_off=THRESHOLD_OFF,
    )

    buffer_start = chunk_end - len(current) / fs

    for candidate in candidates:
        absolute_start = (
            buffer_start + candidate["start_time_seconds"]
        )

        # Assign each detected onset to the chunk in which it begins.
        # This avoids counting the same onset in every overlapping buffer.
        if chunk_start <= absolute_start < chunk_end:
            onset_key = round(absolute_start * fs)
            detected_onsets.add(onset_key)

# Convert unique onset samples into timestamps.
onsets = sorted(sample / fs for sample in detected_onsets)

# Group nearby onsets into candidate activity episodes.
events = []

for onset in onsets:
    if (
        not events
        or onset - events[-1]["last_onset"] > MERGE_GAP_SECONDS
    ):
        events.append({
            "start": onset,
            "last_onset": onset,
            "onset_count": 1,
        })
    else:
        events[-1]["last_onset"] = onset
        events[-1]["onset_count"] += 1

OUTPUT.parent.mkdir(parents=True, exist_ok=True)

with OUTPUT.open("w", newline="", encoding="utf-8") as file:
    writer = csv.DictWriter(
        file,
        fieldnames=[
            "event_id",
            "start_seconds",
            "last_onset_seconds",
            "onset_count",
        ],
    )
    writer.writeheader()

    for event_id, event in enumerate(events, start=1):
        writer.writerow({
            "event_id": event_id,
            "start_seconds": round(event["start"], 2),
            "last_onset_seconds": round(event["last_onset"], 2),
            "onset_count": event["onset_count"],
        })

print("QuakeShield deduplicated replay complete")
print("Samples:", len(filtered))
print("Chunks processed:", int(np.ceil(len(filtered) / chunk_size)))
print("Unique candidate onsets:", len(onsets))
print("Grouped activity episodes:", len(events))
print("CSV saved:", OUTPUT)

for i, event in enumerate(events, start=1):
    print(
        f"Episode {i}: {event['start']:.2f}–"
        f"{event['last_onset']:.2f} s; "
        f"{event['onset_count']} onset(s)"
    )

print("Exploratory offline results only; not validated warnings.")
