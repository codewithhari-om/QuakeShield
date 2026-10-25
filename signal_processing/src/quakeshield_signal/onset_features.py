
import numpy as np


def extract_onset_features(
    signal,
    sampling_rate,
    start_sample,
    end_sample,
    noise_window_seconds=5.0,
):
    """
    Extract onset and frequency features for a detected candidate.

    These measurements describe the waveform; they do not
    confirm that a candidate is an earthquake or P-wave.
    """

    signal = np.asarray(signal, dtype=np.float64)

    if signal.ndim != 1 or signal.size == 0:
        raise ValueError("Signal must be a non-empty 1D array.")

    if not np.all(np.isfinite(signal)):
        raise ValueError("Signal must contain only finite values.")

    if not np.isfinite(sampling_rate) or sampling_rate <= 0:
        raise ValueError("Sampling rate must be positive and finite.")

    if not (
        isinstance(start_sample, (int, np.integer))
        and isinstance(end_sample, (int, np.integer))
        and 0 <= start_sample < end_sample <= len(signal)
    ):
        raise ValueError("Invalid candidate sample bounds.")

    if not np.isfinite(noise_window_seconds) or noise_window_seconds <= 0:
        raise ValueError("Noise window must be positive and finite.")

    candidate = signal[start_sample:end_sample]
    window_samples = int(round(noise_window_seconds * sampling_rate))
    noise_start = max(0, start_sample - window_samples)
    noise = signal[noise_start:start_sample]

    if len(candidate) < 4:
        raise ValueError("Candidate must contain at least 4 samples.")

    if len(noise) < 4:
        raise ValueError("Not enough preceding samples for comparison.")

    # Remove DC offsets before analyzing the waveform.
    candidate = candidate - np.mean(candidate)
    noise = noise - np.mean(noise)

    # Calculate RMS energy in the first and last portions
    # of the candidate to measure how abruptly energy rises.
    window_size = max(2, len(candidate) // 4)
    first_window = candidate[:window_size]
    last_window = candidate[-window_size:]

    first_rms = float(np.sqrt(np.mean(first_window ** 2)))
    last_rms = float(np.sqrt(np.mean(last_window ** 2)))
    onset_ratio = last_rms / max(first_rms, np.finfo(float).eps)

    # Frequency-domain features using a Hann window.
    windowed = candidate * np.hanning(len(candidate))
    spectrum = np.abs(np.fft.rfft(windowed)) ** 2
    frequencies = np.fft.rfftfreq(
        len(windowed),
        d=1.0 / sampling_rate,
    )

    total_power = float(np.sum(spectrum))

    if total_power <= np.finfo(float).eps:
        dominant_frequency = 0.0
        spectral_centroid = 0.0
        spectral_bandwidth = 0.0
    else:
        dominant_frequency = float(
            frequencies[np.argmax(spectrum)]
        )
        spectral_centroid = float(
            np.sum(frequencies * spectrum) / total_power
        )
        spectral_bandwidth = float(
            np.sqrt(
                np.sum(
                    ((frequencies - spectral_centroid) ** 2)
                    * spectrum
                ) / total_power
            )
        )

    noise_rms = float(np.sqrt(np.mean(noise ** 2)))
    candidate_rms = float(np.sqrt(np.mean(candidate ** 2)))

    return {
        "onset_ratio": float(onset_ratio),
        "first_window_rms": first_rms,
        "last_window_rms": last_rms,
        "noise_rms": noise_rms,
        "candidate_rms": candidate_rms,
        "dominant_frequency_hz": dominant_frequency,
        "spectral_centroid_hz": spectral_centroid,
        "spectral_bandwidth_hz": spectral_bandwidth,
    }
