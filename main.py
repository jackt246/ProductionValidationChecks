import json
import matplotlib.pyplot as plt
import requests

from fscChecks import fscChecks
from fileImport import importJsons
from qScoreChecks import qScoreChecks
# Press the green button in the gutter to run the script.

def importJsonFile(fileName):
    with open(fileName, 'r') as file:
        fullJson = json.load(file)

    topLevelKey = list(fullJson.keys())
    return fullJson[topLevelKey[0]]

def writeDicToText(filePath, Dic):
    with open(filePath, 'w') as file:
        # Iterate over dictionary items and write them to the file
        for key, value in Dic.items():
            file.write(f'{key}: {value}\n')

def dicPlotter(dic, title):
    #plot a dictionary
    plt.figure()
    plt.scatter(range(len(list(dic.values()))), list(dic.values()))
    plt.title(title)
    plt.savefig('{}.png'.format(title))

if __name__ == '__main__':

    #set base URL used to access VA JSON files:
    urlString = 'https://wwwint.ebi.ac.uk/emdb/emdb-entry/emdbva/'

    runFSC = True
    runQscore = True

    #import a list of entry IDs
    with open('emdlist.txt', 'r') as entryimport:
        entries = entryimport.readlines()
    entryList = []
    for line in entries:
        entryList.append(line.replace('\n', ''))

    if runFSC is True:
        # define dictionaries to contain minimum values
        minFscDic = {}
        finalFscDic = {}
        gradientFscDic = {}
        entriesWithoutFsc = []
        for entry in entryList:
            #main URL string
            jsonRequest = importJsons(urlString)
            jsonFile = jsonRequest.requestJsonFile(entry)
            #have to wrap the following code in a try/except in case there is no FSC data
            try:
                #instantiate the fscCheck class with the jsonFile
                fscChecker = fscChecks(jsonFile)
                #get the minimum FSC value
                minFscDic[entry] = fscChecker.minValue()
                #get the final FSC value
                finalFscDic[entry] = fscChecker.finalValue()

            except Exception as e:
                print(f"Exception occurred: {e}, this entry will be added to FSCcheckoutputs/missingFSC.txt")
                # Handle the case where fscChecks initialization failed
                entriesWithoutFsc.append(entry)

        dicPlotter(minFscDic, 'FSCcheckoutputs/min_FSC_values')
        dicPlotter(finalFscDic, 'FSCcheckoutputs/final_FSC_values')

        writeDicToText('FSCcheckoutputs/minFSCvalues.txt', minFscDic)
        writeDicToText('FSCcheckoutputs/finalFSCvalues.txt', finalFscDic)


        with open('FSCcheckoutputs/missingFSC.txt', 'w') as file:
            # Iterate over dictionary items and write them to the file
            for  value in entriesWithoutFsc:
                file.write('{}\n'.format(value))

    if runQscore is True:
        qScoreProportionUnderZeroDic = {}
        for entry in entryList:
            #main URL string
            jsonRequest = importJsons(urlString)
            jsonFile = jsonRequest.requestJsonFile(entry)

            try:
                #instantiate the fscCheck class with the jsonFile
                qScoreChecker = qScoreChecks(jsonFile)
                qScoreProportionUnderZeroDic[entry] = qScoreChecker.proportionUnderZero()

            except Exception as e:
                print('Qscore check failed, possibly no model')
                continue

        dicPlotter(qScoreProportionUnderZeroDic, 'qScorecheckoutputs/proportionunderzero')
        writeDicToText('qScorecheckoutputs/propotionUnderZero.txt', qScoreProportionUnderZeroDic)









