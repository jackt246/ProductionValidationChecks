from fscChecks import fscChecks
from fileImport import importJsons
import numpy as np
import matplotlib.pyplot as plt





if __name__ == '__main__':

    # -------------Initial parameters------------------#
    # Put in a parameters file when feeling less lazy
    # set base URL used to access VA JSON files:
    urlString = 'https://www.ebi.ac.uk/emdb/emdb-entry/emdbva/'
    # set which checks you want to run

    # -------------------------------------------------#

    # import a list of entry IDs
    with open('emdList.txt', 'r') as entryimport:
        entries = entryimport.readlines()
    entryList = []
    for line in entries:
        entryList.append(line.replace('\n', ''))

    # Initialize an empty list to accumulate normalized curve data
    normalized_curves_data = []
    # Number of desired points after normalization
    num_desired_points = 60

    for entry in entryList:
        jsonRequest = importJsons(urlString)
        jsonFile = jsonRequest.requestJsonFile(entry)

        try:
            # instantiate the fscCheck class with the jsonFile
            fscChecker = fscChecks(jsonFile)
            fscData = fscChecker.fscCurves['fsc']
            if len(fscData) > 0:
                # Normalize the curve to have num_desired_points points
                num_points = len(fscData)
                x_normalized = np.linspace(0, 1, num_desired_points)  # Normalized x-coordinates
                y_normalized = np.interp(x_normalized, np.linspace(0, 1, num_points), fscData)

                # Combine x and y coordinates into a 2D array
                normalized_curve = np.column_stack((x_normalized, y_normalized))
                normalized_curves_data.append(normalized_curve)

        except Exception as e:
            # Handle the case where fscChecks initialization failed
            print(f'no FSC for this entry ({e})')

    # Convert the accumulated normalized_curves_data list into a NumPy array
    curves_data_array = np.array(normalized_curves_data)

    num_curves = len(curves_data_array)
    num_points_per_curve = len(curves_data_array[0])

    x_coords = curves_data_array[:, :, 0].flatten()
    y_coords = curves_data_array[:, :, 1].flatten()

    # Create a 2D histogram to represent the density of paths
    plt.hist2d(x_coords, y_coords, bins=num_desired_points, cmap='RdBu')

    plt.colorbar(label='Frequency')

    plt.title('Most Common Routes Taken (Heatmap-like Representation)')
    plt.xlabel('Normalized X-axis')
    plt.ylabel('Normalized Y-axis')

    plt.show()
    plt.savefig('fscheatmap.png')