import matplotlib.pyplot as plt
from facet_checks.fsc_checks import fscChecks
from file_handlers.file_import import importJsons
from tqdm import tqdm



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
    checkDic = []

    for entry in tqdm(entryList, desc='Processing entries'):
        # main URL string
        jsonRequest = importJsons(urlString)
        jsonFile = jsonRequest.requestJsonFile(entry)
        try:
            fscChecker = fscChecks(jsonFile)
            checkDic.append(fscChecker.compare_phase_masked())
        except Exception as e:
            print('failed because: {}'.format(e))

    print(checkDic)
    print('Complete')