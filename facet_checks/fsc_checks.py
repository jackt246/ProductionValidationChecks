import numpy as np
from statsmodels.nonparametric.smoothers_lowess import lowess
from scipy.signal import find_peaks

class fscChecks():
    '''This class is designed to run checks on the FSC curve of every entry staged for release. Each check should be added as a function and then called in RunChecksPerCheck.py'''
    def __init__(self, inputFile):
        self.json = inputFile

        try:
            self.fscData = self.json['fsc']
            self.fscCurves = self.fscData['curves']
            self.fscRelion = self.json['relion_fsc']['curves']
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
        difValue = data[len(data)-1] - min(self.fscCurves['fsc'])
        return difValue

    def largeDropCheck(self, window_size=5, drop_threshold=0.7):
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

    def maxGradientCheck(self, window_size=5):
        data = self.fscCurves['fsc']
        max_change = float('-inf')  # Initialize with negative infinity for comparison
        for i in range(window_size, len(data)):
            window_data = data[i - window_size: i]  # Extract data within the window
            differences = [window_data[j] - window_data[j - 1] for j in range(1, window_size)]
            average_difference = sum(differences) / (window_size - 1)
            max_change = max(max_change, abs(average_difference))

        return max_change

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

        return len(peaks)

    def compare_phase_masked(self):
        fsc_phaserandom = self.fscRelion['phaserandmization']
        fsc_masked = self.fscRelion['fsc_masked']

        fsc_phaserandom_intergral = np.trapz(fsc_phaserandom)
        fsc_masked_integral = np.trapz(fsc_masked)

        intergral_div = fsc_masked_integral / fsc_phaserandom_intergral

        return intergral_div