
from pathlib import Path
import csv

import numpy as np
import matplotlib.pyplot as plt
from obspy import read

from quakeshield_signal.pipeline import process_waveform


# 1. Load the real seismic recording
base_dir = Path(__file__).resolve().parents[1]
data_path = base_dir / "data" / "real_waveform.mseed"

if not data_path.exists():
    raise FileNotFoundError(f"Recording not found: {data_path}")

stream = read(str(data_path))
trace = max(stream, key=lambda tr: tr.stats.npts)

signal = np.asarray(trace.data, dtype=np.float64)
sampling_rate = float(trace.stats.sampling_rate)

print("Recording:", trace.id)
print("Start UTC:", trace.stats.starttime)
print("Sampling rate:", sampling_rate, "Hz")
print("Samples:", len(signal))
print("Duration:", len(signal) / sampling_rate, "seconds")

# 2. Process the recording using the integrated pipeline
result = process_waveform(
    signal,
    sampling_rate,
    low_cutoff=0.5,
    high_cutoff=min(10.0, 0.4 * sampling_rate),
)

filtered = result["filtered_signal"]
ranked_candidates = result["ranked_candidates"]

print("\nNumber of candidates:", len(ranked_candidates))
print("\nTop 10 candidates by heuristic score:")


for rank, candidate in enumerate(ranked_candidates[:10], start=1):
    onset = candidate["onset_features"] or {}

    print(
        f"{rank:2}. "
        f"{candidate['start_time_seconds']:.2f}-"
        f"{candidate['end_time_seconds']:.2f} s | "
        f"Score: {candidate['score']:.1f}/100 | "
        f"Priority: {candidate['priority']} | "
        f"Dominant frequency: "
        f"{onset.get('dominant_frequency_hz', float('nan')):.2f} Hz | "
        f"Spectral centroid: "
        f"{onset.get('spectral_centroid_hz', float('nan')):.2f} Hz | "
        f"Onset ratio: "
        f"{onset.get('onset_ratio', float('nan')):.2f} | "
        f"Flags: {candidate['quality']['quality_flags']}"
    )


# 3. Save scored candidates to CSV
csv_path = base_dir / "data" / "ranked_candidate_results.csv"
csv_path.parent.mkdir(parents=True, exist_ok=True)

with csv_path.open("w", newline="", encoding="utf-8") as file:
    fieldnames = [
        "rank",
        "start_seconds",
        "end_seconds",
        "start_utc",
        "end_utc",
        "duration_seconds",
        "peak_amplitude",
        "rms_amplitude",
        "noise_rms",
        "candidate_rms",
        "amplitude_ratio",
        "score",
        "priority",
        "quality_flags",
        "score_reasons",
    ]

    writer = csv.DictWriter(file, fieldnames=fieldnames)
    writer.writeheader()

    for rank, candidate in enumerate(ranked_candidates, start=1):
        feature = candidate["features"]
        quality = candidate["quality"]

        start_s = candidate["start_time_seconds"]
        end_s = candidate["end_time_seconds"]

        writer.writerow({
            "rank": rank,
            "start_seconds": start_s,
            "end_seconds": end_s,
            "start_utc": str(trace.stats.starttime + start_s),
            "end_utc": str(trace.stats.starttime + end_s),
            "duration_seconds": feature["duration_seconds"],
            "peak_amplitude": feature["peak_amplitude"],
            "rms_amplitude": feature["rms_amplitude"],
            "noise_rms": quality["noise_rms"],
            "candidate_rms": quality["candidate_rms"],
            "amplitude_ratio": quality["amplitude_ratio"],
            "score": candidate["score"],
            "priority": candidate["priority"],
            "quality_flags": "; ".join(quality["quality_flags"]),
            "score_reasons": "; ".join(candidate["score_reasons"]),
        })

print("\nRanked results saved to:", csv_path)

# 4. Plot the filtered waveform and candidate intervals
time = np.arange(len(filtered)) / sampling_rate

plt.figure(figsize=(14, 6))
plt.plot(time, filtered, linewidth=0.7, label="Filtered waveform")

for i, candidate in enumerate(ranked_candidates):
    plt.axvspan(
        candidate["start_time_seconds"],
        candidate["end_time_seconds"],
        alpha=0.18,
        label="STA/LTA candidate" if i == 0 else None,
    )

plt.xlabel("Seconds from trace start")
plt.ylabel("Filtered counts")
plt.title("QuakeShield — Ranked Candidate Evaluation")
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.show()
