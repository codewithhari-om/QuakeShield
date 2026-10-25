
from pathlib import Path
from obspy import read

from quakeshield_signal.phasenet_detector import PhaseNetDetector


def main():
    data_path = (
        Path(__file__).resolve().parents[1]
        / "data"
        / "real_waveform.mseed"
    )

    stream = read(str(data_path))

    detector = PhaseNetDetector()
    picks = detector.detect_phases(stream)

    print(f"\nTotal phase picks: {len(picks)}")

    for pick in picks:
        print(
            f"{pick['phase']} | "
            f"{pick['time_utc']} | "
            f"Confidence: {pick['confidence']:.3f} | "
            f"Trace: {pick['trace_id']}"
        )


if __name__ == "__main__":
    main()
