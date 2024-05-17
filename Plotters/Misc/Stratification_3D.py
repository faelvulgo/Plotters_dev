import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

# Generate example data
depths = np.arange(0, 10, 1)  # Depths from surface to bottom
time = np.arange(0, 24, 1)    # Time in hours
temperature_data = np.random.uniform(10, 30, (len(depths), len(time)))  # Random temperature data

# Create a meshgrid for 3D plotting
time_grid, depth_grid = np.meshgrid(time, depths)

# Plot the 3D surface plot
fig = plt.figure(figsize=(10, 6))
ax = fig.add_subplot(111, projection='3d')
ax.plot_surface(time_grid, depth_grid, temperature_data, cmap='viridis')

# Customize the plot
ax.set_xlabel('Time (hours)')
ax.set_ylabel('Depth')
ax.set_zlabel('Temperature (°C)')
ax.set_title('Thermal Stratification Over Time')

# Show the plot
plt.show()

