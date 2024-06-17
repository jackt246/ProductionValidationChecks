class fscChecks():
    '''This class is designed to run checks on the FSC curve of every entry staged for release. Each check should be added as a function and then called in RunChecksPerCheck.py'''
    def __init__(self, inputFile):
        self.json = inputFile

        try:
            self.rapsData = self.json['raps']
            self.fscCurves = self.fscData['curves']
        except KeyError as e:
            raise Exception(f"Error: Required data not found in the JSON file. {e}")

    def maxGradientCheck(self, window_size=5):
        data = self.fscCurves['fsc']
        max_change = float('-inf')  # Initialize with negative infinity for comparison
        for i in range(window_size, len(data)):
            window_data = data[i - window_size: i]  # Extract data within the window
            differences = [window_data[j] - window_data[j - 1] for j in range(1, window_size)]
            average_difference = sum(differences) / (window_size - 1)
            max_change = max(max_change, abs(average_difference))

        return max_change