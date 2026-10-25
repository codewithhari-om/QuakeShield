# QuakeShield — Seismic Signal Processing

## 1. Overview

The `signal_processing` module is an experimental component of **QuakeShield**, an AI-enabled Earthquake Early Warning System prototype.

Its current purpose is to process seismic waveforms, detect candidate signal disturbances, extract basic waveform features, and evaluate detection behavior using recorded seismic data.

The module currently supports offline analysis and exploratory chunk-based replay. It is **not yet a validated real-time earthquake early-warning system**.

## 2. Current Features

### Waveform preprocessing
- Mean removal to reduce constant signal offset.
- Butterworth bandpass filtering using ObsPy.
- Input validation for waveform arrays, sampling rates, and filter cutoffs.

### Candidate signal detection
- STA/LTA (Short-Term Average / Long-Term Average) triggering using ObsPy.
- Configurable STA/LTA window lengths and trigger-on/trigger-off thresholds.
- Candidate start and end sample indices and relative timestamps.

### Feature extraction
For each candidate interval, the pipeline can calculate:
- Peak absolute amplitude.
- Root Mean Square (RMS) amplitude.
- Candidate duration.

These features describe the waveform; they do not independently confirm an earthquake or identify a P-wave.

### Offline recording analysis
- Inspect and plot waveform segments.
- Detect candidate intervals in a recorded waveform.
- Rank candidate intervals by amplitude-related features.
- Summarize candidate statistics.
- Compare different STA/LTA threshold settings.
- Group nearby detections into candidate activity episodes.
- Export analysis results to CSV files.

### Chunk-based replay prototype
The `examples/streaming_demo.py` script replays a saved waveform in one-second chunks with a rolling buffer. It demonstrates exploratory candidate detection and grouping.

This is an offline replay prototype. The waveform is filtered before replay; the script does not yet implement a complete live streaming pipeline with preserved filter state.

## 3. Project Structure

```text
signal_processing/
├── README.md
├── requirements.txt
├── src/
│   └── quakeshield_signal/
│       ├── __init__.py
│       ├── preprocessing.py
│       ├── detection.py
│       ├── features.py
│       └── pipeline.py
├── examples/
│   ├── demo_waveform.py
│   ├── inspect_event.py
│   ├── evaluate_recording.py
│   ├── summarize_results.py
│   ├── rank_candidates.py
│   ├── event_timeline.py
│   ├── compare_thresholds.py
│   ├── verify_p_arrival.py
│   ├── streaming_demo.py
│   └── save_threshold_results.py
├── tests/
│   ├── test_detection.py
│   ├── test_features.py
│   └── test_pipeline.py
├── data/
│   ├── real_waveform.mseed
│   ├── candidate_results.csv
│   ├── ranked_candidates.csv
│   ├── event_timeline.csv
│   ├── streaming_events.csv
│   └── threshold_comparison.csv
└── requirements.txt
```

Some output files are generated during analysis and may not exist until the corresponding example scripts are run.

## 4. Requirements and Setup

The module uses Python with the following dependencies:
- ObsPy
- NumPy
- SciPy
- Matplotlib
- pytest

Create and activate a virtual environment from this directory:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

## 5. Running Tests

From the `signal_processing` directory:

```powershell
$env:PYTHONPATH = "$PWD\src"
pytest -q
```

The current test suite has passed in the development environment. This confirms that the existing tests pass; it does not establish seismic detection accuracy or system readiness.

## 6. Running the Examples

### Inspect a waveform

```powershell
$env:PYTHONPATH = "$PWD\src"
python examples/inspect_event.py
```

### Evaluate a recording

```powershell
$env:PYTHONPATH = "$PWD\src"
python examples/evaluate_recording.py
```

### Summarize and rank candidates

```powershell
$env:PYTHONPATH = "$PWD\src"
python examples/summarize_results.py
python examples/rank_candidates.py
```

### Compare STA/LTA thresholds

```powershell
$env:PYTHONPATH = "$PWD\src"
python examples/compare_thresholds.py
```

### Run the chunk-based replay prototype

```powershell
$env:PYTHONPATH = "$PWD\src"
python examples/streaming_demo.py
```

The replay writes grouped candidate activity to `data/streaming_events.csv`.

## 7. Preliminary Experiment

A ten-minute waveform was analyzed with the following metadata:

| Property | Value |
|---|---|
| Network | IU |
| Station | ANMO |
| Channel | BHZ |
| Sampling rate | 20 Hz |
| Number of samples | 12,000 |
| Recording duration | 600 seconds |
| Recording start | 2010-05-24 16:18:28.019538 UTC |

A USGS catalog query returned a magnitude 6.5 event with an origin time of 2010-05-24 16:18:29.090 UTC. A theoretical P-arrival estimate using the IASP91 model was approximately 511.91 seconds after the recording began.

The candidate detector identified a strong disturbance beginning around 512.2 seconds, approximately 0.29 seconds after the predicted arrival.

This timing agreement is encouraging, but it is not conclusive proof of P-wave detection. The result needs independent verification against the waveform, station metadata, event catalog, and additional labeled recordings.

### Exploratory threshold comparison

Four STA/LTA trigger settings were tested on the same recording:

| Trigger on | Trigger off | Candidate intervals | Earlier candidates* | Difference from predicted arrival |
|---:|---:|---:|---:|---:|
| 2.5 | 1.2 | 100 | 86 | +0.29 s |
| 3.0 | 1.5 | 65 | 55 | +0.29 s |
| 4.0 | 2.0 | 18 | 12 | +0.34 s |
| 5.0 | 2.5 | 4 | 1 | +0.34 s |

\*Earlier candidates are unverified signals, not confirmed false alarms.

The `4.0 / 2.0` setting is retained as an experimental configuration for further testing, not as a validated production setting.

## 8. Generated Results

The examples can generate the following CSV outputs:

- `candidate_results.csv` — candidate intervals and extracted features.
- `ranked_candidates.csv` — candidates ranked by amplitude-related features.
- `event_timeline.csv` — candidate activity groups.
- `threshold_comparison.csv` — exploratory threshold comparison.
- `streaming_events.csv` — grouped activity from chunk-based replay.

These outputs support inspection and reproducibility. Candidate counts and grouped episodes should not be interpreted as counts of confirmed earthquakes.

## 9. Current Limitations

- Candidate detections may represent earthquakes, other seismic signals, or noise.
- The current experiments use limited data and do not establish generalization.
- The chunk-based replay is not a complete live sensor implementation.
- Filtering is performed offline; continuous processing needs appropriate filter-state handling.
- Detection latency, missed-event rate, and false alarms per hour have not been validated.
- No validated earthquake magnitude, source location, or time-to-shaking estimate is produced.
- Hardware integration, gateway communication, backend alert delivery, and end-to-end safety testing remain separate development tasks.

## 10. Next Development Steps

1. Implement continuous waveform processing with appropriate filter-state handling.
2. Evaluate multiple labeled earthquake and noise recordings.
3. Measure detection latency, detection probability, and false alarms per hour.
4. Improve candidate grouping and event-state management.
5. Test the pipeline with real sensor data from the intended hardware.
6. Integrate the signal-processing module with the gateway and application only after appropriate validation.

## Disclaimer

QuakeShield is a research and prototyping project. This module is not a certified earthquake early-warning system and must not be used as the sole basis for public safety decisions.
