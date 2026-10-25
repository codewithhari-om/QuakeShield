
import numpy as np

from .pipeline import process_waveform


class RollingBufferProcessor:
    """Basic rolling-window processor for incoming sensor samples."""

    def __init__(
        self,
        sampling_rate=100,
        window_seconds=15,
        step_seconds=1,
        low_cutoff=1.0,
        high_cutoff=15.0,
    ):
        if sampling_rate <= 0:
            raise ValueError("Sampling rate must be positive.")
        if window_seconds <= 0 or step_seconds <= 0:
            raise ValueError("Window and step must be positive.")
        if step_seconds > window_seconds:
            raise ValueError("Step cannot exceed window.")

        self.sampling_rate = sampling_rate
        self.window_size = int(sampling_rate * window_seconds)
        self.step_size = int(sampling_rate * step_seconds)
        self.low_cutoff = low_cutoff
        self.high_cutoff = high_cutoff
        self.buffer = np.array([], dtype=np.float64)
        self.samples_since_process = 0

    def add_samples(self, samples):
        samples = np.asarray(samples, dtype=np.float64)

        if samples.ndim != 1:
            raise ValueError("Samples must be a one-dimensional array.")
        if not np.all(np.isfinite(samples)):
            raise ValueError("Samples must be finite.")

        self.buffer = np.concatenate((self.buffer, samples))
        self.samples_since_process += len(samples)

        # Keep only the most recent analysis window.
        if len(self.buffer) > self.window_size:
            self.buffer = self.buffer[-self.window_size:]

        if len(self.buffer) < self.window_size:
            return None

        if self.samples_since_process < self.step_size:
            return None

        self.samples_since_process %= self.step_size

        return process_waveform(
            self.buffer,
            self.sampling_rate,
            low_cutoff=self.low_cutoff,
            high_cutoff=self.high_cutoff,
        )
