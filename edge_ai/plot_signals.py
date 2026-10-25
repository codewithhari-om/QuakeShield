import matplotlib.pyplot as plt

# Base synthetic seismic signal
base_signal = [
    1, -1, 2, -2, 1, -1, 2, -2, 1, -1,
    1, -2, 2, -1, 1, -1, 2, -1, 1, -2
]

# Create three signals with different amplitudes
weak_signal = [x * 0.01 for x in base_signal]
medium_signal = [x * 0.03 for x in base_signal]
strong_signal = [x * 0.15 for x in base_signal]

# Sample numbers on the horizontal axis
samples = list(range(1, len(base_signal) + 1))

# Create three graphs
fig, axes = plt.subplots(3, 1, figsize=(10, 8))

signals = [
    ("Weak Signal", weak_signal),
    ("Medium Signal", medium_signal),
    ("Strong Signal", strong_signal),
]

for ax, (name, signal) in zip(axes, signals):
    ax.plot(samples, signal, marker="o")
    ax.set_title(name)
    ax.set_xlabel("Sample Number")
    ax.set_ylabel("Amplitude")
    ax.grid(True)

plt.tight_layout()

# Save the graph as an image
plt.savefig("seismic_signals.png", dpi=150)
print("Graph saved as seismic_signals.png")

plt.show()
