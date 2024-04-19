import matplotlib.pyplot as plt
import numpy as np
import json
import csv


def openJson(filePath):
    # Open the JSON file and read its contents
    with open(filePath, 'r') as file:
        # Load JSON data
        return json.load(file)

def graphPlotter(data, filePath, outliers=None):
    plt.figure()
    if outliers:
        outlier_indices = [i for i, val in enumerate(data) if val < outliers[0] or val > outliers[1]]
        normal_indices = [i for i in range(len(data)) if i not in outlier_indices]
        plt.scatter(normal_indices, [data[i] for i in normal_indices], label='Normal Data', color='blue')
        plt.scatter(outlier_indices, [data[i] for i in outlier_indices], label='Outliers', color='red')
    else:
        plt.scatter(range(len(data)), data)
    plt.title(filePath)
    plt.legend()  # Show legend if plotting outliers separately
    plt.savefig('{}.png'.format(filePath))
    plt.close()

def calcPercentileRange(data, percentileBot, percentileTop):
    # Calculate the 1st and 99th percentiles
    percentile_bot = np.percentile(data, percentileBot)
    percentile_top = np.percentile(data, percentileTop)

    return percentile_bot, percentile_top

# ------- parameters --------#
# open the json file
jsonFile = openJson('checkJSON_staging.json')
plotGraphs = False

#FSC thresholds:
minThreshold = -0.1
finalThreshold = 0.1
peakThreshold = 3
gradientThreshold = 0.1

#Q-score threshold
qScoreThreshold = 0.3

#Masking threshold

maskingThreshold = 21
paddingThreshold = 5

# ------ start code ------- #
# create some containers for data that we can plot later on if we want
fscMinValues = []
fscFinalValues = []
fscPeakNum = []
fscGradient = []

qScorePropUnderZero = []

proportionMasked = []
maskedHor = []
maskedVer = []
maskingIssues = []
paddingIssue = []


entriesWithIssues = {}

for emdCode, emdData in jsonFile.items():
    entriesWithIssues[emdCode] = {'issues': {}}
    if 'FSC' in emdData:
        if 'Min Value' in emdData['FSC']:
            fscMinValues.append(emdData['FSC']['Min Value'])
            if emdData['FSC']['Min Value'] < minThreshold:
                entriesWithIssues[emdCode]['issues']['FSCminValue'] = emdData['FSC']['Min Value']
        if 'Final Value' in emdData['FSC']:
            fscFinalValues.append(emdData['FSC']['Final Value'])
            if emdData['FSC']['Final Value'] > finalThreshold:
                entriesWithIssues[emdCode]['issues']['FSCfinalValue'] = emdData['FSC']['Final Value']
        if 'Detected Peaks' in emdData['FSC']:
            fscPeakNum.append(emdData['FSC']['Detected Peaks'])
            if emdData['FSC']['Detected Peaks'] > peakThreshold:
                entriesWithIssues[emdCode]['issues']['FSCpeakValue'] = emdData['FSC']['Detected Peaks']
        if 'largest gradient' in emdData['FSC']:
            fscGradient.append(emdData['FSC']['largest gradient'])
            if emdData['FSC']['largest gradient'] > gradientThreshold:
                entriesWithIssues[emdCode]['issues']['FSCgradientValue'] = emdData['FSC']['largest gradient']

        if 'missingFSC' in emdData['FSC']:
            entriesWithIssues[emdCode]['issues']['missingFSC'] = emdData['FSC']['missingFSC']

    if 'qScore' in emdData:
        if 'ProportionUnderZero' in emdData['qScore']:
            qScorePropUnderZero.append(emdData['qScore']['ProportionUnderZero'])
            if emdData['qScore']['ProportionUnderZero'] > qScoreThreshold:
                entriesWithIssues[emdCode]['issues']['qScoreProportionUnderZero'] = emdData['qScore']['ProportionUnderZero']

    if 'ImageChecks' in emdData:
        if 'ProportionMasked' in emdData['ImageChecks']:
            proportionMasked.append(emdData['ImageChecks']['ProportionMasked'])
            maskedHor.append(emdData['ImageChecks']['Mask Difference Horizontal'])
            maskedVer.append(emdData['ImageChecks']['Mask Difference Vertical'])

            if emdData['ImageChecks']['ProportionMasked'] > maskingThreshold:
                entriesWithIssues[emdCode]['issues']['Masking'] = emdData['ImageChecks']['ProportionMasked']
                if abs(emdData['ImageChecks']['Mask Difference Horizontal']) > paddingThreshold and abs(emdData['ImageChecks']['Mask Difference Vertical']) > paddingThreshold:
                    entriesWithIssues[emdCode]['issues']['Padding'] = 'Possible'
                    maskingIssues.append(emdCode)

    if not entriesWithIssues[emdCode]['issues']:  # Check if no issues reported
        del entriesWithIssues[emdCode]  # Remove entry if no issues found

