# QuakeShield — Seismic Signal Processing and AI-Based Phase Detection

QuakeShield is an experimental earthquake early-warning prototype designed to process seismic waveforms, detect candidate ground-motion disturbances, and identify potential seismic phase arrivals using traditional signal-processing techniques and pretrained deep-learning models.

The project combines a Python-based signal-processing pipeline with an AI-based phase-picking module. The long-term objective is to integrate the processing system with physical seismic sensors, a hardware gateway, a backend service, and mobile and web applications.

**Current development stage:** Signal-processing pipeline implemented, simulated streaming demonstrated, JSON event export implemented, and standalone pretrained PhaseNet inference successfully tested on an existing seismic recording.

> **Disclaimer:** QuakeShield is a research and development prototype. It is not an operational earthquake warning system and must not be relied upon for public-safety decisions.

---

## 1. Project Objectives

The current software work focuses on the following objectives:

- Process seismic waveform data and validate signal quality.
- Detect candidate disturbances using traditional seismic detection methods.
- Extract numerical features describing candidate events.
- Rank candidate detections using a heuristic scoring system.
- Apply an open-source pretrained deep-learning model to identify potential P-wave and S-wave arrivals.
- Export analysis results in a structured JSON format.
- Prepare the architecture for future backend, mobile application, website, and sensor integration.

The longer-term goal is to investigate whether early seismic signals can support useful warnings before stronger shaking reaches locations farther from an earthquake's source. Achieving this requires reliable phase detection, event-location and timing information, communication infrastructure, and extensive validation.

## 2. Technologies and Tools

| Technology | Purpose |
|---|---|
| Python 3.13 | Primary development language for signal processing and AI integration |
| NumPy | Numerical operations, waveform calculations, RMS and spectral features |
| ObsPy | Reading seismic recordings, waveform manipulation, and band-pass filtering |
| STA/LTA | Traditional short-term average / long-term average trigger for candidate detection |
| SeisBench | Framework for using pretrained seismic machine-learning models |
| PhaseNet | Deep-learning model for seismic phase picking |
| PyTorch | Neural-network inference framework used by the pretrained model |
| JSON | Structured storage and exchange of candidate-analysis results |
| pytest | Automated testing of the signal-processing modules |
| Git and GitHub | Version control and source-code hosting |

### Planned application and hardware technologies

These components are planned for future integration and should not be considered fully implemented by the current signal-processing code.

- **Mobile application:** Flutter
- **Web dashboard:** React and TypeScript
- **Backend API:** FastAPI
- **Sensor nodes:** ESP32 with geophones and an ADS1256 ADC
- **Additional motion sensing:** ADXL355
- **Gateway:** Raspberry Pi 4
- **Cellular communication:** A7670C LTE module

The availability of these components in the project design does not mean that physical sensor data is currently connected to the software pipeline.

---

## 3. Implemented Signal-Processing Pipeline

The traditional signal-processing pipeline is organized into independent Python modules.

### 3.1 Waveform preprocessing

**Module:** `preprocessing.py`

Implemented functionality includes:

- Waveform validation and conversion to numerical arrays.
- Checks for invalid values and inappropriate sampling rates.
- Mean removal to center a signal around zero.
- Band-pass filtering using ObsPy.

These operations prepare the input waveform for subsequent detection and feature extraction.

### 3.2 Candidate detection

**Module:** `detection.py`

The detector uses the STA/LTA method to identify intervals where short-term signal energy increases relative to longer-term background energy.

The implementation supports configurable:

- STA and LTA window durations.
- Trigger-on threshold.
- Trigger-off threshold.

The output contains candidate start and end sample indices and corresponding times relative to the input waveform.

These intervals represent candidate disturbances; they are not automatically confirmed earthquakes or P-wave arrivals.

### 3.3 Event feature extraction

**Module:** `features.py`

The feature extractor calculates basic characteristics of each candidate:

- Event duration.
- Peak absolute amplitude.
- Root mean square (RMS) amplitude.
- Candidate start and end times.

These numerical features help describe and compare detected intervals.

### 3.4 Signal-quality assessment

**Module:** `quality.py`

The quality assessment module evaluates candidate signals using characteristics such as:

- Background noise RMS.
- Candidate RMS.
- Candidate-to-background amplitude ratio.
- Possible clipping.
- Insufficient background data.
- Weak amplitude change.

The resulting quality flags provide additional context for interpreting candidate detections.

### 3.5 Onset and spectral features

**Module:** `onset_features.py`

Additional descriptive features include:

