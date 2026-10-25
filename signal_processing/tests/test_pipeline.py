
import numpy as np
from quakeshield_signal.pipeline import process_waveform


def test_pipeline_returns_candidates_and_features():
    sampling_rate = 100
    duration = 20

    rng = np.random.default_rng(42)
    signal = rng.normal(0, 0.1, sampling_rate * duration)

    # Simulate an oscillating seismic disturbance.
    start = 1000
    end = 1200
    signal[start:end] += 2.0 * np.sin(
        np.linspace(0, 8 * np.pi, end - start)
    )

    result = process_waveform(signal, sampling_rate)

    assert "filtered_signal" in result
    assert "candidates" in result
    assert "features" in result
    assert result["sampling_rate"] == sampling_rate
    assert len(result["features"]) == len(result["candidates"])


def test_pipeline_rejects_invalid_sampling_rate():
    signal = np.zeros(2000)

    try:
        process_waveform(signal, 0)
    except ValueError:
        pass
    else:
        raise AssertionError(
            "Expected ValueError for invalid sampling rate"
        )
