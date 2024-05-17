import os
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
from gsw import SA_from_SP, CT_from_t, sigma0 as gsw_sigma0

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

    def calculate_potential_density(self):
        """
        Calculate potential density based on salinity, temperature, and pressure data.
        """
        self.sa_list = [SA_from_SP(salinity, pressure, 40, 22) for salinity, pressure in zip(self.salinity_list, self.pressure_list)]
        self.ct_list = [CT_from_t(sa, temperature, pressure) for sa, temperature, pressure in zip(self.sa_list, self.temperature_list, self.pressure_list)]
        self.potential_density_list = [gsw_sigma0(sa, ct) for sa, ct, pressure in zip(self.sa_list, self.ct_list, self.pressure_list)]

    def plot_diagram(self, save_dir, csv_files):
        """
        Plot the hydrography diagram and save it in a directory.

        Args:
        save_dir (str): Path to the directory to save the plots.
        """
        water_masses = {
            'AS': {'T': (20, np.inf), 'S': (36, np.inf)},
            'ACAS': {'T': (6, 20), 'S': (34.6, 36)},
            'AIA': {'T': (3, 6), 'S': (34.2, 34.6)},
            'APAN': {'T': (-np.inf, 3), 'S': (34.6, 36)}
        }

        for i, (data, csv_file) in enumerate(zip(self.data_list, csv_files)):
            fig, ax = plt.subplots()

            # Scatter plot
            norm = plt.Normalize(self.pressure_list[i].min(), self.pressure_list[i].max())
            scatter = ax.scatter(self.salinity_list[i], self.temperature_list[i], c=self.pressure_list[i],
                                 cmap='viridis', norm=norm, marker='o', s=20)

            # Contour lines
            salinity_reshaped = np.linspace(self.salinity_list[i].min(), self.salinity_list[i].max(), 100)
            temperature_reshaped = np.linspace(self.temperature_list[i].min(), self.temperature_list[i].max(), 100)
            salinity_grid, temperature_grid = np.meshgrid(salinity_reshaped, temperature_reshaped)
            potential_density_grid = gsw_sigma0(salinity_grid, CT_from_t(salinity_grid, temperature_grid,
                                                                         np.zeros_like(salinity_grid)))
            contour = ax.contour(salinity_grid, temperature_grid, potential_density_grid, levels=[25.7, 26.8, 27.5],
                                 colors='black')
            contour_labels = ax.clabel(contour, inline=True, fontsize=8, fmt='%.1f')

            # Set labels and title
            ax.set_xlabel('Salinity (PSU)')
            ax.set_ylabel('Temperature ($^\circ$C)')
            station_number = os.path.basename(os.path.dirname(csv_file)).split('_')[0]
            ax.set_title(f'Diagrama T-S (potential density) - Radial 3 - {station_number}')

            # Set axis limits
            ax.set_xlim(34.32, 37.36)
            ax.set_ylim(2.95, 24.64)

            # Colorbar
            cbar = plt.colorbar(scatter, ax=ax, label='Pressure (dBar)')

            # Add water mass labels
            for name, props in water_masses.items():
                indices = np.where(np.logical_and(data['TEMPERATURE;C'].values > props['T'][0],
                                                  data['TEMPERATURE;C'].values <= props['T'][1]) &
                                   np.logical_and(data['Calc. SALINITY; PSU'].values > props['S'][0],
                                                  data['Calc. SALINITY; PSU'].values <= props['S'][1]))[0]
                if indices.size > 0:
                    avg_salinity = np.mean(data['Calc. SALINITY; PSU'].values[indices])
                    avg_temperature = np.mean(data['TEMPERATURE;C'].values[indices])
                    ax.text(avg_salinity, avg_temperature, name, fontsize=10, color='black', ha='center', va='center', weight='bold')

            plt.tight_layout()

            # Save the plot with the appropriate station number
            plot_name = os.path.join(save_dir, f'watermass_{station_number}.png')
            plt.savefig(plot_name, format='png', dpi=900, transparent=False)
            plt.close()

def main():
    # List of paths to the CSV files
    csv_files = [
        '/home/labdino/PycharmProjects/CTDprocessing/dados/DadosHidrografia/03_radial_2/0640_31072019_0003/FILE28_10m.csv'
    ]

    # Directory to save the plots
    save_dir = '/home/labdino/PycharmProjects/CTDprocessing/dados/Plots/TSdiagrams'

    # Create HydrographyDiagram object
    hydro_diagram = HydrographyDiagram(csv_files)

    # Calculate potential density
    hydro_diagram.calculate_potential_density()

    # Plot the hydrography diagrams and save them
    hydro_diagram.plot_diagram(save_dir, csv_files)

if __name__ == "__main__":
    main()