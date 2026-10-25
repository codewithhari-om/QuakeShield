
from pathlib import Path
import csv
from collections import Counter

import numpy as np

base_dir = Path(__file__).resolve().parents[1]
csv_path = base_dir / "data" / "candidate_results.csv"

if not csv_path.exists():
    raise FileNotFoundError(
        f"Results not found: {csv_path}\n"
        "Run examples/evaluate_recording.py first."
    )

with csv_path.open(newline="", encoding="utf-8") as file:
    rows = list(csv.DictReader(file))

if not rows:
    print("No candidates found in the CSV.")
    raise SystemExit(0)

durations = np.array(
    [float(row["duration_seconds"]) for row in rows]
)
peaks = np.array(
    [float(row["peak_amplitude"]) for row in rows]
)
rms = np.array(
    [float(row["rms_amplitude"]) for row in rows]
)
starts = np.array(
    [float(row["start_seconds"]) for row in rows]
)

print("\n=== QuakeShield Detection Summary ===")
print("Total candidate intervals:", len(rows))
print(f"First candidate: {starts.min():.2f} seconds")
print(f"Last candidate:  {starts.max():.2f} seconds")
print(f"Median duration: {np.median(durations):.2f} seconds")
print(f"Maximum duration: {durations.max():.2f} seconds")
print(f"Median peak amplitude: {np.median(peaks):.2f}")
print(f"Maximum peak amplitude: {peaks.max():.2f}")
print(f"Median RMS amplitude: {np.median(rms):.2f}")

print("\n=== Largest 5 Candidates by Peak Amplitude ===")
for row in sorted(
    rows,
    key=lambda item: float(item["peak_amplitude"]),
    reverse=True,
)[:5]:
    print(
        f'{row["start_seconds"]}–{row["end_seconds"]} s | '
        f'peak={float(row["peak_amplitude"]):.2f} | '
        f'RMS={float(row["rms_amplitude"]):.2f} | '
        f'duration={float(row["duration_seconds"]):.2f} s'
    )

print("\nThis report describes triggers; it does not classify")
print("earthquakes or confirm P-wave arrivals.")
