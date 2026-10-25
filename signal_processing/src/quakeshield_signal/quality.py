
import numpy as np


def assess_signal_quality(
    signal,
    sampling_rate,
    candidate_start,
    candidate_end,
    clipping_limit=None,
    noise_window_seconds=5.0,
):
    """
    Assess waveform quality around a detected candidate.

    This function flags possible clipping, invalid data, and
    unusually large amplitude relative to preceding background noise.

    It does NOT confirm earthquakes or P-wave arrivals.
    """
    signal = np.asarray(signal, dtype=np.float64)

    result = {
        "valid": False,
        "clipped": None,
        "noise_rms": None,
        "candidate_rms": None,
        "amplitude_ratio": None,
        "quality_flags": [],
    }

    # Validate waveform
    if signal.ndim != 1 or signal.size == 0:
        result["quality_flags"].append("invalid_waveform_shape")
        return result

    if not np.isfinite(sampling_rate) or sampling_rate <= 0:
        result["quality_flags"].append("invalid_sampling_rate")
        return result

    if not np.all(np.isfinite(signal)):
        result["quality_flags"].append("non_finite_samples")
        return result

    if not (
        isinstance(candidate_start, (int, np.integer))
        and isinstance(candidate_end, (int, np.integer))
        and 0 <= candidate_start < candidate_end <= len(signal)
    ):
        result["quality_flags"].append("invalid_candidate_bounds")
        return result

    if noise_window_seconds <= 0:
        result["quality_flags"].append("invalid_noise_window")
        return result

    candidate = signal[candidate_start:candidate_end]

    noise_samples = int(round(noise_window_seconds * sampling_rate))
    noise_start = max(0, candidate_start - noise_samples)
    background = signal[noise_start:candidate_start]

    if candidate.size == 0:
        result["quality_flags"].append("empty_candidate")
        return result

    if background.size < 2:
        result["quality_flags"].append("insufficient_background")
        return result

    # Estimate background and candidate RMS after removing their means.
    background_centered = background - np.mean(background)
    candidate_centered = candidate - np.mean(candidate)

    noise_rms = float(np.sqrt(np.mean(background_centered ** 2)))
    candidate_rms = float(np.sqrt(np.mean(candidate_centered ** 2)))

    epsilon = np.finfo(np.float64).eps
    amplitude_ratio = float(candidate_rms / max(noise_rms, epsilon))

    result["valid"] = True
    result["noise_rms"] = noise_rms
    result["candidate_rms"] = candidate_rms
    result["amplitude_ratio"] = amplitude_ratio

    # Clipping can only be assessed meaningfully when the ADC/sensor limit
    # is known. This checks proximity to a supplied absolute limit.
    if clipping_limit is not None:
        if not np.isfinite(clipping_limit) or clipping_limit <= 0:
            result["quality_flags"].append("invalid_clipping_limit")
        else:
            clipped = bool(np.any(np.abs(candidate) >= 0.99 * clipping_limit))
            result["clipped"] = clipped

            if clipped:
                result["quality_flags"].append("possible_clipping")

    # This is a configurable heuristic, not an earthquake classifier.
    if amplitude_ratio < 2.0:
        result["quality_flags"].append("weak_amplitude_change")

    if not result["quality_flags"]:
        result["quality_flags"].append("no_basic_quality_flags")

    return result
