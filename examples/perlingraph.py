import numpy as np
import matplotlib.pyplot as plt
from noise import pnoise1

# Parameters for the Perlin noise
length = 100  # Number of points along the x-axis
scale = 30.0  # Base scale for Perlin noise
octaves = 4  # Number of noise layers
persistence = 0.5  # Amplitude persistence between layers
lacunarity = 2.0  # Frequency scaling factor between layers
initial_amplitude = 1.0  # Starting amplitude
k = 0.01  # Decay rate for exponential amplitude

# Generate x values
x_values = np.linspace(0, length / scale, length)

# Generate diminishing amplitude (exponential decay)
amplitudes = initial_amplitude * np.exp(-k * x_values)

# Generate y values with increasing frequency towards the end
y_values = [
    amplitudes[i]
    * abs(
        pnoise1(
            x * (1 + i / length),
            octaves=octaves,
            persistence=persistence,
            lacunarity=lacunarity,
            repeat=1024,
            base=0,
        )
    )
    for i, x in enumerate(x_values)
]

# Plotting
plt.figure(figsize=(10, 6))
plt.title(
    "Static Perlin Noise with Diminishing Amplitude and Increasing Aggressiveness"
)
plt.plot(
    x_values,
    y_values,
    color="blue",
    label="Noise with diminishing amplitude and increasing frequency",
)
plt.xlabel("Time (X)")
plt.ylabel("Value (Y)")
plt.ylim(0, initial_amplitude)
plt.legend()
plt.grid(True)
plt.show()
