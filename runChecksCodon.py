import json
import argparse
from facetChecks.fscChecks import fscChecks
from facetChecks.imageChecks import falseColourChecks


def writeDicToText(filePath, Dic):
    with open(filePath, 'w') as file:
        # Iterate over dictionary items and write them to the file
        for key, value in Dic.items():
            file.write(f'{key}: {value}\n')

def process_entry(entry, runFSC, runMaskCheck, output):
    #The checks should be made into their own functions one day
    checkDic = {entry: {'FSC': {}, 'qScore': {}, 'ImageChecks': {}}}
    
    #open json file and prep it for future processing
    with open(entry, 'r') as file:
        va_file = json.load(file)    
    topLevelKey = list(va_file.keys())
    va_dictionary = va_file[topLevelKey[0]]

    
    if runFSC:
        try:
            fscChecker = fscChecks(va_dictionary)
            checkDic[entry]['FSC']['Min Value'] = fscChecker.minValue()
            checkDic[entry]['FSC']['Final Value'] = fscChecker.finalValue()
            checkDic[entry]['FSC']['Detected Peaks'] = fscChecker.peakFinder()
            checkDic[entry]['FSC']['Intergral Difference'] = fscChecker.compare_phase_masked()
            checkDic[entry]['FSC']['largest gradient'] = fscChecker.maxGradientCheck()
        except Exception as e:
            checkDic[entry]['FSC']['missingFSC'] = 'True'

    if runMaskCheck:
        try:
            maskChecker = falseColourChecks(va_dictionary)
            propMasked, diffVertical, diffHorizontal = maskChecker.maskCheck(entry)
            checkDic[entry]['ImageChecks']['ProportionMasked'] = propMasked
            checkDic[entry]['ImageChecks']['Mask Difference Vertical'] = diffVertical
            checkDic[entry]['ImageChecks']['Mask Difference Horizontal'] = diffHorizontal
        except Exception as e:
            print('Failed to check for masking in half-maps')
            checkDic[entry]['ImageChecks']['Mask check failed'] = 'True'

    with open(output, 'w') as json_file:
        json.dump(checkDic, json_file)

    return checkDic

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Process entries for validation.')
    parser.add_argument('--entry', type=str, help='path to a single entry va file')
    parser.add_argument('--output', type=str, default='facet_check_output.json', help='Output JSON file')
    parser.add_argument('--runFSC', action='store_true', help='Run FSC checks')
    parser.add_argument('--runMaskCheck', action='store_true', help='Run Mask checks')

    args = parser.parse_args()

    if args.entry:
        entries = [args.entry]
    elif args.entry_file:
        with open(args.entry_file, 'r') as entry_file:
            entries = [line.strip() for line in entry_file.readlines()]
    else:
        raise ValueError('Either --entry or --entry_file must be provided.')

    process_entry(entries, args.runFSC, args.runMaskCheck, args.output)