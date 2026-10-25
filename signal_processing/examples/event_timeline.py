
from pathlib import Path
import csv

base_dir = Path(__file__).resolve().parents[1]
input_path = base_dir / "data" / "candidate_results.csv"
output_path = base_dir / "data" / "event_timeline.csv"

with input_path.open(
    newline="",
    encoding="utf-8",
) as file:
    rows = list(csv.DictReader(file))

if not rows:
    print("No candidates found.")
    raise SystemExit(0)

rows.sort(key=lambda row: float(row["start_seconds"]))

# Merge candidates separated by no more than this interval.
# This is a grouping choice for inspection, not earthquake classification.
gap_seconds = 5.0
groups = []
current_group = [rows[0]]

for row in rows[1:]:
    previous_end = float(current_group[-1]["end_seconds"])
    current_start = float(row["start_seconds"])

    if current_start - previous_end <= gap_seconds:
        current_group.append(row)
    else:
        groups.append(current_group)
        current_group = [row]

groups.append(current_group)

with output_path.open(
    "w",
    newline="",
    encoding="utf-8",
) as file:
    fields = [
        "group_id",
        "start_seconds",
        "end_seconds",
        "duration_seconds",
        "candidate_count",
        "maximum_peak_amplitude",
    ]
    writer = csv.DictWriter(file, fieldnames=fields)
    writer.writeheader()

    print("\n=== Candidate Activity Groups ===")

    for group_id, group in enumerate(groups, start=1):
        start = float(group[0]["start_seconds"])
        end = max(float(item["end_seconds"]) for item in group)
        maximum_peak = max(
            float(item["peak_amplitude"]) for item in group
        )

        result = {
            "group_id": group_id,
            "start_seconds": round(start, 3),
            "end_seconds": round(end, 3),
            "duration_seconds": round(end - start, 3),
            "candidate_count": len(group),
            "maximum_peak_amplitude": round(maximum_peak, 3),
        }

        writer.writerow(result)
        print(result)

print(f"\nSaved timeline: {output_path}")
print(
    "\nGroups represent nearby triggers only; "
    "they are not confirmed earthquake events."
)
