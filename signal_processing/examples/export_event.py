from pathlib import Path

from quakeshield_signal.pipeline import process_waveform
from quakeshield_signal.event_output import (
    build_event_message,
    save_event_message,
)

import numpy as np

SAMPLE_RATE = 100

def main():
    # Generate simulated sensor data
    rng = np.random.default_rng(42)
    signal = rng.normal(0, 0.02, SAMPLE_RATE * 15)

    # Add a simulated disturbance
    t = np.arange(len(signal)) / SAMPLE_RATE
    signal += 0.3 * np.sin(2 * np.pi * 5 * t) * (
        (t >= 8) & (t < 12)
    )

    # Process the waveform
    result = process_waveform(signal, SAMPLE_RATE)

    # Build a JSON-ready message
    message = build_event_message(result)

    # Save output
    output_path = (
        Path(__file__).resolve().parents[1]
        / "data"
        / "latest_event_message.json"
    )

    save_event_message(message, output_path)

    print("Analysis complete.")
    print(f"Candidates: {message['candidate_count']}")
    print(f"Output saved to: {output_path}")

    for event in message["candidates"][:5]:
        print(
            f"Time: {event['start_time_seconds']:.2f}s | "
            f"Score: {event['score']} | "
            f"Priority: {event['priority']}"
        )

if __name__ == "__main__":
    main()