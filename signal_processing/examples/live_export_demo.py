
from pathlib import Path
import time

import numpy as np

from quakeshield_signal.stream_processor import RollingBufferProcessor
from quakeshield_signal.event_output import (
    build_event_message,
    save_event_message,
)

SAMPLE_RATE = 100
CHUNK_SECONDS = 1
TOTAL_SECONDS = 40


def generate_sensor_chunk(rng, elapsed_seconds):
    """Generate simulated sensor samples for development."""
    chunk_size = SAMPLE_RATE * CHUNK_SECONDS
    t = elapsed_seconds + np.arange(chunk_size) / SAMPLE_RATE

    # Background sensor noise
    signal = rng.normal(0, 0.02, chunk_size)

    # Simulated disturbance between 20 and 24 seconds
    mask = (t >= 20) & (t < 24)
    signal[mask] += (
        0.3 * np.sin(2 * np.pi * 5 * t[mask])
    )

    return signal


def main():
    rng = np.random.default_rng(42)

    processor = RollingBufferProcessor(
        sampling_rate=SAMPLE_RATE,
        window_seconds=15,
        step_seconds=1,
        low_cutoff=1.0,
        high_cutoff=15.0,
    )

    output_path = (
        Path(__file__).resolve().parents[1]
        / "data"
        / "latest_event_message.json"
    )

    print("QuakeShield live export demo")
    print("Using SIMULATED sensor data, not real earthquake data.")
    print("Waiting for the first complete 15-second window...\n")

    for elapsed in range(0, TOTAL_SECONDS, CHUNK_SECONDS):
        chunk = generate_sensor_chunk(rng, elapsed)
        result = processor.add_samples(chunk)

        print(f"Received samples at t={elapsed}s")

        if result is not None:
            message = build_event_message(result)
            save_event_message(message, output_path)

            print(
                f"  Candidates: {message['candidate_count']}"
            )
            print(f"  JSON updated: {output_path.name}")

            if message["candidates"]:
                best = message["candidates"][0]
                print(
                    f"  Highest priority: {best['priority']} | "
                    f"Score: {best['score']}"
                )

            print()

        time.sleep(0.1)

    print("Demo finished.")
    print(f"Latest JSON file: {output_path}")


if __name__ == "__main__":
    main()
