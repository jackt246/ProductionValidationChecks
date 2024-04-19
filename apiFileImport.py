import requests
import json
from datetime import datetime, timedelta
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import traceback

class fileImport():
    def __init__(self):
        self.apiURL = 'https://ebi.ac.uk/emdb/api/'
    def importValidation(self, entry):
        # URL for API endpoint
        URL = '{}analysis/{}'.format(self.apiURL, entry)
        # Use requests to pull the data from that URL
        response = requests.get(URL)
        # Pull the json file from the response that we can then use elsewhere
        json_data = response.json()

        return json_data

    def importMetaData(self, entry):
        # URL for API endpoint
        URL = '{}entry/{}'.format(self.apiURL, entry)
        # Use requests to pull the data from that URL
        response = requests.get(URL)
        # Pull the json file from the response that we can then use elsewhere
        json_data = response.json()

        return json_data

class EMDBsearcher():
    def __init__(self):
        self.apiURL = 'https://ebi.ac.uk/emdb/api/'
    def emdbRecentEntries(self):

        #find out date of last wednesday
        today = datetime.today()
        todayToWednesday = (today.weekday() - 2) % 7  # 2 represents Wednesday (0: Monday, 1: Tuesday, ..., 6: Sunday)
        lastWednesday = today - timedelta(days=todayToWednesday)
        lastWednesdayFormatted = lastWednesday.strftime('%Y-%m-%d')

        #URL for API endpoint
        URL = '{}search/release_date:"{}T00:00:00Z" AND database:EMDB'.format(self.apiURL, lastWednesdayFormatted)
        # Use requests to pull the data from that URL
        response = requests.get(URL)
        # Pull the json file from the response that we can then use elsewhere
        json_data = response.json()

        return json_data

if __name__ == "__main__":
    # Instantiate the fileImporter class
    fileImporter = fileImport()

    # Pull and save validation information
    #validationJson = fileImporter.importValidation('EMD-1001')
    #with open('validationJson.json', 'w') as json_file:
    #    json.dump(validationJson, json_file)

    #Pull and save Metadata information
    #metadataJson = fileImporter.importMetaData('EMD-1001')
    #with open('metadataJson.json', 'w') as json_file:
    #    json.dump(metadataJson, json_file)

    Searcher = EMDBsearcher()
    LastRelease = Searcher.emdbRecentEntries()
    #with open('recentEntries.json', 'w') as json_file:
    #    json.dump(LastRelease, json_file)

    emDf = pd.DataFrame(columns=['id', 'method', 'FSC Resolution'])
    for entry in LastRelease:
        entryId = entry['emdb_id']
        entryIdTrunc = entryId.strip('EMD-')
        print(entryIdTrunc)
        # get the EM method
        emMethod = entry['structure_determination_list']['structure_determination'][0]['method']
        validationJson = fileImporter.importValidation(entry['emdb_id'])
        try:
            resolutionEMDB = 1 / validationJson[entryIdTrunc]['fsc']['intersections']['0.143']['x']
            dataForDf = {'id': entryId, 'method': emMethod, 'FSC Resolution': resolutionEMDB}
            emDf = emDf._append(dataForDf, ignore_index=True)
        except KeyError as e:
            print('{} has no FSC Curve: {}'.format(entry['emdb_id'], str(e)))
            traceback.print_exc()

sns.histplot(emDf, x='FSC Resolution', hue='method', multiple='layer')
plt.show()




