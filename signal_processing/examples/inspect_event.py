
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
from obspy import read

from quakeshield_signal.preprocessing import (
    remove_mean,
    bandpass_filter,
)
from quakeshield_signal.detection import detect_candidates


# 1. Load the saved real seismic recording
data_path = (
    Path(__file__).resolve().parents[1]
    / "data"
    / "real_waveform.mseed"
)

stream = read(str(data_path))
trace = max(stream, key=lambda item: item.stats.npts)

sampling_rate = float(trace.stats.sampling_rate)
raw_signal = np.asarray(trace.data, dtype=np.float64)

print("Recording:", trace.id)
print("Sampling rate:", sampling_rate, "Hz")
print("Total samples:", len(raw_signal))


# 2. Select a 40-second inspection window
event_time = 512.0
window_before = 20.0
window_after = 20.0

start = max(
    0,
    int((event_time - window_before) * sampling_rate),
)
end = min(
    len(raw_signal),
    int((event_time + window_after) * sampling_rate),
)

raw_segment = raw_signal[start:end]
time = np.arange(start, end) / sampling_rate

if len(raw_segment) < 2:
    raise ValueError("Selected waveform segment is too short.")

if not np.all(np.isfinite(raw_segment)):
    raise ValueError("Selected waveform contains invalid values.")


# 3. Remove the mean and filter the selected segment
centered_segment = remove_mean(raw_segment)

high_cutoff = min(10.0, 0.4 * sampling_rate)

filtered_segment = bandpass_filter(
    centered_segment,
    sampling_rate,
    low_cutoff=0.5,
    high_cutoff=high_cutoff,
)


# 4. Detect candidate disturbances in the filtered segment
candidates = detect_candidates(
    filtered_segment,
    sampling_rate,
)

print("\nCandidates in inspection window:")

if candidates:
    for candidate in candidates:
        absolute_start = time[0] + candidate["start_time_seconds"]
        absolute_end = time[0] + candidate["end_time_seconds"]

        print(
            f"Start: {absolute_start:.2f} s, "
            f"End: {absolute_end:.2f} s, "
            f"Duration: "
            f"{candidate['end_time_seconds'] - candidate['start_time_seconds']:.2f} s"
        )
else:
    print("No candidate intervals detected.")


# 5. Plot raw and filtered waveforms
fig, axes = plt.subplots(
    2,
    1,
    figsize=(13, 8),
    sharex=True,
)

axes[0].plot(
    time,
    raw_segment,
    linewidth=0.8,
    label="Raw waveform",
)
axes[0].set_title("Raw seismic waveform")
axes[0].set_ylabel("Recorded counts")
axes[0].grid(True)
axes[0].legend()

axes[1].plot(
    time,
    filtered_segment,
    linewidth=0.8,
    label="Filtered waveform",
)
axes[1].set_title("Mean-removed and bandpass-filtered waveform")
axes[1].set_xlabel("Time from recording start (seconds)")
axes[1].set_ylabel("Filtered counts")
axes[1].grid(True)

# Mark the approximate reference time
for ax in axes:
    ax.axvline(
        event_time,
        linestyle="--",
        label="Approximate reference time",
    )

# Shade the detected candidate intervals
for i, candidate in enumerate(candidates):
    absolute_start = (
        time[0] + candidate["start_time_seconds"]
    )
    absolute_end = (
        time[0] + candidate["end_time_seconds"]
    )

    axes[1].axvspan(
        absolute_start,
        absolute_end,
        alpha=0.25,
        color="orange",
        label="STA/LTA candidate" if i == 0 else None,
    )

axes[1].legend()

plt.tight_layout()
plt.show()
