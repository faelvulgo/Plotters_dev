import os
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
from gsw import SA_from_SP, CT_from_t, rho as gsw_rho


class HydrographyDiagram:
    def __init__(self, csv_files):
        """
        Initialize the HydrographyDiagram object with data from CSV files.

        Args:
        csv_files (list): List of paths to CSV files containing hydrographic data.
        """
        self.data_list = [pd.read_csv(csv_file) for csv_file in csv_files]
        self.salinity_list = [data['Calc. SALINITY; PSU'].values for data in self.data_list]
        self.temperature_list = [data['TEMPERATURE;C'].values for data in self.data_list]
        self.pressure_list = [data['PRESSURE;DBAR'].values for data in self.data_list]

    def calculate_density(self):
        """
        Calculate density based on salinity, temperature, and pressure data.
        """
        self.sa_list = [SA_from_SP(salinity, pressure, 42, 24) for salinity, pressure in zip(self.salinity_list, self.pressure_list)]
        self.ct_list = [CT_from_t(sa, temperature, pressure) for sa, temperature, pressure in zip(self.sa_list, self.temperature_list, self.pressure_list)]
        self.density_list = [gsw_rho(sa, ct, pressure) for sa, ct, pressure in zip(self.sa_list, self.ct_list, self.pressure_list)]

    def plot_diagram(self, save_dir):
        """
        Plot the hydrography diagram and save it in a directory.

        Args:
        save_dir (str): Path to the directory to save the plots.
        """
        os.makedirs(save_dir, exist_ok=True)  # Create directory if it doesn't exist

        for i, data in enumerate(self.data_list):
            fig, ax = plt.subplots()

            # Scatter plot
            norm = plt.Normalize(self.pressure_list[i].min(), self.pressure_list[i].max())
            scatter = ax.scatter(self.salinity_list[i], self.temperature_list[i], c=self.pressure_list[i], cmap='viridis', norm=norm, marker='o', s=20)

            # Contour lines
            salinity_reshaped = np.linspace(self.salinity_list[i].min(), self.salinity_list[i].max(), 100)
            temperature_reshaped = np.linspace(self.temperature_list[i].min(), self.temperature_list[i].max(), 100)
            salinity_grid, temperature_grid = np.meshgrid(salinity_reshaped, temperature_reshaped)
            density_grid = gsw_rho(salinity_grid, temperature_grid, np.zeros_like(salinity_grid))
            contour = ax.contour(salinity_grid, temperature_grid, density_grid, colors='black')
            contour_labels = ax.clabel(contour, inline=True, fontsize=8, fmt='%.1f')

            # Water mass labels
            self._plot_water_mass_labels(ax, i)

            # Set labels and title
            ax.set_xlabel('Salinity (PSU)')
            ax.set_ylabel('Temperature ($^\circ$C)')
            ax.set_title(f'Diagrama T-S - Radial {i+1} - 0630')

            # Set axis limits
            ax.set_xlim(34.32, 37.36)
            ax.set_ylim(2.95, 24.64)

            # Colorbar
            cbar = plt.colorbar(scatter, ax=ax, label='Pressure (dBar)')

            plt.tight_layout()

            # Save the plot
            plot_name = os.path.join(save_dir, f'watermass_{i}.png')
            plt.savefig(plot_name, format='png', dpi=900, transparent=False)
            plt.close()

    def _plot_water_mass_labels(self, ax, index):
        """
        Plot water mass labels within specified temperature and salinity ranges.

        Args:
        ax (matplotlib.axes.Axes): Axes object for plotting.
        index (int): Index of the data set.
        """
        index_ranges = {
            'WNACW': {'salinity': [35, 36.7], 'temperature': [7, 20]},
            'ENACW': {'salinity': [35.2, 36.7], 'temperature': [8, 18]},
            'SACW': {'salinity': [34.3, 35.8], 'temperature': [5, 18]},
            'WASIW': {'salinity': [34, 35.1], 'temperature': [3, 9]},
            'EASIW': {'salinity': [34.4, 35.3], 'temperature': [3, 9]},
            'MW': {'salinity': [35, 36.2], 'temperature': [2.6, 11]}
        }

        for mass_name, index_range in index_ranges.items():
            sal_range = index_range['salinity']
            temp_range = index_range['temperature']

            # Check if any data points fall within the specified temperature and salinity ranges
            if any((self.salinity_list[index] >= sal_range[0]) & (self.salinity_list[index] <= sal_range[1]) &
                   (self.temperature_list[index] >= temp_range[0]) & (self.temperature_list[index] <= temp_range[1])):
                ax.text(np.mean(sal_range), np.mean(temp_range), mass_name, ha='center', va='center', rotation=45,
                        bbox=dict(facecolor='none', edgecolor='none'))


def main():
    # List of paths to the CSV files
    csv_files = [
        '/home/labdino/PycharmProjects/CTDprocessing/dados/DadosHidrografia/01_radial_1/0630_29072019_0410/FILE5_10m.csv',
        # Add more CSV files here if needed
    ]

    # Create HydrographyDiagram object
    hydro_diagram = HydrographyDiagram(csv_files)

    # Calculate density
    hydro_diagram.calculate_density()

    # Plot the hydrography diagrams and save them in unique directories
    for i, csv_file in enumerate(csv_files):
        save_dir = os.path.dirname(csv_file)  # Directory to save the plots
        hydro_diagram.plot_diagram(os.path.join(save_dir, f'radial_{i+1}'))

if __name__ == "__main__":
    main()
