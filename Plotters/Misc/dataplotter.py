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
        ctd_df[''] = pd.to_datetime(
            ctd_df[''])
        print(f'Plotting data from {input_file}...')
        plt.plot(ctd_df[''],
                 ctd_df[''],
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
    input_files = [r""]
    save_path = r""

    plot_temperature_over_time(input_files)
