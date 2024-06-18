import json
import re
from file_handlers.file_import import VaFileFinder

def this_weeks_release(status_json_path='/nfs/production/gerard/emdb/archive/staging/status/latest/emdb_update.json'):
    with open(status_json_path, 'r') as file:
        update_json = json.load(file)

    return update_json['Releases']['entries']

class VaAssessment:
    def __init__(self, entry):
        self.entry = entry
        self.entry_number = entry.strip('EMD-')
        self.feature_extraction_json = (VaFileFinder.find_va_file(self.entry))
        #open the feature extraction file
        with open(self.feature_extraction_json, 'r') as file:
            self.feature_extraction_data = json.load(file)
        self.issue_dic = {}
    def fsc_assessment(self):
        assert self.feature_extraction_data[self.entry_number]['FSC'], 'FSC info not in file'
        assert self.feature_extraction_data[self.entry_number]['feature_zones'], 'feature zones not in file'
        fsc_data = self.feature_extraction_data[self.entry_number]['FSC']
        feature_zone = self.feature_extraction_data[self.entry_number]['feature_zones']
        # FSC thresholds:
        min_threshold = -0.1
        final_threshold = 0.1
        peakThreshold = 2
        gradientThreshold = 0.1
        phaseRandomThreshold = 1.1

        if 'minValue' in fsc_data and fsc_data['minValue'] < min_threshold:
            self.issue_dic[entry]['fsc_issues']['min_value']  = fsc_data['minValue']
        if 'endValue' in fsc_data and fsc_data['endValue'] > final_threshold:
            self.issue_dic[entry]['fsc_issues']['end_value'] = fsc_data['endValue']
        if 'peaks' in fsc_data and fsc_data['peaks'] > peakThreshold:
            self.issue_dic[entry]['fsc_issues']['peaks'] = fsc_data['peaks']
        if 'largestGradient' in fsc_data and fsc_data['largestGradient'] > gradientThreshold:
            self.issue_dic[entry]['FSCgradientValue'] = fsc_data['largestGradient']
        if 'overfit_zone' in feature_zone and feature_zone['feature_zone_ratio'] < phaseRandomThreshold:
            self.issues['FSC']['feature_zone_ratio'] = feature_zone['feature_zone_ratio']


    def masking_assessment(self):
        #Masking threshold
        maskingThreshold = 21
        paddingThreshold = 5

    def output_json(self):
        assert self.issue_dic, "The issue_dic dictionary is empty"
        # Write the dictionary to a JSON file
        with open('output_json.json', 'w') as json_file:
            json.dump(self.issue_dic, json_file)

if __name__ == '__main__':
    entry_list = this_weeks_release()

    for entry in entry_list:
        assessor = VaAssessment(entry)
        assessor.fsc_assessment()
        assessor.masking_assessment()
