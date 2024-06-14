import json
import re

def this_weeks_release(status_json_path='/nfs/production/gerard/emdb/archive/staging/status/latest/emdb_update.json'):
    with open(status_json_path, 'r') as file:
        update_json = json.load(file)

    return update_json['Releases']['entries']

def find_va_file(self, entry):
    # Check the EMD-ID agrees with regular expression
    if not re.match(r'^EMD-\d{4,5}$', entry):
        raise ValueError('Entry must be in the format EMD-XXXX or EMD-XXXXX where X is an integer.')
    # Strip EMD- for now
    entry = entry.strip('EMD-')
    # Find path depending on 4/5 digits
    if len(entry) == 4:
        full_va_path = f"{self.va_path}/{entry[0]}{entry[1]}/EMD-{entry}"
    elif len(entry) == 5:
        full_va_path = f"{self.va_path}/{entry[0]}{entry[1]}/{entry[2]}/EMD-{entry}"
    else:
        raise ValueError('EMD IDs need to be 4 or 5 digit')

    return full_va_path

class assessments:
    def __init__(self, entry):
        self.entry = entry
        self.feature_extraction_json = find_va_file(self.entry)
        #open the feature extraction file
        with open(self.feature_extraction_json, 'r') as file:
            self.feature_extraction_data = json.load(file)
    def fsc_assessment(self):
        # FSC thresholds:
        minThreshold = -0.1
        finalThreshold = 0.1
        peakThreshold = 2
        gradientThreshold = 0.1
        phaseRandomThreshold = 1.1



    def masking_assessment(self):
        #Masking threshold
        maskingThreshold = 21
        paddingThreshold = 5

if __name__ == '__main__':
    entry_list = this_weeks_release()
