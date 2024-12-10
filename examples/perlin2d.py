import numpy as np
import matplotlib.pyplot as plt
from noise import pnoise2

# Parameters for the Perlin noise grid
width, height = 100, 100  # Size of the grid
scale = 10.0  # Scale of Perlin noise; smaller means more aggressive changes
octaves = 4  # Number of noise layers
persistence = 0.5  # Amplitude persistence between layers
lacunarity = 2.0  # Frequency scaling factor between layers

# Time steps for diminishing amplitude
time_steps = 100  # Number of frames
initial_amplitude = 1.0

# Create figure
fig, ax = plt.subplots(figsize=(8, 8))

# Generate diminishing amplitude animation
for t in range(time_steps):
    # Generate Perlin noise for the frame
    amplitude = initial_amplitude * (1 - t / time_steps)  # Diminishing amplitude
    noise_grid = np.zeros((width, height))

    for i in range(width):
        for j in range(height):
            # Apply Perlin noise with absolute values and diminishing amplitude
            noise_value = pnoise2(
                i / scale,
                j / scale,
                octaves=octaves,
                persistence=persistence,
                lacunarity=lacunarity,
                repeatx=1024,
                repeaty=1024,
                base=t,
            )
            noise_grid[i, j] = abs(noise_value) * amplitude

    # Clear the previous frame and plot
    ax.clear()
    ax.imshow(noise_grid, cmap="inferno", interpolation="nearest")
    ax.set_title(f"Perlin Noise Frame {t+1}")
    ax.axis("off")

    plt.pause(0.1)  # Pause to create an animation effect

plt.show()
