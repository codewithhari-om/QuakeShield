
import numpy as np
import pytest

from quakeshield_signal.features import extract_event_features


def test_extract_event_features():
    signal = np.array([0.0, 1.0, -2.0, 2.0, 0.0])
    sampling_rate = 1.0

    candidates = [{
        "start_sample": 1,
        "end_sample": 4,
        "start_time_seconds": 1.0,
        "end_time_seconds": 4.0,
    }]

    results = extract_event_features(
        signal,
        sampling_rate,
        candidates,
    )

    assert len(results) == 1
    assert results[0]["peak_amplitude"] == 2.0
    assert results[0]["rms_amplitude"] == pytest.approx(
        np.sqrt(3.0)
    )
    assert results[0]["duration_seconds"] == 3.0
    assert results[0]["start_time_seconds"] == 1.0
    assert results[0]["end_time_seconds"] == 4.0


def test_empty_candidate_list():
    signal = np.array([1.0, 2.0, 3.0])

    results = extract_event_features(
        signal,
        10.0,
        [],
    )

    assert results == []


def test_reject_empty_signal():
    with pytest.raises(ValueError):
        extract_event_features(
            np.array([]),
            10.0,
            [],
        )


def test_reject_multidimensional_signal():
    with pytest.raises(ValueError):
        extract_event_features(
            np.array([[1.0, 2.0], [3.0, 4.0]]),
            10.0,
            [],
        )


def test_reject_non_finite_signal():
    with pytest.raises(ValueError):
        extract_event_features(
            np.array([1.0, np.nan, 3.0]),
            10.0,
            [],
        )


def test_reject_invalid_sampling_rate():
    for sampling_rate in [0, -1, np.inf, np.nan]:
        with pytest.raises(ValueError):
            extract_event_features(
                np.array([1.0, 2.0]),
                sampling_rate,
                [],
            )


def test_reject_invalid_candidate_bounds():
    signal = np.array([1.0, 2.0, 3.0])

    invalid_candidates = [
        {
            "start_sample": -1,
            "end_sample": 2,
            "start_time_seconds": 0.0,
            "end_time_seconds": 0.2,
        },
        {
            "start_sample": 0,
            "end_sample": 4,
            "start_time_seconds": 0.0,
            "end_time_seconds": 0.4,
        },
        {
            "start_sample": 2,
            "end_sample": 2,
            "start_time_seconds": 0.2,
            "end_time_seconds": 0.2,
        },
    ]

    for candidate in invalid_candidates:
        with pytest.raises(ValueError):
            extract_event_features(
                signal,
                10.0,
                [candidate],
            )


def test_reject_non_integer_candidate_indices():
    signal = np.array([1.0, 2.0, 3.0])

    candidate = {
        "start_sample": 0.5,
        "end_sample": 2,
        "start_time_seconds": 0.0,
        "end_time_seconds": 0.2,
    }

    with pytest.raises(ValueError):
        extract_event_features(
            signal,
            10.0,
            [candidate],
        )
