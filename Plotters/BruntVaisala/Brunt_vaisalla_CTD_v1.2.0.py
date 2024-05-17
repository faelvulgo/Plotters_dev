import pandas as pd
import matplotlib.pyplot as plt
import gsw
import time
import numpy as np


def remove_rows_with_empty_cells(df):
    """
    Remove rows with empty cells (NaN values) from a DataFrame.

    Parameters:
    df (pandas.DataFrame): Input DataFrame.

    Returns:
    pandas.DataFrame: Cleaned DataFrame with rows containing empty cells removed.
    """
    # Identify rows with empty cells (NaN values) in any column
    empty_rows = df.isnull().any(axis=1)

    # Exclude rows with empty cells
    df_cleaned = df[~empty_rows]

    return df_cleaned


def bruntvaisala():
    """
    Calculate Brunt-Väisälä frequency from salinity, temperature, and pressure.

    Returns:
    tuple: A tuple containing the Brunt-Väisälä frequency and corresponding pressure values.
    """
    # Calculate absolute salinity from practical salinity (salinity, pressure, lon, lat)
    sa = gsw.conversions.SA_from_SP(salinity, pressure, 41, 23)

    # Calculate conservative temperature (absolute salinity, in-situ temperature, sea pressure)
    ct = gsw.conversions.CT_from_t(sa, temperature, pressure)

    # Calculate Brunt-Väisälä frequency (absolute salinity, conservative temperature, sea pressure, lat=None, axis=0)
    n2 = gsw.Nsquared(sa, ct, pressure)

    # Transform the tuple n2 into a pandas DataFrame and save it to a CSV file
    n2_df = pd.DataFrame({'Brunt-Väisälä Frequency': n2[0], 'Mid-Pressure': n2[1]})

    return n2


def plotvaisala(n2):
    """
    Plot the Brunt-Väisälä frequency.

    Parameters:
    n2 (tuple): A tuple containing the Brunt-Väisälä frequency and corresponding pressure values.
    """
    pressures = n2[1]  # Extract pressures
    n2_values = n2[0]  # Extract Brunt-Väisälä frequency values

    plt.figure(figsize=(7, 5))
    plt.plot(pressures, n2_values)
    plt.xlabel('Pressure (dBar)')
    plt.ylabel('Brunt-Väisälä Frequency (N^2)')
    plt.title('Brunt-Väisälä Frequency Profile - Cruise 2 - 525m')
    plt.grid(True)
    plt.tight_layout()
    plt.savefig('/home/labdino/PycharmProjects/Internal_waves/dados/Cruzeiro_2/03.CTD3-525m/bruntvaisala525m.png', format='png', dpi=900, transparent=False)
    plt.show()


def timecounter():
    """
    Execute and time each function.
    """
    start_time = time.perf_counter()
    vaisala_result = bruntvaisala()
    end_time = time.perf_counter()
    elapsed_time = end_time - start_time
    print(f"bruntvaisala elapsed time: {elapsed_time} seconds")

    start_time = time.perf_counter()
    plotvaisala(vaisala_result)
    end_time = time.perf_counter()
    elapsed_time = end_time - start_time
    print(f"plotvaisala elapsed time: {elapsed_time} seconds")


# Create the DataFrame
df = pd.read_csv('/dados/Cruzeiro_2/03.CTD3-525m/525m.csv')

# Remove rows with empty cells
new_df = remove_rows_with_empty_cells(df)
print(len(df))
print(len(new_df))
# Extract columns from the DataFrame to a NumPy array
salinity = new_df['    salinity(PSU)'].values
pressure = new_df['    pressure(dbar)'].values
temperature = new_df['    temperature(°C)'].values

timecounter()
