from fscChecks import fscChecks
import json
from fileImport import importJsons

def writeDicToText(filePath, Dic):
    with open(filePath, 'w') as file:
        # Iterate over dictionary items and write them to the file
        for key, value in Dic.items():
            file.write(f'{key}: {value}\n')

if __name__ == '__main__':

    # -------------Initial parameters------------------#
    # Put in a parameters file when feeling less lazy
    # set base URL used to access VA JSON files:
    urlString = 'https://www.ebi.ac.uk/emdb/emdb-entry/emdbva/'

    # import a list of entry IDs
    with open('../2002_2020_withhalfmaps.txt', 'r') as entryimport:
        entries = entryimport.readlines()
    entryList = []
    for line in entries:
        entryList.append(line.replace('\n', ''))
    FSCDic = {}

    for entry in entryList:
        try:
            FSCDic[entry] = {'FSC': {}}
            # main URL string
            jsonRequest = importJsons(urlString)
            jsonFile = jsonRequest.requestJsonFile(entry)

            fscChecker = fscChecks(jsonFile)
            fscData = fscChecker.fscCurves['fsc']
            FSCDic[entry]['FSC'] = fscData

        except Exception as e:
            print('data not in json')

    with open('../FSCClassification/fscCurves.json', 'w') as json_file:
        json.dump(FSCDic, json_file)

    print ('written out file')

