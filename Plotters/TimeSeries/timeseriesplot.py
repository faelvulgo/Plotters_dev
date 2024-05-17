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
            ctd_files = os.listdir(directory)
            self.ctd_data[ctd_name] = pd.DataFrame()

            # Carregar os dados CSV para cada CTD
            self.ctd_data[ctd_name] = pd.DataFrame()
            for file in ctd_files:
                if file.endswith('.csv'):
                    file_path = os.path.join(directory, file)
                    try:
                        chunk_iter = pd.read_csv(file_path, skiprows=16, chunksize=1000)  # Adjust chunksize as needed
                        df_chunks = []
                        for chunk in chunk_iter:
                            chunk = chunk.fillna(0)
                            chunk = chunk.rename(columns=lambda x: x.strip())
                            df_chunks.append(chunk)
                        self.ctd_data[ctd_name] = pd.concat(df_chunks, ignore_index=True)
                    except pd.errors.ParserError as e:
                        print(f"Erro ao ler o arquivo {file_path}: {e}")

    @staticmethod
    def _read_csv(file_path):
        return pd.read_csv(file_path, skiprows=16)

    def _process_data(self, df, ctd_name):
        df = df.fillna(0)
        columns_to_convert = [col for col in df.columns if col != 'timestamp(yyyy-mm-ddTHH:MM:ss.FFF)']
        df[columns_to_convert] = df[columns_to_convert].apply(pd.to_numeric, errors='coerce')
        df = df.rename(columns=lambda x: x.strip())
        self.ctd_data[ctd_name] = pd.concat([self.ctd_data[ctd_name], df], ignore_index=True)


class DataPlotter:
    def __init__(self, ctd_data):
        self.ctd_data = ctd_data

    def plot_temperature_over_time(self):
        plt.figure(figsize=(10, 6))
        for ctd_name, ctd_df in self.ctd_data.items():
            ctd_df['// timestamp(yyyy-mm-ddTHH:MM:ss.FFF)'] = ctd_df['// timestamp(yyyy-mm-ddTHH:MM:ss.FFF)'].astype(str)
            plt.plot(ctd_df['// timestamp(yyyy-mm-ddTHH:MM:ss.FFF)'], ctd_df['temperature(°C)'], label=ctd_name)

        plt.xlabel('Tempo')
        plt.ylabel('Temperatura (°C)')
        plt.title('Temperatura ao Longo do Tempo para os 7 CTDs')
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
