import numpy as np
import matplotlib.pyplot as plt
from noise import pnoise1

# Parameters for the Perlin noise line
length = 1000  # Number of points along the x-axis
scale = 50.0  # Scale of Perlin noise; smaller means more aggressive changes
octaves = 4  # Number of noise layers
persistence = 0.5  # Amplitude persistence between layers
lacunarity = 2.0  # Frequency scaling factor between layers
time_steps = 100  # Number of frames
initial_amplitude = 1.0  # Initial amplitude of the noise

# Generate x values
x_values = np.linspace(0, length / scale, length)

# Initialize plot
plt.figure(figsize=(10, 6))
plt.title("1D Perlin Noise with Absolute Values and Diminishing Amplitude")
plt.xlabel("X")
plt.ylabel("Y")
plt.ylim(-1, 1)

for t in range(time_steps):
    # Calculate diminishing amplitude
    amplitude = initial_amplitude * (1 - t / time_steps)  # Diminishing amplitude

    # Generate y values based on Perlin noise
    y_values = [
        amplitude
        * abs(
            pnoise1(
                x,
                octaves=octaves,
                persistence=persistence,
                lacunarity=lacunarity,
                repeat=1024,
                base=t,
            )
        )
        for x in x_values
    ]

    # Clear previous lines and plot the new one
    plt.cla()
    plt.plot(x_values, y_values, color="blue", linewidth=1.5, label=f"Frame {t + 1}")
    plt.legend(loc="upper right")
    plt.ylim(0, initial_amplitude)
    plt.pause(0.1)  # Pause for animation effect

plt.show()
