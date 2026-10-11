# QuakeShield 🌍
### AI-Assisted Earthquake Early Warning and Seismic Monitoring System

QuakeShield is a developing engineering project aimed at building an integrated earthquake monitoring and early-warning platform using seismic sensors, signal processing, Artificial Intelligence and Machine Learning (AI/ML), geospatial visualization, and real-time alert delivery.

The project aims to explore how ground-motion data can be processed to identify potential seismic events and communicate relevant information through mobile and web-based interfaces. Its long-term vision is to develop a scalable system that combines hardware-based seismic sensing, automated data processing, historical earthquake analysis, and emergency notification capabilities.

**Project status:** Research and prototype development.

> **Important disclaimer:** The current application is a software prototype. Its monitor waveform, alert, countdown, and siren are simulated demonstrations. They are not connected to a validated earthquake detection system and must not be relied upon as official earthquake warnings or predictions.

---

## 🎯 Project Objectives

- **Seismic monitoring:** Explore methods for collecting and processing ground-motion data from seismic sensors.
- **Early-warning research:** Investigate P-wave detection and the potential to provide useful warning time before stronger seismic waves arrive.
- **AI/ML integration:** Explore signal classification, event detection, noise filtering, and anomaly detection.
- **Real earthquake data:** Integrate trustworthy seismic observations and historical earthquake records from authorized sources.
- **Geospatial visualization:** Display earthquake locations, magnitudes, depths, and event details on an interactive map.
- **Emergency communication:** Develop mobile alerts, audible notifications, and event information interfaces.
- **Web-based monitoring:** Build a complementary website for monitoring seismic events, visualizing data, and presenting analytics.

## 🏗️ Proposed System Architecture

QuakeShield is intended to evolve into a modular system with the following components:

### 1. Hardware and Seismic Data Acquisition

The hardware component will explore the use of Arduino-compatible microcontrollers and suitable seismic sensors for collecting ground-motion measurements.

Planned research areas include:
- Sensor selection, calibration, and noise characterization.
- Sampling and preprocessing of seismic signals.
- P-wave onset detection and investigation of subsequent wave arrivals.
- Reliable transfer of measurements to a processing system.

### 2. Backend and Data Management

A backend service will eventually coordinate data ingestion, processing, storage, and communication between system components.

Planned responsibilities include:
- Receiving measurements from supported sensors.
- Integrating authorized external seismic data sources.
- Validating timestamps, coordinates, and event attributes.
- Storing earthquake events and associated metadata.
- Exposing APIs to the mobile application and web platform.

The backend technology and deployment architecture will be finalized as implementation progresses.

### 3. AI/ML and Signal Processing

The AI/ML component will investigate techniques for distinguishing potential seismic signals from environmental noise and other disturbances.

Potential research directions include:
- Digital signal filtering and feature extraction.
- P-wave onset detection and signal classification.
- Anomaly detection and event characterization.
- Model evaluation using appropriately labelled seismic datasets.
- Assessing false alarms, missed detections, latency, and generalization.

Machine learning will complement, rather than replace, the need for reliable sensors, validated detection algorithms, and independent testing.

### 4. Flutter Mobile Application

The mobile application is being developed using Flutter and Dart.

Current prototype features include:
- A monitoring interface with simulated waveform and alert demonstrations.
- A demonstration countdown and audible siren.
- An earthquake history section with a data-source status interface.
- An architecture designed to accommodate future earthquake records, filters, and geospatial visualization.

The simulated monitoring features are not connected to operational seismic detection or an official warning feed.

### 5. Web Monitoring Platform

A complementary website is planned to provide a broader monitoring and analysis interface.

Proposed capabilities include:
- An interactive map of verified earthquake events.
- Event tables, historical trends, and magnitude-based filtering.
- Monitoring dashboards and statistical summaries.
- Visualizations for processed seismic data.
- System health and data-source status indicators.

The web platform remains part of the planned system unless explicitly documented as implemented.

### 6. Alert and Notification System

The alert subsystem is intended to communicate validated event information to users through appropriate channels.

Future development may include local alarms, push notifications, event severity indicators, and delivery-status monitoring. Any operational warning functionality will require validated event detection, reliable communication, and appropriate safety testing.

---

## 📡 Earthquake Data Sources

QuakeShield prioritizes trustworthy and traceable seismic information.

The preferred source for Indian earthquake history is the **National Center for Seismology (NCS), Government of India**.

Official portal: https://riseq.seismo.gov.in/riseq/earthquake/