with open('jsonCheckOutputs/entriesWithIssues.json', 'w') as json_file:
    json.dump(entriesWithIssues, json_file)

with open('jsonCheckOutputs/maskingIssues.csv', 'w', newline='') as csvfile:
    csv_writer = csv.writer(csvfile)
    for value in maskingIssues:
        csv_writer.writerow([value])

with open('jsonCheckOutputs/paddingIssues.csv', 'w', newline='') as csvfile:
    csv_writer = csv.writer(csvfile)
    for value in paddingIssue:
        csv_writer.writerow([value])


# ---- Outliers ----- #

# FSC
#minPercentileBot, minPercentilMax = calcPercentileRange(fscMinValues, 1, 99)
#finalPercentileBot, finalPercentilMax = calcPercentileRange(fscFinalValues, 0, 99)
#peakPercentileBot, peakPercentilMax = calcPercentileRange(fscPeakNum, 0, 99)
#gradPercentileBot, gradPercentilMax = calcPercentileRange(fscGradient, 0, 99)

# Qscore

#qscorePercentileBot, qscorePercentilMax = calcPercentileRange(qScorePropUnderZero, 99)

# Masking

#maskedPercentileBot, maskedPercentilMax = calcPercentileRange(proportionMasked, 0, 96)

#plt.figure()
#plt.plot()

# ------ graph plotting ------- #
if plotGraphs is True:
    # FSC
    graphPlotter(fscMinValues, 'jsonCheckOutputs/fscMinValues', (minPercentileBot, minPercentilMax))
    graphPlotter(fscFinalValues, 'jsonCheckOutputs/fscFinalValues', (finalPercentileBot, finalPercentilMax))
    graphPlotter(fscPeakNum, 'jsonCheckOutputs/fscPeakNum', (peakPercentileBot, peakPercentilMax))
    graphPlotter(fscGradient, 'jsonCheckOutputs/fscGradient', (gradPercentileBot, gradPercentilMax))

    # qscore
    #graphPlotter(qScorePropUnderZero, 'jsonCheckOutputs/qScorePropUnderZero', (qscorePercentileBot, qscorePercentilMax))

    # masking
    graphPlotter(proportionMasked, 'jsonCheckOutputs/proportionMasked')
    # plot the padding
    plt.figure()
    print()
    plt.scatter(maskedVer, maskedHor)
    # Draw a square with a side length of 5
    square_side = 10
    square = plt.Rectangle((0 - (square_side/2), 0 - (square_side/2)), square_side, square_side, linewidth=1, edgecolor='r', facecolor='none')
    plt.gca().add_patch(square)
    plt.savefig('jsonCheckOutputs/horandVert.png')

    ## ---- box plot ---- ##

    # Combine all lists
    all_data = [fscMinValues, fscFinalValues, fscPeakNum, fscGradient, qScorePropUnderZero, proportionMasked]
    list_names = ['fscMinValues', 'fscFinalValues', 'fscPeakNum', 'fscGradient', 'qScorePropUnderZero',
                  'proportionMasked']

    # Create subplots for boxplots
    fig, axes = plt.subplots(len(all_data), 1, figsize=(6, 12), sharex=True)

    # Transpose the data to plot it along the y-axis
    transposed_data = [np.array(data).reshape(-1, 1) for data in all_data]

    # Create subplots for boxplots
    fig, axes = plt.subplots(1, len(all_data), figsize=(12, 6), sharex=True)

    # Create boxplots for each dataset
    for i, data in enumerate(transposed_data):
        axes[i].boxplot(data, vert=True)
        axes[i].set_title(f'Dataset {i + 1}')
        axes[i].set_xlabel('Values')

    # Set y-axis label only on the leftmost subplot
    axes[0].set_ylabel('values')

    # Set titles of each subplot with the names of the lists
    for ax, name in zip(axes, list_names):
        ax.set_title(name)

    # Adjust layout and save or show the plot
    plt.tight_layout()
    plt.savefig('jsonCheckOutputs/boxplot.png')

    #### ------------ ######
