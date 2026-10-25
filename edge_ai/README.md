QuakeShield 🌍

An Earthquake Early Warning System — Edge AI Development

QuakeShield is a project focused on earthquake early warning through seismic signal analysis and technology-assisted alerts. The project includes application, backend, hardware design, and Edge AI components.

🎯 Project Objective

Develop a system that can analyze seismic signals, identify unusual patterns, and support an earthquake early warning workflow. The long-term goal is to integrate sensor data, Edge AI processing, and alert delivery.

🧠 Edge AI Component

My current contribution focuses on the Edge AI component, which explores local seismic signal analysis and anomaly detection.

Current Features

- Synthetic seismic signal generation for testing.
- RMS (Root Mean Square) calculation to measure signal variation.
- Threshold-based signal classification.
- Separate weak, medium, and strong synthetic signal tests.
- Signal visualization using Python and Matplotlib.

Current Test Results

Synthetic Signal| Expected Classification
Weak| NORMAL
Medium| NORMAL
Strong| ANOMALY_DETECTED

These tests use artificial signals to verify the basic processing logic.

🛠️ Technologies Used

- Python — signal processing and anomaly detection.
- Matplotlib — seismic signal visualization.
- GitHub Codespaces — browser-based development.
- Flutter — mobile application technology used by the wider project.

📁 Edge AI Files

edge_ai/
├── first
└── plot_signals.py

- "first" — Python script for synthetic signal analysis and threshold-based classification.
- "plot_signals.py" — generates plots of weak, medium, and strong synthetic signals.

The plotting script generates "seismic_signals.png" when executed successfully.

▶️ Running the Edge AI Demo

Open a terminal in the repository's "edge_ai" directory.

Install the plotting dependency:

python3 -m pip install matplotlib

Run the signal analysis demo:

python3 first

Generate the signal plots:

python3 plot_signals.py

🚧 Current Limitations and Future Work

The current implementation is an early prototype using synthetic signals and a fixed RMS threshold. It is not a trained machine-learning model and has not been validated against real seismic recordings.

Planned improvements include:

- Processing real seismic sensor data.
- Testing with labelled seismic datasets.
- Evaluating false alarms and missed detections.
- Exploring machine-learning-based anomaly detection.
- Integrating the Edge AI component with the project's hardware and mobile application.

Safety note: This prototype is for development and educational testing only. It must not be used as a real earthquake warning system.
