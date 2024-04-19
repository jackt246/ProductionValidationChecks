import matplotlib.pyplot as plt
import requests

from fscChecks import fscChecks
from fileImport import importJsons
from qScoreChecks import qScoreChecks
from imageChecks import falseColourChecks


def writeDicToText(filePath, Dic):
    with open(filePath, 'w') as file:
        # Iterate over dictionary items and write them to the file
        for key, value in Dic.items():
            file.write(f'{key}: {value}\n')


def dicPlotter(dic, title):
    # plot a dictionary
    plt.figure()
    plt.scatter(range(len(list(dic.values()))), list(dic.values()))
    plt.title(title)
    plt.savefig('{}.png'.format(title))

def dicPlotterTwo(dic1, dic2, title):
    # plot a dictionary
    plt.figure()
    plt.scatter(list(dic1.values()), list(dic2.values()))

    # Draw a square with a side length of 5
    square_side = 10
    square = plt.Rectangle((0 - (square_side/2), 0 - (square_side/2)), square_side, square_side, linewidth=1, edgecolor='r', facecolor='none')
    plt.gca().add_patch(square)

    plt.title(title)
    plt.show()

if __name__ == '__main__':

    # -------------Initial parameters------------------#
    # Put in a parameters file when feeling less lazy
    # set base URL used to access VA JSON files:
    urlString = 'https://www.ebi.ac.uk/emdb/emdb-entry/emdbva/'
    # set which checks you want to run
    runFSC = True
    runQscore = False
    runMaskCheck = False
    # -------------------------------------------------#

    # import a list of entry IDs
    with open('2002_2020_withhalfmaps.txt', 'r') as entryimport:
        entries = entryimport.readlines()
    entryList = []
    for line in entries:
        entryList.append(line.replace('\n', ''))

    # ------- Run FSC checks ------ #
    if runFSC is True:
        # define dictionaries to contain minimum values
        minFscDic = {}
        finalFscDic = {}
        minFinalFscDifDic = {}
        gradientFscDic = {}
        peakDic = {}
        entriesWithoutFsc = []
        fscIssueDic = {}
        issuesForSearch = []
        for entry in entryList:
            # main URL string
            jsonRequest = importJsons(urlString)
            jsonFile = jsonRequest.requestJsonFile(entry)
            # have to wrap the following code in a try/except in case there is no FSC data
            try:
                # instantiate the fscCheck class with the jsonFile
                fscChecker = fscChecks(jsonFile)
                # get the minimum FSC value
                minFscDic[entry] = fscChecker.minValue()
                # get the final FSC value
                finalFscDic[entry] = fscChecker.finalValue()
                # get difference between min and final value
                minFinalFscDifDic[entry] = fscChecker.minFinalDifValue()
                # peak finding
                peakDic[entry] = fscChecker.peakFinder()
                # gradient check
                try:
                    gradientFscDic[entry] = fscChecker.maxGradientCheck()
                except Exception as e:
                    print(f"no steep gradient detected. {e}")
                # Plot FSC curves to do manual inspection
                fscChecker.fscPlotter('FSCCurves/{}'.format(entry))
                #thresholds:
                minThreshold = -0.1
                finalThreshold = 0.1
                peakThreshold = 3
                gradientThreshold = 0
                masking = 0.2

                # List to store multiple issues for an entry
                issues = []

                if finalFscDic[entry] >= finalThreshold:
                    issues.append('final value, ')
                if minFscDic[entry] <= minThreshold:
                    issues.append('minimum value issue, ')
                if peakDic[entry] >= peakThreshold:
                    issues.append('too many peaks, ')
                if gradientFscDic[entry] > gradientThreshold:
                    issues.append('sharp drop detected, ')

                # Assign the list of issues to fscIssueDic for the entry
                if issues:
                    fscIssueDic[entry] = issues
                    issuesForSearch.append('{} OR'.format(entry))

            except Exception as e:
                print(f"Exception occurred: {e} for entry {entry}, this entry will be added to FSCcheckoutputs/missingFSC.txt")
                # Handle the case where fscChecks initialization failed
                entriesWithoutFsc.append(entry)

        dicPlotter(minFscDic, 'FSCcheckoutputs/min_FSC_values')
        dicPlotter(finalFscDic, 'FSCcheckoutputs/final_FSC_values')
        dicPlotter(peakDic, 'FSCcheckoutputs/peaks')
        dicPlotter(gradientFscDic, 'FSCcheckoutputs/gradient')
        dicPlotter(minFinalFscDifDic, 'FSCcheckoutputs/min_final_dif')

        writeDicToText('FSCcheckoutputs/minFSCvalues.txt', minFscDic)
        writeDicToText('FSCcheckoutputs/finalFSCvalues.txt', finalFscDic)
        writeDicToText('FSCcheckoutputs/peaks.txt', peakDic)
        writeDicToText('FSCcheckoutputs/fscIssueEntries.txt', fscIssueDic)
        writeDicToText('FSCcheckoutputs/GradientISsues.txt', gradientFscDic)
        writeDicToText('FSCcheckoutputs/min_final_dif.txt', minFinalFscDifDic)

        with open('FSCcheckoutputs/fscIssues_EMDBSearch.txt', 'w') as file:
            # Iterate over dictionary items and write them to the file
            for value in issuesForSearch:
                file.write('{}'.format(value))

        with open('FSCcheckoutputs/missingFSC.txt', 'w') as file:
            # Iterate over dictionary items and write them to the file
            for value in entriesWithoutFsc:
                file.write('{}\n'.format(value))

    # ------- Run Q-score checks ------ #
    if runQscore is True:
        qScoreProportionUnderZeroDic = {}
        for entry in entryList:
            # main URL string
            jsonRequest = importJsons(urlString)
            jsonFile = jsonRequest.requestJsonFile(entry)

            try:
                # instantiate the fscCheck class with the jsonFile
                qScoreChecker = qScoreChecks(jsonFile)
                qScoreProportionUnderZeroDic[entry] = qScoreChecker.proportionUnderZero()

            except Exception as e:
                print('Qscore check failed, possibly no model')
                continue

        dicPlotter(qScoreProportionUnderZeroDic, 'qScorecheckoutputs/proportionunderzero')
        writeDicToText('qScorecheckoutputs/propotionUnderZero.txt', qScoreProportionUnderZeroDic)

    # ------- Run Mask checks -------- #

    if runMaskCheck is True:
        maskCheckDic = {}
        verticalProportion = {}
        horizontalPropotion = {}
        for entry in entryList:
            jsonRequest = importJsons(urlString)
            jsonFile = jsonRequest.requestJsonFile(entry)

            try:
                maskChecker = falseColourChecks(jsonFile)
                maskCheckDic[entry], verticalProportion[entry], horizontalPropotion[entry] = maskChecker.maskCheck(entry, urlString)

            except Exception as e:
                print('failed to check for masking in half-maps')
                continue

        dicPlotter(maskCheckDic, 'ImageChecks/proportionGreen')
        dicPlotter(verticalProportion, 'ImageChecks/vertical')
        dicPlotter(horizontalPropotion, 'ImageChecks/horiztonal')
        dicPlotterTwo(verticalProportion, horizontalPropotion, 'ImageChecks/horandVert')
        writeDicToText('ImageChecks/proportionGreen.txt', maskCheckDic)
        writeDicToText('ImageChecks/verticalProportion.txt', verticalProportion)
        writeDicToText('ImageChecks/horizontalPropotion.txt', horizontalPropotion)




