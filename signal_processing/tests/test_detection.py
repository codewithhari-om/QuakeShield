
import numpy as np
import pytest

from quakeshield_signal.detection import detect_candidates


def make_test_signal():
    """Create noise with an artificial event beginning at 30 seconds."""
    sampling_rate = 100.0
    duration = 60.0
    time = np.arange(int(sampling_rate * duration)) / sampling_rate

    rng = np.random.default_rng(42)
    signal = rng.normal(0, 0.05, len(time))

    event_start = int(30 * sampling_rate)
    event_end = int(35 * sampling_rate)

    signal[event_start:event_end] += (
        0.5 * np.sin(2 * np.pi * 5 * time[event_start:event_end])
    )

    return signal, sampling_rate


def test_detects_artificial_event():
    signal, sampling_rate = make_test_signal()

    candidates = detect_candidates(signal, sampling_rate)

    assert len(candidates) > 0

    # At least one detected interval should be near the injected event.
    assert any(
        29.0 <= candidate["start_time_seconds"] <= 31.0
        for candidate in candidates
    )


def test_rejects_invalid_sampling_rate():
    signal, sampling_rate = make_test_signal()

    with pytest.raises(ValueError):
        detect_candidates(signal, 0)


def test_rejects_waveform_that_is_too_short():
    signal = np.array([0.1, 0.2, 0.1, 0.3])

    with pytest.raises(ValueError):
        detect_candidates(signal, 100.0)

def test_background_noise_only():
    sampling_rate = 100.0
    rng = np.random.default_rng(123)

    # 60 seconds of low-amplitude background noise.
    signal = rng.normal(0, 0.05, int(60 * sampling_rate))

    candidates = detect_candidates(signal, sampling_rate)

    # This is a desired behavior for our synthetic noise test.
    assert len(candidates) == 0

@pytest.mark.parametrize("amplitude", [0.3, 0.5, 0.8])
def test_detects_events_at_different_amplitudes(amplitude):
    sampling_rate = 100.0
    time = np.arange(6000) / sampling_rate

    rng = np.random.default_rng(42)
    signal = rng.normal(0, 0.05, len(time))

    start = int(30 * sampling_rate)
    end = int(35 * sampling_rate)

    signal[start:end] += (
        amplitude
        * np.sin(2 * np.pi * 5 * time[start:end])
    )

    candidates = detect_candidates(signal, sampling_rate)

    assert any(
        29.0 <= candidate["start_time_seconds"] <= 31.0
        for candidate in candidates
    )
