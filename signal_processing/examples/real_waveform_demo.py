
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
from obspy import UTCDateTime, read
from obspy.clients.fdsn import Client

from quakeshield_signal.pipeline import process_waveform


# 1. Select a historical seismic recording.
# IU.ANMO.00.BHZ is the station/channel identifier.
client = Client("EARTHSCOPE")

start_time = UTCDateTime("2010-05-24T16:18:28")
end_time = start_time + 600  # Request 10 minutes.

print("Downloading real seismic waveform...")

stream = client.get_waveforms(
    network="IU",
    station="ANMO",
    location="00",
    channel="BHZ",
    starttime=start_time,
    endtime=end_time,
)

if len(stream) == 0:
    raise RuntimeError("No waveform data returned.")

# Merge compatible segments and inspect the recording.
stream.merge(method=1, fill_value="interpolate")
stream = stream.split()

if len(stream) == 0:
    raise RuntimeError("No usable waveform segments found.")

# Use the longest continuous segment.
trace = max(stream, key=lambda item: item.stats.npts)

print("\nSelected recording:")
print(trace)
print("Start time:", trace.stats.starttime)
print("Sampling rate:", trace.stats.sampling_rate, "Hz")
print("Number of samples:", trace.stats.npts)

# Save the downloaded waveform for future experiments.
data_dir = Path(__file__).resolve().parents[1] / "data"
data_dir.mkdir(parents=True, exist_ok=True)

waveform_path = data_dir / "real_waveform.mseed"
trace.write(str(waveform_path), format="MSEED")
print("Saved waveform to:", waveform_path)

# 2. Prepare samples for our existing pipeline.
signal = np.asarray(trace.data, dtype=np.float64)
sampling_rate = float(trace.stats.sampling_rate)

if not np.all(np.isfinite(signal)):
    raise ValueError("Recording contains invalid samples.")

# Keep the high cutoff safely below the Nyquist frequency.
low_cutoff = 0.5
high_cutoff = min(10.0, 0.4 * sampling_rate)

if high_cutoff <= low_cutoff:
    raise ValueError(
        "Sampling rate is too low for the selected filter."
    )

# 3. Process the real recording.
print("\nRunning QuakeShield pipeline...")

result = process_waveform(
    signal,
    sampling_rate,
    low_cutoff=low_cutoff,
    high_cutoff=high_cutoff,
)

print("\nCandidate intervals:")
if result["candidates"]:
    for candidate in result["candidates"]:
        print(candidate)
else:
    print("No candidates detected.")

print("\nExtracted features:")
for feature in result["features"]:
    print(feature)

# 4. Plot the processed waveform and candidates.
time = np.arange(len(signal)) / sampling_rate

plt.figure(figsize=(13, 5))
plt.plot(
    time,
    result["filtered_signal"],
    linewidth=0.7,
    label="Filtered seismic waveform",
)

for i, candidate in enumerate(result["candidates"]):
    plt.axvspan(
        candidate["start_time_seconds"],
        candidate["end_time_seconds"],
        alpha=0.25,
        label="Candidate" if i == 0 else None,
    )

plt.xlabel("Time from recording start (seconds)")
plt.ylabel("Amplitude (recorded counts, filtered)")
plt.title("QuakeShield — Real Seismic Recording Test")
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.show()
