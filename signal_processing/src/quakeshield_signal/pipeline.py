
from .preprocessing import (
    validate_signal,
    remove_mean,
    bandpass_filter,
)
from .detection import detect_candidates
from .features import extract_event_features
from .quality import assess_signal_quality
from .scoring import score_candidate
from .onset_features import extract_onset_features


def process_waveform(
    signal,
    sampling_rate,
    low_cutoff=1.0,
    high_cutoff=15.0,
):
    """Process a waveform and characterize detected candidates."""

    signal = validate_signal(signal, sampling_rate)
    centered_signal = remove_mean(signal)

    filtered_signal = bandpass_filter(
        centered_signal,
        sampling_rate,
        low_cutoff,
        high_cutoff,
    )

    candidates = detect_candidates(filtered_signal, sampling_rate)

    features = extract_event_features(
        filtered_signal, sampling_rate, candidates
    )

    quality_results = []
    ranked_candidates = []

    for candidate, feature in zip(candidates, features):
        start = candidate["start_sample"]
        end = candidate["end_sample"]

        quality = assess_signal_quality(
            filtered_signal,
            sampling_rate,
            start,
            end,
        )
        
        onset_features = None
        try:
            onset_features = extract_onset_features(
                filtered_signal,
                sampling_rate,
                start,
                end,
            )
        except ValueError:
            # Very short candidates or candidates without enough
            # preceding background cannot provide these features.
            pass

        score = score_candidate(feature, quality)
ml_result = None

if predictor is not None and onset_features is not None:
    combined_features = {
        **feature,
        **onset_features,
    }

    ml_result = predictor(combined_features)
        quality_results.append(quality)

        ranked_candidates.append({
            **candidate,
            "features": feature,
            "quality": quality,
            "onset_features": onset_features,
            "score": score["score"],
            "priority": score["priority"],
            "score_reasons": score["reasons"],
        })

    ranked_candidates.sort(
        key=lambda item: item["score"],
        reverse=True,
    )

    return {
        "filtered_signal": filtered_signal,
        "candidates": candidates,
        "features": features,
        "quality": quality_results,
        "ranked_candidates": ranked_candidates,
        "sampling_rate": sampling_rate,
    }
