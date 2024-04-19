import matplotlib.pyplot as plt
import json

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


if __name__ == '__main__':

    # -------------Initial parameters------------------#
    # Put in a parameters file when feeling less lazy
    # set base URL used to access VA JSON files:
    urlString = 'https://www.ebi.ac.uk/emdb/emdb-entry/emdbva/'
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

    for entry in entryList:

        # main URL string
        jsonRequest = importJsons(urlString)
        jsonFile = jsonRequest.requestJsonFile(entry)

        with open('testOutputs/{}.json'.format(entry), 'w') as json_file:
            json.dump(jsonFile, json_file)
