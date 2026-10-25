
from pathlib import Path
import csv

base_dir = Path(__file__).resolve().parents[1]
input_path = base_dir / "data" / "candidate_results.csv"
output_path = base_dir / "data" / "ranked_candidates.csv"

if not input_path.exists():
    raise FileNotFoundError(
        f"Candidate results not found: {input_path}"
    )

with input_path.open(
    newline="",
    encoding="utf-8",
) as file:
    rows = list(csv.DictReader(file))

rows.sort(
    key=lambda row: float(row["peak_amplitude"]),
    reverse=True,
)

if rows:
    fieldnames = list(rows[0].keys())
    fieldnames.append("rank")

    with output_path.open(
        "w",
        newline="",
        encoding="utf-8",
    ) as file:
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()

        for rank, row in enumerate(rows, start=1):
            row["rank"] = rank
            writer.writerow(row)

print("Candidates ranked:", len(rows))
print("Saved report:", output_path)

print("\nTop 10 candidates by peak amplitude:")
for rank, row in enumerate(rows[:10], start=1):
    print(
        f'{rank:2}. {row["start_seconds"]}–'
        f'{row["end_seconds"]} s | '
        f'Peak: {float(row["peak_amplitude"]):.2f} | '
        f'RMS: {float(row["rms_amplitude"]):.2f}'
    )

print(
    "\nRanking is based only on filtered signal amplitude; "
    "it does not confirm seismic event type."
)
