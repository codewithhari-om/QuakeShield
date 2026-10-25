
import csv
from pathlib import Path

output = Path("data/threshold_comparison.csv")
output.parent.mkdir(parents=True, exist_ok=True)

rows = [
    [2.5, 1.2, 100, 86, 0.29],
    [3.0, 1.5, 65, 55, 0.29],
    [4.0, 2.0, 18, 12, 0.34],
    [5.0, 2.5, 4, 1, 0.34],
]

with output.open("w", newline="", encoding="utf-8") as f:
    writer = csv.writer(f)
    writer.writerow([
        "threshold_on",
        "threshold_off",
        "total_candidates",
        "earlier_candidates_unverified",
        "arrival_difference_seconds",
    ])
    writer.writerows(rows)

print(f"Saved preliminary results to: {output}")
print("These results are exploratory, not a validated performance benchmark.")
