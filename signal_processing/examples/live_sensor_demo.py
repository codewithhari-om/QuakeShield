
from time import sleep

import numpy as np

from quakeshield_signal.pipeline import process_waveform


SAMPLE_RATE = 100
CHUNK_SECONDS = 10
CHUNK_SIZE = SAMPLE_RATE * CHUNK_SECONDS


def generate_sensor_chunk(rng, elapsed_seconds):
    """Simulate ground-motion samples for development only."""
    signal = rng.normal(0, 0.02, CHUNK_SIZE)

    # Add a synthetic disturbance after 30 seconds.
    if 30 <= elapsed_seconds < 40:
        t = np.arange(CHUNK_SIZE) / SAMPLE_RATE
        signal += 0.5 * np.sin(2 * np.pi * 5 * t)

    return signal


def main():
    rng = np.random.default_rng(42)

    print("QuakeShield simulated live sensor")
    print("This is synthetic data, not real earthquake monitoring.\n")

    for elapsed in range(0, 60, CHUNK_SECONDS):
        chunk = generate_sensor_chunk(rng, elapsed)

        print(
            f"Received {len(chunk)} samples "
            f"at t={elapsed}s"
        )

        # A short chunk may not contain enough history for
        # the current STA/LTA detector. This first demo verifies
        # sample generation and the pipeline interface only.
        if len(chunk) > 0:
            print(
                f"  Mean: {np.mean(chunk):.5f}, "
                f"RMS: {np.sqrt(np.mean(chunk ** 2)):.5f}"
            )

        sleep(0.2)


if __name__ == "__main__":
    main()