- First-window and last-window RMS.
- Candidate and background RMS.
- Onset ratio.
- Dominant frequency.
- Spectral centroid.
- Spectral bandwidth.

These features describe signal behavior and frequency content. They are not, by themselves, a validated classifier for distinguishing P-waves from other disturbances.

### 3.6 Candidate scoring and ranking

**Module:** `scoring.py`

A heuristic scoring function assigns candidate scores between 0 and 100 and categorizes candidates as HIGH, MEDIUM, or LOW priority.

The current score is based on selected signal features and quality-related penalties. It is intended to rank candidates for investigation.

**Important:** The score is not a calibrated earthquake probability, and a HIGH priority candidate is not a confirmed earthquake alert.

### 3.7 Integrated processing pipeline

**Module:** `pipeline.py`

The processing pipeline combines the traditional processing stages:

1. Validate the input waveform.
2. Remove its mean.
3. Apply band-pass filtering.
4. Detect candidate intervals using STA/LTA.
5. Extract event features.
6. Assess signal quality.
7. Extract additional onset and spectral features when possible.
8. Calculate heuristic scores and priority labels.
9. Sort candidates by score.

The pipeline returns the filtered signal, detected candidates, features, quality results, and ranked candidates.

---

## 4. Simulated Streaming and Rolling-Buffer Processing

**Modules:** `stream_processor.py` and the streaming examples.

A rolling-buffer processor has been implemented to support the initial development of a streaming workflow.

Implemented functionality includes:

- Accepting incoming numerical sample chunks.
- Maintaining a rolling waveform buffer.
- Waiting until the configured analysis window is full.
- Reprocessing the buffer at configured intervals.
- Passing the buffered waveform through the existing processing pipeline.

The simulated streaming examples generate synthetic background noise and disturbances. The live export demo successfully processes repeated windows and updates a JSON output file.

This demonstrates the software flow from incoming sample chunks to candidate analysis. It does not yet represent a hardware-connected, continuous real-time earthquake monitoring system.

**Current limitation:** The basic rolling-buffer processor reprocesses each window. Filtering and candidate timing across overlapping windows have not yet been fully addressed for a production streaming implementation.

---

## 5. JSON Event Output

**Module:** `event_output.py`

The JSON exporter converts processing results into a structured message containing:

- Station identifier.
- Message generation timestamp.
- Sampling rate.
- Number of candidate detections.
- Candidate start and end times.
- Heuristic score and priority.
- Signal-quality flags.
- Extracted event features.
- Available onset and spectral features.
- An experimental-prototype warning.

The generated message can be saved to:

`data/latest_event_message.json`

This provides a basic data-exchange format for a future backend or application.

At present, the JSON output has been tested with the traditional processing pipeline. PhaseNet predictions have not yet been integrated into the exported message.

---

## 6. Open-Source AI Integration: PhaseNet

### 6.1 Framework and model

The project uses SeisBench to load a pretrained PhaseNet model with the `geofon` pretrained weights.

The current environment includes Python, SeisBench, PyTorch, ObsPy, and NumPy.

PhaseNet is used for seismic phase picking: identifying likely arrival times for phases such as P and S in seismic waveforms.

### 6.2 Implemented AI wrapper

**Module:** `phasenet_detector.py`

A separate `PhaseNetDetector` class has been implemented. It:

1. Loads the pretrained PhaseNet model.
2. Accepts an ObsPy waveform stream.
3. Runs phase classification.
4. Extracts the model's phase picks.
5. Returns structured results containing phase type, UTC arrival time, confidence output, and trace identifier.

A standalone example, `examples/test_phasenet_detector.py`, has been run successfully.

### 6.3 Preliminary test result

The existing recording used for the initial test is:

- **File:** `data/real_waveform.mseed`
- **Trace:** `IU.ANMO.00.BHZ`
- **Sampling rate:** 20 Hz
- **Number of samples:** 12,000
- **Recorded duration:** Approximately 10 minutes

PhaseNet returned one P-phase pick:

- **Predicted arrival:** `2010-05-24T16:27:00.059538Z`
- **Model confidence output:** `0.852`

A previously identified theoretical P-wave arrival was approximately `2010-05-24T16:26:59.929861Z`, making the difference between these two times approximately 0.13 seconds.

This is an encouraging preliminary result for one recording, but it is not a reliable performance benchmark. The available waveform contains only one vertical component, whereas PhaseNet generally benefits from three-component input. The model output must be evaluated against appropriate reference arrivals across multiple recordings.

The reported confidence value is a model output and should not be interpreted as a guaranteed probability of correctness.

