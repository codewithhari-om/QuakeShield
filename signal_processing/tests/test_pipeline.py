
import numpy as np

from quakeshield_signal.pipeline import process_waveform


def test_pipeline_detects_artificial_event():
    sampling_rate = 100.0
    time = np.arange(6000) / sampling_rate

    rng = np.random.default_rng(42)
    signal = rng.normal(0, 0.05, len(time))

    start = int(30 * sampling_rate)
    end = int(35 * sampling_rate)

    signal[start:end] += (
        0.5 * np.sin(2 * np.pi * 5 * time[start:end])
    )

    result = process_waveform(signal, sampling_rate)

    assert len(result["filtered_signal"]) == len(signal)
    assert result["sampling_rate"] == sampling_rate
    assert len(result["candidates"]) > 0

    assert any(
        29.0 <= item["start_time_seconds"] <= 31.0
        for item in result["candidates"]
    )
    assert len(result["features"]) == len(result["candidates"])
