import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
from gsw import SA_from_SP, CT_from_t, rho as gsw_rho


class HydrographyDiagram:
    def __init__(self, csv_file):
        """
        Initialize the HydrographyDiagram object with data from a CSV file.

        Args:
        csv_file (str): Path to the CSV file containing hydrographic data.
        """
        self.data = pd.read_csv(csv_file)
        self.salinity = self.data['Calc. SALINITY; PSU'].values
        self.temperature = self.data['TEMPERATURE;C'].values
        self.pressure = self.data['PRESSURE;DBAR'].values

    def calculate_density(self):
        """
        Calculate density based on salinity, temperature, and pressure data.
        """
        self.sa = SA_from_SP(self.salinity, self.pressure, 39, 22)
        self.ct = CT_from_t(self.sa, self.temperature, self.pressure)
        self.density = gsw_rho(self.sa, self.ct, self.pressure)

    def plot_diagram(self):
        """
        Plot the hydrography diagram.
        """
        fig, ax = plt.subplots()

        # Scatter plot
        norm = plt.Normalize(self.pressure.min(), self.pressure.max())
        scatter = ax.scatter(self.salinity, self.temperature, c=self.pressure, cmap='viridis', norm=norm, marker='o',
                             s=20)

        # Contour lines
        salinity_reshaped = np.linspace(self.salinity.min(), self.salinity.max(), 100)
        temperature_reshaped = np.linspace(self.temperature.min(), self.temperature.max(), 100)
        salinity_grid, temperature_grid = np.meshgrid(salinity_reshaped, temperature_reshaped)
        density_grid = gsw_rho(salinity_grid, temperature_grid, np.zeros_like(salinity_grid))
        contour = ax.contour(salinity_grid, temperature_grid, density_grid, colors='black')
        contour_labels = ax.clabel(contour, inline=True, fontsize=8, fmt='%.1f')

        # Water mass labels
        self._plot_water_mass_labels(ax)

        # Set labels and title
        ax.set_xlabel('Salinity (PSU)')
        ax.set_ylabel('Temperature ($^\circ$C)')
        ax.set_title('Hydrography Diagram')

        # Set axis limits
        ax.set_xlim(34.32, 37.36)
        ax.set_ylim(2.95, 24.64)

        # Colorbar
        cbar = plt.colorbar(scatter, ax=ax, label='Pressure (dBar)')

        plt.tight_layout()

        # Save and display the plot
        plt.savefig('hydrography_diagram.png', format='png', dpi=900, transparent=False)
        plt.show()

    def _plot_water_mass_labels(self, ax):
        """
        Plot water mass labels within specified temperature and salinity ranges.

        Args:
        ax (matplotlib.axes.Axes): Axes object for plotting.
        """
        index_ranges = {
            'WNACW': {'salinity': [35, 36.7], 'temperature': [7, 20]},
            'ENACW': {'salinity': [35.2, 36.7], 'temperature': [8, 18]},
            'SACW': {'salinity': [34.3, 35.8], 'temperature': [5, 18]},
            'WASIW': {'salinity': [34, 35.1], 'temperature': [3, 9]},
            'EASIW': {'salinity': [34.4, 35.3], 'temperature': [3, 9]},
            'MW': {'salinity': [35, 36.2], 'temperature': [2.6, 11]}
        }

        for index, index_range in index_ranges.items():
            sal_range = index_range['salinity']
            temp_range = index_range['temperature']

            # Check if any data points fall within the specified temperature and salinity ranges
            if any((self.salinity >= sal_range[0]) & (self.salinity <= sal_range[1]) &
                   (self.temperature >= temp_range[0]) & (self.temperature <= temp_range[1])):
                ax.text(np.mean(sal_range), np.mean(temp_range), index, ha='center', va='center', rotation=45,
                        bbox=dict(facecolor='none', edgecolor='none'))


def main():
    # Path to the CSV file
    csv_file = '/home/labdino/PycharmProjects/CTDprocessing/dados/DadosHidrografia/01_radial_1/0626_28072019_1609/FILE1_10m.csv'

    # Create HydrographyDiagram object
    hydro_diagram = HydrographyDiagram(csv_file)

    # Calculate density
    hydro_diagram.calculate_density()

    # Plot the hydrography diagram
    hydro_diagram.plot_diagram()


if __name__ == "__main__":
    main()
