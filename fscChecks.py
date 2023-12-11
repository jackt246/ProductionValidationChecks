import numpy as np


class fscChecks():
    '''This class is designed to run checks on the FSC curve of every entry staged for release. Each check should be added as a function and then called in main.py'''
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

    def gradientCheck(self):
        #look for curves which increase in correlation after already hitting a minimum
        #Start by defining x and y values
        y = np.array(self.fscCurves['fsc'])
        x = np.arange(len(y))

        #determine the minimum value after which we should look at correlation
        initial_drop_index = np.argmin(y)

        if initial_drop_index != len(y) - 1:
            total_values = len(y)
            half_index = total_values // 2

            y_first_half = y[:half_index]
            y_second_half = y[half_index:]

            # Create x values corresponding to the length of the y values
            x_values = np.arange(total_values)

            # Perform linear regression for both segments
            slope_first_half, _ = np.polyfit(np.arange(len(y_first_half)), y_first_half, 1)
            slope_second_half, _ = np.polyfit(np.arange(len(y_second_half)), y_second_half, 1)

            return abs(np.round(slope_second_half, 3))
        else:
            print('The initial drop index is the last index in the data. The gradient is set to 0')
            return 0

    def zeroCheck(self):
        #check whether the FSC curve reaches zero
        print('a')
    def subZeroCheck(self):
        #check whether FSC curve drops significantly below 0
        print('a')
