import numpy as np
import matplotlib.pyplot as plt
from statsmodels.nonparametric.smoothers_lowess import lowess
from scipy.signal import find_peaks

class fscChecks():
    '''This class is designed to run checks on the FSC curve of every entry staged for release. Each check should be added as a function and then called in RunChecksPerCheck.py'''
    def __init__(self, inputFile):
        self.fscFile = inputFile

        try:
            self.fscData = self.fscFile['fsc']
            self.fscCurves = self.fscData['curves']
        except KeyError as e:
            raise Exception(f"Error: Required data not found in the JSON file. {e}")

    def minValue(self):
        return min(self.fscCurves['fsc'])

    def finalValue(self):
        data = self.fscCurves['fsc']
        finalPoint = data[len(data)-1]
        return finalPoint

    def minFinalDifValue(self):
        data = self.fscCurves['fsc']
        difValue = min(self.fscCurves['fsc']) - data[len(data)-1]
        return difValue

    def gradientCheck(self, window_size=5, drop_threshold=0.7):
        data = self.fscCurves['fsc']
        try:
            max_gradient_change = 0  # Initialize maximum gradient change
            for i in range(window_size, len(data)):
                window_data = data[i - window_size: i]  # Extract data within the window
                drop_condition = abs(window_data[-1] - window_data[0]) > drop_threshold
                if drop_condition:
                    differences = [window_data[j] - window_data[j - 1] for j in range(1, window_size)]
                    average_difference = sum(differences) / (window_size - 1)
                    if abs(average_difference) > max_gradient_change:
                        max_gradient_change = abs(average_difference)

            return max_gradient_change
        except Exception as e:
            raise Exception(f"Failed to find the largest gradient change {e}")

    def peakFinder(self):
        # start by smoothing the line

        # Example dataset (replace this with your actual data)
        originalData = self.fscCurves['fsc']

        # Fraction of points used to fit each local regression
        fraction = 0.05

        # Apply LOESS smoothing to the data
        smoothed_data = lowess(originalData, range(len(originalData)), frac=fraction)[:, 1]

        #  Find peaks in the smoothed data
        peaks, _ = find_peaks(smoothed_data, distance=5, prominence=0.1)  # Adjust distance parameter as needed

        # Plotting the original and smoothed data
        # plt.figure(figsize=(8, 6))
        # plt.plot(originalData, label='Original Data')
        # plt.plot(smoothed_data, label='Smoothed Data')
        # plt.plot(peaks, smoothed_data[peaks], 'r.', markersize=10, label='Detected Peaks')
        # plt.legend()
        # plt.title('Smoothing Data with LOESS')
        # plt.xlabel('Data Points')
        # plt.ylabel('Values')
        # plt.savefig('{}peaks.png'.format(entry))
        # plt.show()
        return len(peaks)
    def fscPlotter(self, filepath):
        try:
            plt.figure()
            fsc_values = self.fscCurves['fsc']
            plt.plot(range(len(fsc_values)), fsc_values)
            plt.title(filepath)
            plt.savefig('{}.png'.format(filepath))
            plt.close()  # Close the figure to free up memory
        except FileNotFoundError as e:
            print(f"FileNotFoundError: {e}")
            print('Failed to save figure. File not found.')
        except Exception as e:
            print(f"Error: {e}")
            print('Failed to save figure.')