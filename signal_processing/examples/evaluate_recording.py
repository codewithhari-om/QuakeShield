
from pathlib import Path
import csv

import numpy as np
import matplotlib.pyplot as plt
from obspy import read

from quakeshield_signal.preprocessing import bandpass_filter
from quakeshield_signal.detection import detect_candidates
from quakeshield_signal.features import extract_event_features


# 1. Load the saved real recording
base_dir = Path(__file__).resolve().parents[1]
data_path = base_dir / "data" / "real_waveform.mseed"

stream = read(str(data_path))
trace = max(stream, key=lambda tr: tr.stats.npts)

signal = np.asarray(trace.data, dtype=np.float64)
sampling_rate = float(trace.stats.sampling_rate)

print("Recording:", trace.id)
print("Start UTC:", trace.stats.starttime)
print("Sampling rate:", sampling_rate, "Hz")
print("Samples:", len(signal))
print("Duration:", len(signal) / sampling_rate, "seconds")

if not np.all(np.isfinite(signal)):
    raise ValueError("Recording contains non-finite samples.")

# 2. Remove the mean and filter the complete recording
centered = signal - np.mean(signal)

high_cutoff = min(10.0, 0.4 * sampling_rate)

filtered = bandpass_filter(
    centered,
    sampling_rate,
    low_cutoff=0.5,
    high_cutoff=high_cutoff,
)

# 3. Detect candidate intervals
candidates = detect_candidates(filtered, sampling_rate)

print("\nNumber of candidates:", len(candidates))

# 4. Extract features for each candidate
features = extract_event_features(
    filtered,
    sampling_rate,
    candidates,
) if candidates else []

# 5. Save candidate times and features to CSV
csv_path = base_dir / "data" / "candidate_results.csv"
csv_path.parent.mkdir(parents=True, exist_ok=True)

with csv_path.open("w", newline="", encoding="utf-8") as file:
    writer = csv.writer(file)
    writer.writerow([
        "start_seconds",
        "end_seconds",
        "start_utc",
        "end_utc",
        "duration_seconds",
        "peak_amplitude",
        "rms_amplitude",
    ])

    for candidate, feature in zip(candidates, features):
        start_s = candidate["start_time_seconds"]
        end_s = candidate["end_time_seconds"]

        writer.writerow([
            start_s,
            end_s,
            str(trace.stats.starttime + start_s),
            str(trace.stats.starttime + end_s),
            end_s - start_s,
            feature.get("peak_amplitude", ""),
            feature.get("rms_amplitude", ""),
        ])

print("Results saved to:", csv_path)

# 6. Plot the entire filtered recording
time = np.arange(len(filtered)) / sampling_rate

plt.figure(figsize=(14, 6))
plt.plot(time, filtered, linewidth=0.7, label="Filtered waveform")

for i, candidate in enumerate(candidates):
    plt.axvspan(
        candidate["start_time_seconds"],
        candidate["end_time_seconds"],
        alpha=0.2,
        label="STA/LTA candidate" if i == 0 else None,
    )

plt.xlabel("Seconds from trace start")
plt.ylabel("Filtered counts")
plt.title("QuakeShield — Full Recording Candidate Evaluation")
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.show()
