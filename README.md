# QuakeShield 🌍

**An Earthquake Early Warning Research and Development System**

QuakeShield is a research-driven project focused on seismic monitoring, earthquake detection, and timely alert delivery. It aims to integrate seismic sensors, signal processing, AI-assisted analysis, and multiple warning channels into a unified system.

The project explores detecting seismic activity and identifying relevant wave arrivals, including P-waves, to support the delivery of alerts before stronger shaking reaches locations where useful warning time is available. Actual warning time and reliability depend on sensor placement, detection performance, communication latency, and distance from the earthquake.

> **Project status:** Under development. QuakeShield is a research and prototyping project, not a certified or operational public warning service.

## 🎯 Project Objectives

- Develop a seismic sensing and monitoring system.
- Study P-wave and S-wave behavior for earthquake detection.
- Process seismic signals and investigate noise reduction and phase detection.
- Explore AI models for seismic event classification and edge inference.
- Integrate hardware, embedded firmware, signal processing, and AI.
- Develop warning channels for mobile devices, websites, and browser extensions.
- Evaluate detection performance, latency, reliability, and alert delivery.

## 🏗️ System Architecture

QuakeShield is organized into three primary system layers.

### 1. Warning Systems

The interfaces and services through which seismic information and alerts can be delivered.

- **Mobile application:** Flutter-based application for monitoring and alert presentation.
- **Website:** Web interface for seismic status, historical information, and related project features.
- **Browser extension:** Potential browser-based status and notification channel.
- **Backend:** APIs, data services, alert coordination, database integration, and communication with other components.
- **Shared assets:** Branding, icons, and common visual resources.

### 2. Hardware System

The physical sensing and embedded electronics layer.

- Hardware architecture and specifications.
- Sensor selection and electrical interfaces.
- Circuit schematics, PCB design, and wiring diagrams.
- Firmware, sensor acquisition, and device drivers.
- CAD models, assemblies, enclosure design, and technical drawings.
- Bill of materials, manufacturing documentation, and hardware testing.

### 3. Hardware–Software Integration

The processing and integration layer connecting sensor data to detection and warning channels.

- **Signal processing:** Filtering, preprocessing, feature extraction, and seismic phase detection research.
- **Edge AI:** Investigation of local model inference on supported edge devices.
- **ML models:** Model development, evaluation, configuration, and deployment assets.
- **Interfaces and communication:** Data exchange between sensors, processing components, backend services, and warning channels.
- **Integration and validation:** End-to-end testing, performance measurement, and system validation.

## 📁 Repository Structure

```text
QuakeShield/
├── warning_systems/
│   ├── mobile_app/              # Flutter mobile application
│   ├── website/                 # Website source and tests
│   ├── browser_extension/       # Browser extension
│   ├── backend/                 # APIs and alert services
│   ├── shared_assets/           # Shared visual assets
│   └── README.md
│
├── hardware_system/
│   ├── architecture/
│   ├── specifications/
│   ├── circuit_design/
│   │   ├── schematics/
│   │   ├── pcb/
│   │   └── wiring_diagrams/
│   ├── firmware/
│   ├── cad/
│   │   ├── source/
│   │   ├── assemblies/
│   │   ├── exports/
│   │   └── technical_drawings/
│   ├── enclosure/
│   ├── bill_of_materials/
│   ├── manufacturing/
│   ├── tests/
│   └── README.md
│
├── hardware_software_integration/
│   ├── architecture/
│   ├── interfaces/
│   ├── signal_processing/
│   ├── ai_integration/
│   │   ├── edge_ai/
│   │   └── ml_models/
│   ├── communication/
│   ├── integration_tests/
│   ├── validation/
│   └── README.md
│
├── research/
│   ├── seismology/
│   ├── data/
│   ├── experiments/
│   ├── evaluation/
│   └── references/
│
├── docs/
│   ├── architecture/
│   ├── api/
│   ├── team/
│   ├── testing/
│   └── safety/
│
├── scripts/
├── tests/
├── CONTRIBUTING.md
└── README.md
```

*The structure describes the intended organization. Some directories may contain only starter documentation until their implementation begins.*

## 🔬 Research and Development

The project investigates the following areas:

- Seismology and seismic wave behavior.
- Sensor acquisition and embedded systems.
- Seismic signal processing and event detection.
- AI-assisted classification and edge inference.
- Hardware–software communication and integration.
- Alert delivery and end-to-end system evaluation.

## 🧪 Testing and Validation

Testing will cover the components as they are implemented, including:

- Unit and integration tests.
- Signal-processing and detection evaluation.
- Hardware and sensor validation.
- AI model evaluation and inference performance.
- Alert delivery latency and reliability.
- End-to-end testing using appropriate test data and controlled experiments.

## 🛡️ Safety and Limitations

QuakeShield is intended to investigate earthquake early warning, which relies on detecting an earthquake after it begins and using the time before stronger shaking reaches a receiving location.

It does not claim to predict the exact time, location, or magnitude of an earthquake before it starts. Alerts may be unavailable, delayed, or inaccurate. The project must be validated against appropriate seismic data and hardware tests before any real-world safety use.

QuakeShield must not replace official earthquake alerts, emergency guidance, or established safety procedures.

## 🤝 Collaboration

The repository separates work by technical responsibility:

- Seismology research and detection requirements.
- Hardware design and embedded systems.
- CAD, enclosure design, and manufacturing documentation.
- Signal processing and seismic data analysis.
- AI model research and inference.
- Application, website, backend, and system integration.

Contributors should work in the relevant module, document interfaces and assumptions, test changes where possible, and coordinate shared deliverables through pull requests or reviewed commits.

See [CONTRIBUTING.md](CONTRIBUTING.md) for repository contribution guidelines.

## 🚧 Development Status

QuakeShield is being developed incrementally. The presence of a directory does not mean its subsystem is complete or connected to a working end-to-end detection pipeline.

## 📜 Disclaimer

QuakeShield is an experimental research and development project. It is not a substitute for official earthquake monitoring, public warning infrastructure, or emergency services.

---

**QuakeShield — Researching better ways to detect seismic activity and deliver timely warnings.**
