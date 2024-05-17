import os
import re
import matplotlib.pyplot as plt
import matplotlib.image as mpimg


def plot_station_images(ts_diagrams, temp_profiles, brunt_vaisala_freqs):
    """
    Plot T-S diagrams, temperature profiles, and Brunt-Vaisala frequency plots
    for each station, side by side.

    Parameters:
    ts_diagrams (list): List of file paths to T-S diagram images
    temp_profiles (list): List of file paths to temperature profile images
    brunt_vaisala_freqs (list): List of file paths to Brunt-Vaisala frequency images

    Returns:
    None
    """
    # Create a dictionary to store the images for each station
    station_data = {}  # {station_num: {'ts_diagram': file, 'temp_profile': file,...}}

    # Iterate over the T-S diagrams and extract station numbers
    for file in ts_diagrams:

        # Extract station number from file name using regular expression
        station_num = re.search(r'_(\d+).png', file).group(1)

        # Create a new entry in the station_data dictionary if it doesn't exist
        station_data.setdefault(station_num, {})['ts_diagram'] = file

    # Iterate over the temperature profiles and extract station numbers
    for file in temp_profiles:
        station_num = re.search(r'_(\d+).png', file).group(1)
        station_data.setdefault(station_num, {})['temp_profile'] = file

    # Iterate over the Brunt-Vaisala frequency files and extract station numbers
    for file in brunt_vaisala_freqs:
        station_num = re.search(r'_10m_(\d+).png', file).group(1)
        station_data.setdefault(station_num, {})['brunt_vaisala_freq'] = file

    # Plot the images for each station
    for station_num, images in station_data.items():

        # Check if all three images are present for this station
        if all(key in images for key in ['ts_diagram', 'temp_profile', 'brunt_vaisala_freq']):

            # Load the images
            ts_diagram = mpimg.imread(images['ts_diagram'])
            temp_profile = mpimg.imread(images['temp_profile'])
            brunt_vaisala_freq = mpimg.imread(images['brunt_vaisala_freq'])

            # Create figure with 3 subplots
            fig, axs = plt.subplots(1, 3, figsize=(27, 9), width_ratios=[1, 1,1])  # Set the figure size to 27x9 inches, with three equal-sized subplots

            # Plot the T-S diagram
            axs[0].imshow(ts_diagram, extent=[0, ts_diagram.shape[1], 0, ts_diagram.shape[0]])  # Set the extent of the image data
            axs[0].axis('off')  # Turn off axis labels

            # Plot the temperature profile
            axs[1].imshow(temp_profile, extent=[0, temp_profile.shape[1], 0, temp_profile.shape[0]])  # Set the extent of the image data
            axs[1].axis('off')

            # Plot the Brunt-Vaisala frequency plot
            axs[2].imshow(brunt_vaisala_freq, extent=[0, brunt_vaisala_freq.shape[1], 0, brunt_vaisala_freq.shape[0]])  # Set the extent of the image data
            axs[2].axis('off')

            # Adjust the padding around the plot
            plt.subplots_adjust(left=0.01, right=0.99, bottom=0.01, top=0.99)  # Set the padding to 5% of the figure width and height

            # Set the title for the figure
            plt.suptitle(f'Estação {station_num}', y=0.95, fontsize=35)

            plt.tight_layout()

            # Save the plot with the name "Plots_<station_number>.png"
            plt.savefig(os.path.join(save_dir, f"Plots_{station_num}.png"))

        else:

            # Print a warning if any images are missing for this station
            print(f"Warning: Missing images for station {station_num}")


# Example usage:
ts_diagrams = [r'']

temp_profiles = [r'']

brunt_vaisala_freqs = [r'']

save_dir = r''

plot_station_images(ts_diagrams, temp_profiles, brunt_vaisala_freqs)
