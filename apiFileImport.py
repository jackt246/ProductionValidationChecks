import requests
class fileImport():
    def __init__(self):
        apiURL = 'https://ebi.ac.uk/emdb/api/'
    def importValidation(self, entry):
        # URL for API endpoint
        URL = '{}analysis/{}'.format(self.baseURL, entry)
        # Use requests to pull the data from that URL
        response = requests.get(URL)
        # Pull the json file from the response that we can then use elsewhere
        json_data = response.json()

        return json_data

    def importMetaData(self, entry):
        # URL for API endpoint
        URL = '{}entry/{}'.format(self.baseURL, entry)
        # Use requests to pull the data from that URL
        response = requests.get(URL)
        # Pull the json file from the response that we can then use elsewhere
        json_data = response.json()

        return json_data

class EMDBsearcher():

    def __init__(self):
        baseURL = 'https://ebi.ac.uk/emdb/api/'

    def recentRelease(self):

if __name__ == "__main__":


