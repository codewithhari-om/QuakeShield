
import numpy as np
import matplotlib.pyplot as plt

from quakeshield_signal.features import extract_event_features
from quakeshield_signal.preprocessing import bandpass_filter
from quakeshield_signal.detection import detect_candidates


# 1. Generate a synthetic waveform
sampling_rate = 100.0
duration = 60.0

time = np.arange(int(sampling_rate * duration)) / sampling_rate

rng = np.random.default_rng(42)
signal = rng.normal(0, 0.05, len(time))


# 2. Add an artificial waveform disturbance at 30 seconds
event_start = int(30 * sampling_rate)
event_end = int(35 * sampling_rate)

signal[event_start:event_end] += (
    0.5
    * np.sin(
        2 * np.pi * 5 * time[event_start:event_end]
    )
)


# 3. Apply the bandpass filter
filtered = bandpass_filter(
    signal,
    sampling_rate,
    low_cutoff=1.0,
    high_cutoff=15.0,
)


# 4. Detect candidate disturbances
candidates = detect_candidates(
    filtered,
    sampling_rate,
)


# 5. Print detection results and event features
print("Candidate intervals:")

if candidates:
    for candidate in candidates:
        print(candidate)

    features = extract_event_features(
        filtered,
        sampling_rate,
        candidates,
    )

    print("\nEvent features:")

    for feature in features:
        print(feature)
else:
    print("No candidate intervals detected.")


# 6. Plot the filtered waveform and detected intervals
plt.figure(figsize=(12, 5))

plt.plot(
    time,
    filtered,
    linewidth=0.8,
    label="Filtered waveform",
)

for i, candidate in enumerate(candidates):
    start_time = candidate["start_time_seconds"]
    end_time = candidate["end_time_seconds"]

    plt.axvspan(
        start_time,
        end_time,
        alpha=0.25,
        label="Detected candidate" if i == 0 else None,
    )

plt.xlabel("Time (seconds)")
plt.ylabel("Amplitude (synthetic units)")
plt.title("QuakeShield - Waveform and Detected Candidates")
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.show()
