
import numpy as np


def score_candidate(features, quality):
    """
    Calculate a transparent 0-100 priority score.

    This is an experimental heuristic, not a probability
    that an earthquake has occurred.
    """

    score = 0.0
    reasons = []

    # 1. Signal amplitude relative to background noise (0-40 points).
    ratio = quality.get("amplitude_ratio")

    if ratio is not None and np.isfinite(ratio) and ratio >= 0:
        amplitude_score = min(ratio / 5.0, 1.0) * 40.0
        score += amplitude_score
        reasons.append(f"Amplitude contribution: {amplitude_score:.1f}/40")
    else:
        reasons.append("Amplitude ratio unavailable")

    # 2. Signal duration (0-20 points).
    duration = features.get("duration_seconds", 0.0)

    if np.isfinite(duration) and duration > 0:
        duration_score = min(duration / 3.0, 1.0) * 20.0
        score += duration_score
        reasons.append(f"Duration contribution: {duration_score:.1f}/20")
    else:
        reasons.append("Duration unavailable or invalid")

    # 3. Candidate RMS relative to background noise (0-40 points).
    noise_rms = quality.get("noise_rms")
    candidate_rms = quality.get("candidate_rms")

    if (
        noise_rms is not None
        and candidate_rms is not None
        and np.isfinite(noise_rms)
        and np.isfinite(candidate_rms)
        and noise_rms >= 0
        and candidate_rms >= 0
    ):
        epsilon = np.finfo(float).eps
        rms_ratio = candidate_rms / max(noise_rms, epsilon)
        rms_score = min(rms_ratio / 5.0, 1.0) * 40.0
        score += rms_score
        reasons.append(f"RMS contribution: {rms_score:.1f}/40")
    else:
        reasons.append("RMS measurements unavailable")

    flags = quality.get("quality_flags", [])

    # Quality warnings reduce priority.
    penalties = {
        "possible_clipping": 20.0,
        "weak_amplitude_change": 15.0,
        "insufficient_background": 10.0,
        "non_finite_samples": 100.0,
        "invalid_waveform_shape": 100.0,
        "invalid_sampling_rate": 100.0,
        "invalid_candidate_bounds": 100.0,
    }

    penalty = sum(penalties.get(flag, 0.0) for flag in flags)
    score = float(np.clip(score - penalty, 0.0, 100.0))

    if not quality.get("valid", False):
        score = 0.0
        reasons.append("Invalid signal quality assessment")

    if penalty:
        reasons.append(f"Quality penalty: {penalty:.1f} points")

    return {
        "score": score,
        "priority": (
            "HIGH" if score >= 70
            else "MEDIUM" if score >= 40
            else "LOW"
        ),
        "reasons": reasons,
    }
