import numpy as np
from signal_processing.preprocessing import (
    remove_mean,
    normalize_signal,
    bandpass_filter,
)

def test_remove_mean():
    signal = np.array([2, 4, 6, 8, 10])
    result = remove_mean(signal)
    expected = np.array([-4, -2, 0, 2, 4])
    np.testing.assert_allclose(result, expected)
    print("PASS: remove_mean")

def test_normalize_signal():
    signal = np.array([2, 4, 6, 8, 10])
    result = normalize_signal(signal)
    expected = np.array([0.2, 0.4, 0.6, 0.8, 1.0])
    np.testing.assert_allclose(result, expected)
    print("PASS: normalize_signal")

def test_bandpass_filter():
    sampling_rate = 100
    time = np.arange(0, 5, 1 / sampling_rate)

    signal = (
        np.sin(2 * np.pi * 5 * time)
        + 0.5 * np.sin(2 * np.pi * 30 * time)
    )

    result = bandpass_filter(
        signal,
        sampling_rate,
        low_cutoff=1,
        high_cutoff=10,
    )

    assert result.shape == signal.shape
    assert np.all(np.isfinite(result))
    print("PASS: bandpass_filter")

if __name__ == "__main__":
    test_remove_mean()
    test_normalize_signal()
    test_bandpass_filter()
    print("All tests passed!")
