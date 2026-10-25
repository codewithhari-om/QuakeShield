
import numpy as np
import pytest

from quakeshield_signal.onset_features import extract_onset_features


def test_extract_onset_and_frequency_features():
    sampling_rate = 100
    rng = np.random.default_rng(42)

    signal = rng.normal(0, 0.1, 1500)
    t = np.arange(200) / sampling_rate

    signal[500:700] += 2.0 * np.sin(2 * np.pi * 8 * t)

    result = extract_onset_features(
        signal,
        sampling_rate,
        500,
        700,
    )

    assert result["candidate_rms"] > result["noise_rms"]
    assert result["dominant_frequency_hz"] == pytest.approx(
        8.0, abs=1.0
    )
    assert result["spectral_centroid_hz"] > 0
    assert result["spectral_bandwidth_hz"] >= 0


def test_rejects_invalid_candidate_bounds():
    with pytest.raises(ValueError):
        extract_onset_features(
            np.ones(1000),
            100,
            700,
            500,
        )


def test_rejects_insufficient_background():
    with pytest.raises(ValueError):
        extract_onset_features(
            np.ones(1000),
            100,
            0,
            100,
        )
