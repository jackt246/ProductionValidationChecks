import json


def this_weeks_release(status_json_path='/nfs/production/gerard/emdb/archive/staging/status/latest/emdb_update.json'):
    with open(status_json_path, 'r') as file:
        update_json = json.load(file)

    return update_json['Releases']['entries']

entry_list = this_weeks_release()
print(entry_list)

#FSC thresholds:
minThreshold = -0.1
finalThreshold = 0.1
peakThreshold = 2
gradientThreshold = 0.1
phaseRandomThreshold = 1.1

#Q-score threshold
qScoreThreshold = 0.3

#Masking threshold
maskingThreshold = 21
paddingThreshold = 5