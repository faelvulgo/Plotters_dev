import os
import pandas as pd
import matplotlib.pyplot as plt

class CTDDataLoader:
    def __init__(self, ctd_directories):
        self.ctd_directories = ctd_directories
        self.ctd_data = {}

    def load_ctd_data(self):
        print("Starting data loading...")
        for directory in self.ctd_directories:
            print(f"Loading data from directory: {directory}")
            ctd_name = os.path.basename(directory)
            ctd_files = [file for file in os.listdir(directory) if file.endswith('.csv')]
            combined_df = pd.DataFrame()
            for file in ctd_files:
                print(f"Loading data from file: {file}")
                file_path = os.path.join(directory, file)
                try:
                    chunk_iter = pd.read_csv(file_path, skiprows=16, chunksize=500, engine='python')
                    df_chunks = []
                    for chunk in chunk_iter:
                        chunk.iloc[:, 1:] = chunk.iloc[:, 1:].astype('float16')  # Convert numeric columns to float16
                        df_chunks.append(chunk)
                    df = pd.concat(df_chunks, ignore_index=True)
                    combined_df = pd.concat([combined_df, df], ignore_index=True)
                except pd.errors.ParserError as e:
                    print(f"Error reading file {file_path}: {e}")
            self.ctd_data[ctd_name] = combined_df


class DataPlotter:
    def __init__(self, ctd_data):
        self.ctd_data = ctd_data
        self.colors = ['blue', 'green', 'red', 'purple', 'orange', 'cyan']  # Define colors for each CTD

    def plot_temperature_over_time(self):
        print("Plotting temperature over time...")
        plt.figure(figsize=(10, 6))
        color_index = 0
        for ctd_name, ctd_df in self.ctd_data.items():
            ctd_df['// timestamp(yyyy-mm-ddTHH:MM:ss.FFF)'] = pd.to_datetime(ctd_df['// timestamp(yyyy-mm-ddTHH:MM:ss.FFF)'])
            plt.plot(ctd_df['// timestamp(yyyy-mm-ddTHH:MM:ss.FFF)'], ctd_df['temperature(°C)'], label=ctd_name, color=self.colors[color_index])
            color_index += 1

        plt.xlabel('Time')
        plt.ylabel('Temperature (°C)')
        plt.title('Temperature Over Time')
        plt.legend(title='CTD')
        plt.grid(True)
        plt.show()


def main():
    ctd_directories = ["D:\InternalWaves_teste\cruzeiro2"]

    ctd_loader = CTDDataLoader(ctd_directories)
    print('Initializing...')
    print('Loading data...')
    ctd_loader.load_ctd_data()

    plotter = DataPlotter(ctd_loader.ctd_data)
    print('Data loaded.')
    print('Plotting...')
    plotter.plot_temperature_over_time()


if __name__ == "__main__":
    main()
