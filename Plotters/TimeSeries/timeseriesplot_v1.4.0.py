import pandas as pd
import matplotlib.pyplot as plt
import os


class LighterData:
    def __init__(self, input_files, output_files, chunksize=500):
        self.input_files = input_files
        self.output_files = output_files
        self.chunksize = chunksize

    def make_data_lighter(self):
        for input_file, output_file in zip(self.input_files, self.output_files):
            print(f"Making data lighter for {input_file}...")
            for chunk in pd.read_csv(input_file, skiprows=16, chunksize=self.chunksize):
                # Exclude non-numeric columns
                numeric_columns = [col for col in chunk.columns if col != '// timestamp(yyyy-mm-ddTHH:MM:ss.FFF)']

                if numeric_columns:
                    # Convert numeric columns to float16
                    chunk[numeric_columns] = chunk[numeric_columns].astype('float16')

                    # Append processed chunk to the output file
                    chunk.to_csv(output_file, mode='a', header=not os.path.exists(output_file), index=False)

        print("Process complete.")


class DataPlotter:
    def __init__(self, input_files, save_path=None):
        self.input_files = input_files
        self.save_path = save_path

    def plot_temperature_over_time(self):
        colors = ['blue', 'green', 'red', 'purple', 'orange', 'cyan', 'magenta']

        plt.figure(figsize=(10, 6))  # Create a single figure for all plots

        for i, input_file in enumerate(self.input_files):
            print(f"Reading processed data from {input_file}...")
            ctd_data = pd.read_csv(input_file)

            # Plot temperature over time for the current file using a different color
            ctd_df = ctd_data.copy()  # Make a copy to avoid modifying the original DataFrame
            ctd_df['// timestamp(yyyy-mm-ddTHH:MM:ss.FFF)'] = pd.to_datetime(
                ctd_df['// timestamp(yyyy-mm-ddTHH:MM:ss.FFF)'])
            print(f'Plotting data from {input_file}...')
            plt.plot(ctd_df['// timestamp(yyyy-mm-ddTHH:MM:ss.FFF)'],
                     ctd_df['temperature(°C)'],
                     label=os.path.basename(input_file),  # Use the file name as label
                     color=colors[i % len(colors)])  # Cycle through colors list

        plt.xlabel('Time')
        plt.ylabel('Temperature (°C)')
        plt.title('Temperature Over Time')
        plt.legend(title='File')
        plt.grid(True)

        # Save the figure if save_path is provided
        if self.save_path:
            plt.savefig(self.save_path)
            print(f"Figure saved as {self.save_path}")
        else:
            plt.show()


if __name__ == "__main__":
    input_files = []

    output_files = []

    lighter = LighterData(
        input_files=input_files,
        output_files=output_files
    )

    lighter.make_data_lighter()

    save_path = r""

    plotter = DataPlotter(input_files, save_path)

    plotter.plot_temperature_over_time()
