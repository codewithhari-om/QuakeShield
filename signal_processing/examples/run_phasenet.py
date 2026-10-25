
from pathlib import Path

from obspy import read
import seisbench.models as sbm


def main():
    data_path = (
        Path(__file__).resolve().parents[1]
        / "data"
        / "real_waveform.mseed"
    )

    print("Loading seismic recording...")
    stream = read(str(data_path))
    print(stream)

    print("\nLoading pretrained PhaseNet...")
    model = sbm.PhaseNet.from_pretrained("geofon")

    print("\nRunning PhaseNet...")
    output = model.classify(
        stream,
        P_threshold=0.3,
        S_threshold=0.3,
        strict=False,
    )

    picks = output.picks

    print(f"\nTotal phase picks: {len(picks)}")

    for pick in picks:
        print(
            f"Phase: {pick.phase} | "
            f"Time: {pick.peak_time} | "
            f"Confidence: {pick.peak_value:.3f} | "
            f"Trace: {pick.trace_id}"
        )

    if not picks:
        print("No phase picks exceeded the configured thresholds.")

    print("\nPhaseNet test complete.")
    print("Predictions require validation against known arrivals.")


if __name__ == "__main__":
    main()
