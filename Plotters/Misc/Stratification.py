import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from scipy.interpolate import griddata
from matplotlib.dates import date2num, num2date
from matplotlib.ticker import MaxNLocator

data = pd.read_csv('')

# Convert 'Time' column to numerical values
data[''] = pd.to_datetime(data[''])
data[''] = date2num(data[''])

# Generate example data
depths = data[''].values
time = data[''].values
temperature = data[''].values

# Create a meshgrid with regular intervals
time_grid = np.linspace(time.min(), time.max(), 100)
depth_grid = np.linspace(depths.min(), depths.max(), 100)
T, D = np.meshgrid(time_grid, depth_grid)

# Interpolate the temperature data onto the meshgrid
temperature_interp = griddata((time, depths), temperature, (T, D), method='linear')

# Create a 2D plot with depth on the y-axis, time on the x-axis, and temperature as the color
plt.figure(figsize=(10, 6))
plt.pcolormesh(T, D, temperature_interp, shading='auto', cmap='viridis')

# Customize the plot
plt.xlabel('Time')
plt.ylabel('Depth')
plt.title('Thermal Stratification Over Time and Depth')
plt.colorbar(label='Temperature (°C)')

# Set a reasonable interval for displaying the time values on the x-axis
plt.xticks(rotation=45)
plt.gca().xaxis.set_major_locator(MaxNLocator(nbins=10))

# Convert numerical time values back to hh:mm:ss format for display on the plot
tick_labels = [num2date(num).strftime('%H:%M:%S') for num in plt.xticks()[0]]
plt.xticks(plt.xticks()[0], tick_labels)

# Show the plot
plt.show()
