# QuakeShield — Signal Processing

## Overview

This module provides an experimental seismic waveform-processing pipeline for the QuakeShield Earthquake Early Warning System.

It currently supports waveform preprocessing, STA/LTA candidate detection, basic feature extraction, offline recording analysis, threshold comparisons, and candidate-event reporting.

## Implemented Features

- **Preprocessing:** mean removal and Butterworth bandpass filtering using ObsPy.
- **Candidate detection:** Short-Term Average / Long-Term Average (STA/LTA) triggering.
- **Feature extraction:** peak amplitude, RMS amplitude, and candidate duration.
- **Offline evaluation:** waveform inspection, candidate ranking, and threshold comparisons.
- **Candidate grouping:** exploratory grouping of nearby detections.
- **CSV reporting:** exports candidate and evaluation results for further analysis.

## Project Structure

```text
signal_processing/
├── src/
│   └── quakeshield_signal/
│       ├── __init__.py
│       ├── preprocessing.py
│       ├── detection.py
│       └── features.py
├── examples/
├── tests/
├── data/
├── requirements.txt
└── README.md
```

## Setup

Create and activate a virtual environment, then install the dependencies:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

## Run Tests

From this directory, run:

```powershell
$env:PYTHONPATH = "$PWD\src"
pytest -q
```

## Run the Offline Replay

```powershell
$env:PYTHONPATH = "$PWD\src"
python examples/streaming_demo.py
```

The replay processes a saved waveform in chunks and exports grouped candidate activity to `data/streaming_events.csv`.

Other scripts in `examples/` support waveform inspection, feature evaluation, candidate ranking, and threshold comparison.

## Current Limitations

- The current replay uses a saved waveform, not a live sensor stream.
- Filtering is performed offline; continuous operation requires appropriate filter-state handling.
- STA/LTA detections indicate candidate signal disturbances, not confirmed earthquakes or P-wave arrivals.
- Threshold settings have only been explored on limited data and are not validated production settings.
- False-alarm rates, detection probability, and real-time latency have not been established.
- Public earthquake warnings must not be issued by this experimental module.

## Future Work

1. Implement continuous waveform processing with preserved filter state.
2. Evaluate multiple labeled seismic recordings and known arrival times.
3. Measure detection latency, missed detections, and false alarms per hour.
4. Integrate supported sensor hardware and validate end-to-end alert behavior.
5. Document and test the interface between signal processing, the gateway, and the QuakeShield application.

## Disclaimer

This is a research and prototyping module. It is not a certified earthquake early-warning system.
