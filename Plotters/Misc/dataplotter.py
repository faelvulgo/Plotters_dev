import pandas as pd
import matplotlib.pyplot as plt
import os


def plot_temperature_over_time(input_files):
    colors = ['blue', 'green', 'red', 'purple', 'orange', 'cyan', 'magenta']

    plt.figure(figsize=(10, 6))  # Create a single figure for all plots

    for i, input_file in enumerate(input_files):
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
    plt.show()
    plt.savefig(save_path)
    print(f"Figure saved as {save_path}")


if __name__ == "__main__":
    input_files = [r"D:\InternalWaves_teste\cruzeiro2\200423_20200228_1645_light.csv",
                   r"D:\InternalWaves_teste\cruzeiro2\200424_20200228_1608_light.csv",
                   r"D:\InternalWaves_teste\cruzeiro2\200425_20200228_1551_light.csv",
                   r"D:\InternalWaves_teste\cruzeiro2\200426_20200228_1527_light.csv",
                   r"D:\InternalWaves_teste\cruzeiro2\200427_20200228_1501_light.csv",
                   r"D:\InternalWaves_teste\cruzeiro2\200428_20200227_2329_light.csv"]
    save_path = r"D:\InternalWaves_teste\cruzeiro2"

    plot_temperature_over_time(input_files)
