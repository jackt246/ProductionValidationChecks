import matplotlib.pyplot as plt
import json

from facetChecks.fscChecks import fscChecks
from fileHandlers.fileImport import importJsons
from facetChecks.qScoreChecks import qScoreChecks
from facetChecks.imageChecks import falseColourChecks


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


if __name__ == '__main__':

    # -------------Initial parameters------------------#
    # Put in a parameters file when feeling less lazy
    # set base URL used to access VA JSON files:
    urlString = 'https://wwwint.ebi.ac.uk/emdb/emdb-entry/emdbva/'
    # set which checks you want to run
    runFSC = True
    runQscore = False
    runMaskCheck = True
    # -------------------------------------------------#

    # import a list of entry IDs
    with open('CurrentRelease.txt', 'r') as entryimport:
        entries = entryimport.readlines()
    entryList = []
    for line in entries:
        entryList.append(line.replace('\n', ''))
    checkDic = {}

    for entry in entryList:

        checkDic[entry] = {'FSC': {}, 'qScore': {}, 'ImageChecks': {}}
        # main URL string
        jsonRequest = importJsons(urlString)
        jsonFile = jsonRequest.requestJsonFile(entry)

        # ------- Run FSC checks ------ #
        if runFSC is True:
            try:
                # instantiate the fscCheck class with the jsonFile
                fscChecker = fscChecks(jsonFile)
                # get the minimum FSC value
                checkDic[entry]['FSC']['Min Value'] = fscChecker.minValue()
                # get the final FSC value
                checkDic[entry]['FSC']['Final Value'] = fscChecker.finalValue()
                # peak finding
                checkDic[entry]['FSC']['Detected Peaks'] = fscChecker.peakFinder()
                #Phase random check
                checkDic[entry]['FSC']['Intergral Difference'] = fscChecker.compare_phase_masked()
                #gradient check
                checkDic[entry]['FSC']['largest gradient'] = fscChecker.maxGradientCheck()
                #
            except Exception as e:
                # Handle the case where fscChecks initialization failed
                checkDic[entry]['FSC']['missingFSC'] = 'True'


        # ------- Run Q-score checks ------ #
        if runQscore is True:
            try:
                # instantiate the fscCheck class with the jsonFile
                qScoreChecker = qScoreChecks(jsonFile)
                checkDic[entry]['qScore']['ProportionUnderZero'] = qScoreChecker.proportionUnderZero()

            except Exception as e:
                print('Qscore check failed, possibly no model')
                checkDic[entry]['qScore']['NoQScore'] = 'True'

        # ------- Run Mask checks -------- #

        if runMaskCheck is True:
            try:
                maskChecker = falseColourChecks(jsonFile)
                propMasked, diffVertical, diffHorizontal = maskChecker.maskCheck(entry, urlString)
                checkDic[entry]['ImageChecks']['ProportionMasked'] = propMasked
                checkDic[entry]['ImageChecks']['Mask Difference Vertical'] = diffVertical
                checkDic[entry]['ImageChecks']['Mask Difference Horizontal'] = diffHorizontal

            except Exception as e:
                print('failed to check for masking in half-maps')
                checkDic[entry]['ImageChecks']['Mask check failed'] = 'True'

    with open('checkJSON_staging.json', 'w') as json_file:
        json.dump(checkDic, json_file)

    print('Complete')