---

## 7. Current Project Structure

The following shows the main files relevant to the current implementation. Check the repository for any additional files.

```text
signal_processing/
├── src/
│   └── quakeshield_signal/
│       ├── __init__.py
│       ├── preprocessing.py
│       ├── detection.py
│       ├── features.py
│       ├── quality.py
│       ├── scoring.py
│       ├── onset_features.py
│       ├── pipeline.py
│       ├── stream_processor.py
│       ├── event_output.py
│       └── phasenet_detector.py
├── examples/
│   ├── demo_waveform.py
│   ├── inspect_event.py
│   ├── evaluate_recording.py
│   ├── summarize_results.py
│   ├── rank_candidates.py
│   ├── event_timeline.py
│   ├── compare_thresholds.py
│   ├── streaming_demo.py
│   ├── live_sensor_demo.py
│   ├── export_event.py
│   ├── live_export_demo.py
│   ├── run_phasenet.py
│   └── test_phasenet_detector.py
├── tests/
├── data/
│   ├── real_waveform.mseed
│   ├── candidate_results.csv
│   └── ranked_candidate_results.csv
├── README.md
└── requirements.txt
```

---

## 8. Testing and Development Environment

The project has been developed and tested on Windows using a Python virtual environment.

**Known environment details:**

- Python 3.13
- Virtual environment: `signal_processing/.venv`
- Test framework: pytest
- AI framework: SeisBench and PyTorch

A previous full test run reported 24 passing tests before the latest PhaseNet wrapper work. The PhaseNet example subsequently ran successfully, but a fresh full test run after the latest changes has not yet been confirmed.

### Run the existing tests

From PowerShell:

```powershell
cd E:\quakeshield_app\signal_processing
.\.venv\Scripts\Activate.ps1
$env:PYTHONPATH = "$PWD\src"
pytest -q
```

### Run the PhaseNet example

```powershell
python examples\test_phasenet_detector.py
```

The pretrained model may need to be downloaded on the first run if its cached weights are unavailable.

---

## 9. Remaining Work and Roadmap

### Phase 1 — Finish AI integration

- Add PhaseNet picks to the JSON event message.
- Keep AI confidence separate from the traditional heuristic score.
- Add automated tests for the combined output.
- Define how phase picks and candidate detections are associated.
- Test timestamp handling and overlapping-window behavior.

### Phase 2 — Backend development

- Implement a basic FastAPI service.
- Expose endpoints for service health and the latest candidate-analysis message.
- Define a stable JSON contract for the mobile and web applications.
- Add input validation and appropriate error handling.
- Test the API with locally generated analysis results.

### Phase 3 — Application integration

- Build the QuakeShield Flutter mobile interface.
- Develop the React and TypeScript web dashboard.
- Display sensor status, candidate detections, phase picks, timestamps, and quality indicators.
- Clearly label simulated or unverified detections.
- Connect the interfaces to the backend when it is ready.

### Phase 4 — Physical sensor integration

- Connect the intended seismic sensors and ADC to the sensor node.
- Establish data acquisition and timestamping.
- Transfer sample data to the gateway.
- Evaluate data loss, noise, sampling stability, and communication latency.
- Verify that the software correctly handles real sensor samples.

### Phase 5 — Validation and evaluation

- Test multiple labeled seismic recordings.
- Measure phase-picking timing error.
- Evaluate missed detections and false positives.
- Compare PhaseNet against the traditional STA/LTA baseline.
- Evaluate end-to-end processing and communication latency.
- Investigate multi-station confirmation and alert delivery.

These phases are planned work; they should only be marked complete after implementation and testing.

---

## 10. Limitations and Safety Considerations

QuakeShield is currently an experimental signal-processing and AI prototype.

- STA/LTA candidate detections do not confirm that an earthquake has occurred.
- Heuristic scores are not calibrated probabilities.
- PhaseNet phase picks require validation.
- A single-component recording does not provide the full three-component input normally preferred for PhaseNet.
- Synthetic disturbances demonstrate software behavior but do not establish real-world earthquake detection performance.
- Real-time hardware integration, multi-station processing, reliable alert distribution, and safety validation remain incomplete.

The project investigates early-warning technology; it does not predict earthquakes before rupture begins.

---

## 11. Repository

GitHub: https://github.com/codewithhari-om/QuakeShield

The repository should document implemented features separately from planned functionality so contributors can distinguish tested code from future development.

**Next immediate task:** Integrate PhaseNet predictions into the existing JSON event output, add tests, and then continue with the FastAPI backend.
