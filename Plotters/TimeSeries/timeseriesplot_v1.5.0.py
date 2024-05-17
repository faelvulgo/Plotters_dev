import pandas as pd
import matplotlib.pyplot as plt
import os


class LighterData:
    """
    A class to lighten data by converting numeric columns to float16.

    Attributes:
        input_files (list of str): List of input file paths.
        output_files (list of str): List of output file paths.
        chunksize (int): Size of data chunks to process at a time.
    """

    def __init__(self, input_files, output_files, chunksize=500):
        """
        Initializes LighterData with input and output file paths and chunk size.

        Args:
            input_files (list of str): List of input file paths.
            output_files (list of str): List of output file paths.
            chunksize (int, optional): Size of data chunks to process at a time. Default is 500.
        """
        self.input_files = input_files
        self.output_files = output_files
        self.chunksize = chunksize

    def make_data_lighter(self):
        """
        Lightens the data by converting numeric columns to float16 and saves the processed data to output files.
        """
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
    """
    A class to plot temperature over time from multiple files.

    Attributes:
        input_files2 (list of str): List of file paths containing processed data.
        save_path (str): File path to save the plot.
    """

    def __init__(self, input_files2, save_path=None):
        """
        Initializes DataPlotter with input file paths and save path for the plot.

        Args:
            input_files2 (list of str): List of file paths containing processed data.
            save_path (str, optional): File path to save the plot. Default is None.
        """
        self.input_files2 = input_files2
        self.save_path = save_path

    def plot_temperature_over_time(self):
        """
        Plots temperature over time for each file in input_files2 and saves the plot if save_path is provided.
        """
        colors = ['blue', 'green', 'red', 'purple', 'orange', 'cyan', 'magenta']

        plt.figure(figsize=(10, 6))  # Create a single figure for all plots

        for i, input_file2 in enumerate(self.input_files2):
            print(f"Reading processed data from {input_file2}...")
            ctd_data = pd.read_csv(input_file2)

            # Plot temperature over time for the current file using a different color
            ctd_df = ctd_data.copy()  # Make a copy to avoid modifying the original DataFrame
            ctd_df['// timestamp(yyyy-mm-ddTHH:MM:ss.FFF)'] = pd.to_datetime(
                ctd_df['// timestamp(yyyy-mm-ddTHH:MM:ss.FFF)'])
            print(f'Plotting data from {input_file2}...')
            plt.plot(ctd_df['// timestamp(yyyy-mm-ddTHH:MM:ss.FFF)'],
                     ctd_df['    temperature(°C)'],
                     label=os.path.basename(input_file2),  # Use the file name as label
                     color=colors[i % len(colors)])  # Cycle through colors list

        plt.xlabel('Time')
        plt.ylabel('Temperature (°C)')
        plt.title('Temperature Over Time')
        plt.legend(title='File', bbox_to_anchor=(1.05, 1), loc='upper left')  # Move legend outside the plot
        plt.grid(True)

        # Save the figure if save_path is provided
        if self.save_path:
            plt.savefig(self.save_path, bbox_inches='tight')  # Ensure legend is saved
            print(f"Figure saved as {self.save_path}")
        else:
            plt.show()


if __name__ == "__main__":
    '''
    input_files = [
        r"/home/labdino/PycharmProjects/Internal_waves/dados/Cruzeiro_3/01.BoiadeTopo-150m/200428_20200619_2330_150m.csv",
        r"/home/labdino/PycharmProjects/Internal_waves/dados/Cruzeiro_3/02.CTD2-325m/200427_20200619_2241_325m.csv",
        r"/home/labdino/PycharmProjects/Internal_waves/dados/Cruzeiro_3/03.CTD3-525m/200426_20200619_2256_525m.csv",
        r"/home/labdino/PycharmProjects/Internal_waves/dados/Cruzeiro_3/04.CTD4-600m/200429_20200619_2313_600m.csv",
        r"/home/labdino/PycharmProjects/Internal_waves/dados/Cruzeiro_3/05.CTD5-755m/200425_20200619_2223_755m.csv",
        r"/home/labdino/PycharmProjects/Internal_waves/dados/Cruzeiro_3/06.CTD6-975m/200423_20200619_2147_975m.csv",
        r"/home/labdino/PycharmProjects/Internal_waves/dados/Cruzeiro_3/07.BoiadeTopo-1125m/200424_20200619_2205_1125m.csv"
        ]

    output_files = [
        r"/home/labdino/PycharmProjects/Internal_waves/dados/Cruzeiro_3/01.BoiadeTopo-150m/150m.csv",
        r"/home/labdino/PycharmProjects/Internal_waves/dados/Cruzeiro_3/02.CTD2-325m/325m.csv",
        r"/home/labdino/PycharmProjects/Internal_waves/dados/Cruzeiro_3/03.CTD3-525m/525m.csv",
        r"/home/labdino/PycharmProjects/Internal_waves/dados/Cruzeiro_3/04.CTD4-600m/600m.csv",
        r"/home/labdino/PycharmProjects/Internal_waves/dados/Cruzeiro_3/05.CTD5-755m/755m.csv",
        r"/home/labdino/PycharmProjects/Internal_waves/dados/Cruzeiro_3/06.CTD6-975m/975m.csv",
        r"/home/labdino/PycharmProjects/Internal_waves/dados/Cruzeiro_3/07.BoiadeTopo-1125m/1125m.csv"
        ]

    lighter = LighterData(
        input_files=input_files,
        output_files=output_files
    )

    lighter.make_data_lighter()
    '''
    input_files2 = [
        r"/home/labdino/PycharmProjects/Internal_waves/dados/Cruzeiro_2/01.BoiadeTopo-75m/75m.csv",
        r"/home/labdino/PycharmProjects/Internal_waves/dados/Cruzeiro_2/02.CTD2-325m/325m.csv",
        r"/home/labdino/PycharmProjects/Internal_waves/dados/Cruzeiro_2/03.CTD3-525m/525m.csv",
        r"/home/labdino/PycharmProjects/Internal_waves/dados/Cruzeiro_2/04.CTD4-755m/755m.csv",
        r"/home/labdino/PycharmProjects/Internal_waves/dados/Cruzeiro_2/05.CTD5-975m/975m.csv",
        r"/home/labdino/PycharmProjects/Internal_waves/dados/Cruzeiro_2/06.BoiadeProfundidade-1125m/1125m.csv"]

    save_path = r"/dados/Cruzeiro_2/cruzeiro2_temperatura.png"

    plotter = DataPlotter(input_files2, save_path)

    plotter.plot_temperature_over_time()
