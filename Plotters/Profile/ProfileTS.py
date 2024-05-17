import os
import pandas as pd
import matplotlib.pyplot as plt

class HydrographyPlotter:
    def __init__(self, csv_files):
        """
        Initialize HydrographyPlotter object with a list of CSV file paths.

        Args:
        csv_files (list): List of paths to CSV files containing hydrographic data.
        """
        self.csv_files = csv_files

    def plot_profiles(self, save_dir):
        """
        Plot temperature and salinity profiles for each CSV file and save them in the specified directory.

        Args:
        save_dir (str): Path to the directory to save the plots.
        """
        for csv_file in self.csv_files:
            station_number = os.path.basename(os.path.dirname(csv_file)).split('_')[0]
            self._plot_profile(csv_file, save_dir, station_number)

    def _plot_profile(self, csv_file, save_dir, station_number):
        """
        Plot temperature and salinity profile from a single CSV file.

        Args:
        csv_file (str): Path to the CSV file containing hydrographic data.
        save_dir (str): Path to the directory to save the plot.
        station_number (str): Station number extracted from the folder name.
        """
        df = pd.read_csv(csv_file)

        # Extract relevant columns
        temperature = df['']
        salinity = df['']
        depth = df['']

        # Create the plot
        fig, ax1 = plt.subplots(figsize=(10, 6))

        # Plot Temperature on the first x-axis and pressure on the y-axis
        ax1.set_xlabel('Temperatura ($^\circ$C)', color='tab:blue')
        ax1.set_ylabel('Profundidade (m)', color='tab:blue')
        ax1.plot(temperature, depth, color='tab:blue', label='Temperature')

        # Create the second x-axis for Salinity
        ax2 = ax1.twiny()
        ax2.set_xlabel('Salinidade', color='tab:orange')
        ax2.plot(salinity, depth, color='tab:orange', label='Salinity')

        # Invert the y-axis
        ax1.invert_yaxis()

        # Set the title
        plt.title(f'Perfil de Temperatura e Salinidade - {station_number}')

        # Set the y-axis label
        plt.ylabel('Profundidade (m)')

        # Adjust layout
        fig.tight_layout()

        # Add legend
        fig.legend(loc='upper right', bbox_to_anchor=(1, 1))

        # Save the plot as PNG image
        plot_name = os.path.join(save_dir, f'PerfilTS_{station_number}.png')
        plt.savefig(plot_name, format='png', dpi=900, transparent=False)

def main():
    # List of paths to the CSV files
    csv_files = ['']

    # Directory to save the plots
    save_dir = ''

    # Create HydrographyPlotter object
    plotter = HydrographyPlotter(csv_files)

    # Plot and save profiles
    plotter.plot_profiles(save_dir)


if __name__ == "__main__":
    main()
