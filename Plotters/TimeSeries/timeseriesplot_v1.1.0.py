import os
import pandas as pd
import matplotlib.pyplot as plt


class CTDDataLoader:
    def __init__(self, ctd_directories):
        self.ctd_directories = ctd_directories
        self.ctd_data = {}

    def load_ctd_data(self):
        for directory in self.ctd_directories:
            ctd_name = os.path.basename(directory)
            ctd_files = [file for file in os.listdir(directory) if file.endswith('.csv')]
            combined_df = pd.DataFrame()
            for file in ctd_files:
                file_path = os.path.join(directory, file)
                try:
                    chunk_iter = pd.read_csv(file_path, skiprows=16, chunksize=500)
                    df_chunks = []
                    for chunk in chunk_iter:
                        chunk = chunk.fillna(0)
                        chunk = chunk.rename(columns=lambda x: x.strip())
                        df_chunks.append(chunk)
                    df = pd.concat(df_chunks, ignore_index=True)
                    combined_df = pd.concat([combined_df, df], ignore_index=True)
                except pd.errors.ParserError as e:
                    print(f"Error reading file {file_path}: {e}")
            self.ctd_data[ctd_name] = combined_df


class DataPlotter:
    def __init__(self, ctd_data):
        self.ctd_data = ctd_data

    def plot_temperature_over_time(self):
        plt.figure(figsize=(10, 6))
        for ctd_name, ctd_df in self.ctd_data.items():
            ctd_df['// timestamp(yyyy-mm-ddTHH:MM:ss.FFF)'] = pd.to_datetime(ctd_df['// timestamp(yyyy-mm-ddTHH:MM:ss.FFF)'])
            plt.plot(ctd_df['// timestamp(yyyy-mm-ddTHH:MM:ss.FFF)'], ctd_df['temperature(°C)'], label=ctd_name)

        plt.xlabel('Time')
        plt.ylabel('Temperature (°C)')
        plt.title('Temperature Over Time for 7 CTDs')
        plt.legend()
        plt.grid(True)
        plt.show()


def main():
    ctd_directories = [
        "/home/labdino/PycharmProjects/Internal_waves/dados/Cruzeiro_2/01.BoiadeTopo-75m",
        "/home/labdino/PycharmProjects/Internal_waves/dados/Cruzeiro_2/02.CTD2-325m",
        "/home/labdino/PycharmProjects/Internal_waves/dados/Cruzeiro_2/03.CTD3-525m",
        "/home/labdino/PycharmProjects/Internal_waves/dados/Cruzeiro_2/04.CTD4-755m",
        "/home/labdino/PycharmProjects/Internal_waves/dados/Cruzeiro_2/05.CTD5-975m"
    ]

    ctd_loader = CTDDataLoader(ctd_directories)
    print('Loading data...')
    ctd_loader.load_ctd_data()

    plotter = DataPlotter(ctd_loader.ctd_data)
    print('Plotting...')
    plotter.plot_temperature_over_time()

if __name__ == "__main__":
    main()