Until a documented and suitable automated data source is verified, the application deliberately displays an official-portal-only state and directs users to the NCS website.

The project will not treat invented records as real observations or scrape the portal without an appropriate basis. Any future automated integration should document the source, access method, update frequency, and data limitations.

Historical earthquake records, live seismic measurements, and validated early-warning alerts are separate data categories and must be clearly distinguished.

## 🗺️ Geographic Focus and Potential Impact

QuakeShield is motivated by the need to improve access to understandable seismic information, particularly in earthquake-prone regions of Northeast India.

The project's research direction includes exploring how local sensor observations, verified earthquake data, and rapid information delivery might support seismic awareness and future early-warning research.

The actual warning time available for any earthquake depends on the event location, sensor coverage, detection latency, communication infrastructure, and the distance between the earthquake source and the recipient. Useful warning time cannot be guaranteed.

## 🛠️ Technology Stack

| Component | Technology / Direction |
|---|---|
| Mobile application | Flutter, Dart |
| Mobile alarm | `audioplayers` |
| Hardware prototype | Arduino-compatible microcontroller and suitable seismic sensors |
| Backend | To be selected and implemented |
| AI/ML | Signal processing and machine-learning methods under investigation |
| Database | To be selected |
| Web platform | Planned; framework to be selected |
| Mapping | Planned integration of a suitable geospatial mapping solution |
| Version control | Git and GitHub |
| Testing | Flutter tests and future hardware, data, and model validation |

Technologies listed as planned or under investigation are not necessarily implemented in the current prototype.

## 📁 Repository Structure

The current repository contains the Flutter application and its supporting tests. The broader project may eventually be organized into the following structure:

```text
QuakeShield/
├── lib/                 # Flutter application source
│   ├── features/        # Application features
│   ├── app_shell.dart   # Application shell
│   └── main.dart        # Application entry point
├── assets/
│   └── sounds/          # Application audio assets
├── test/                # Flutter tests
├── android/             # Android platform files
├── ios/                 # iOS platform files
├── web/                 # Flutter web platform files
├── backend/             # Planned backend services
├── ai-ml/               # Planned AI/ML research and models
├── hardware/            # Planned sensor firmware and designs
├── docs/                # Planned architecture and technical docs
├── pubspec.yaml         # Flutter dependencies and configuration
└── README.md
```

The `backend/`, `ai-ml/`, `hardware/`, and `docs/` directories represent the intended future organization and should only be added as the corresponding work is developed.

## 🚧 Development Roadmap

- [x] Create the initial Flutter application prototype.
- [x] Develop the initial monitoring interface and simulated siren.
- [x] Establish the earthquake-history feature structure and source-status handling.
- [x] Initialize Git and prepare the GitHub repository.
- [ ] Refine the mobile interface and improve navigation.
- [ ] Implement interactive geospatial visualization.
- [ ] Verify an authorized and suitable automated NCS data source.
- [ ] Develop backend services and validated earthquake-event storage.
- [ ] Prototype sensor acquisition and signal preprocessing.
- [ ] Research and evaluate P-wave detection methods.
- [ ] Develop and test AI/ML components using suitable seismic datasets.
- [ ] Build the complementary web monitoring platform.
- [ ] Evaluate end-to-end latency, reliability, false alarms, and system limitations.
- [ ] Conduct controlled testing before considering any real warning functionality.

Checklist items describe development goals or completed prototype work, not certification of an operational earthquake-warning system.

## 🧪 Testing and Validation

The current Flutter project includes application tests. As the system expands, validation will also need to cover:

- Data correctness and provenance.
- Sensor calibration and signal quality.
- Detection accuracy and false-alarm rates.
- Processing and communication latency.
- Mobile and web interface reliability.
- Failure handling, offline behavior, and notification delivery.

No operational early-warning performance should be assumed until it has been demonstrated through appropriate testing.

## 🤝 Contributions

Contributions and suggestions related to seismic sensing, embedded systems, signal processing, AI/ML, geospatial visualization, backend development, and Flutter or web development are welcome.

Before contributing, please distinguish implemented features from proposed functionality and preserve the project's data-integrity and safety requirements.

## ⚠️ Disclaimer

QuakeShield is a research-oriented engineering prototype under development. It is not an official earthquake-warning service, is not certified for public-safety use, and does not currently predict earthquakes or provide validated operational early warnings.

For official earthquake information and public-safety guidance, consult the relevant government authorities and authorized sources.

## 📄 License

A license has not yet been selected. Usage, redistribution, and contribution terms will be specified once an appropriate license is chosen.
