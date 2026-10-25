
import numpy as np

from quakeshield_signal.quality import assess_signal_quality


def test_valid_candidate_with_amplitude_change():
    rng = np.random.default_rng(42)
    signal = rng.normal(0, 0.1, 400)

    # Add a synthetic disturbance after 10 seconds at 20 Hz.

    signal[200:240] += 2.0 * np.sin(
    np.linspace(0, 8 * np.pi, 40)
    )
    result = assess_signal_quality(
        signal,
        sampling_rate=20,
        candidate_start=200,
        candidate_end=240,
    )

    assert result["valid"] is True
    assert result["amplitude_ratio"] > 2.0
    assert result["clipped"] is None


def test_invalid_waveform_is_flagged():
    signal = np.array([0.0, 1.0, np.nan, 2.0])

    result = assess_signal_quality(
        signal,
        sampling_rate=20,
        candidate_start=2,
        candidate_end=3,
    )

    assert result["valid"] is False
    assert "non_finite_samples" in result["quality_flags"]


def test_possible_clipping_is_flagged():
    signal = np.zeros(200)
    signal[100:120] = 9.99

    result = assess_signal_quality(
        signal,
        sampling_rate=20,
        candidate_start=100,
        candidate_end=120,
        clipping_limit=10.0,
    )

    assert result["clipped"] is True
    assert "possible_clipping" in result["quality_flags"]


def test_candidate_without_enough_background():
    signal = np.ones(100)

    result = assess_signal_quality(
        signal,
        sampling_rate=20,
        candidate_start=0,
        candidate_end=20,
    )

    assert result["valid"] is False
    assert "insufficient_background" in result["quality_flags"]
