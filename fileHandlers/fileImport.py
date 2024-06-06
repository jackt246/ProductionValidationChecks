import json
import matplotlib.pyplot as plt
import requests
import logging
from datetime import datetime, timedelta
from io import StringIO


class importJsons():
    def __init__(self, baseUrl):
        self.baseUrl = baseUrl

    def requestJsonFile(self, entry):
        #this should create a URL that will pull the json for the current entry
        entry = entry.strip('EMD-')
        entry = entry.strip('emd-')
        urlExtension = 'va-{}/va/emd_{}_all.json'.format(entry, entry)
        fullUrl = self.baseUrl + urlExtension

        try:
            # Send a GET request to the URL
            response = requests.get(fullUrl)
            response.raise_for_status()  # Raises an HTTPError if the response code is not 2xx

            # Parse the JSON content of the response
            json_data = response.json()

            # pre-process the file so we have direct access to the actual data
            topLevelKey = list(json_data.keys())
            return json_data[topLevelKey[0]]

        except requests.HTTPError as http_err:
            # Handles HTTP errors (e.g., 404, 500, etc.)
            logging.error(f"HTTP error occurred: {http_err}")
            logging.exception(str(http_err))
        except Exception as err:
            # Handles other types of exceptions
            logging.error(f"An error occurred: {err}")
            logging.exception(str(err))

class APIsearch():
    def __init__(self):
        self.apiURL = 'https://www.ebi.ac.uk/emdb/api/'

    def emdbLastRelease(self, saveFile=False, fileType='json'):
        # find out date of last wednesday
        today = datetime.today()
        todayToWednesday = (today.weekday() - 2) % 7  # 2 represents Wednesday (0: Monday, 1: Tuesday, ..., 6: Sunday)
        lastWednesday = today - timedelta(days=todayToWednesday)
        lastWednesdayFormatted = lastWednesday.strftime('%Y-%m-%d')

        # URL for API endpoint
        if fileType == 'json':
            URL = '{}search/release_date:"{}T00:00:00Z" AND database:EMDB'.format(self.apiURL, lastWednesdayFormatted)
            # Use requests to pull the data from that URL
            response = requests.get(URL)
            # Pull the json file from the response that we can then use elsewhere
            json_data = response.json()

            # save json file if wanted
            if saveFile == True:
                with open('lastReleaseEntries.json', 'w') as json_file:
                    json.dump(json_data, json_file)

            return json_data

        elif fileType == 'csv':
            URL = '{}search/release_date:"{}T00:00:00Z"%20AND%20database:EMDB?&wt=csv&downlod=false&fl=emdb_id'.format(
                self.apiURL, lastWednesdayFormatted)
            # Use requests to pull the data from that URL
            response = requests.get(URL)
            csv_content = response.content.decode('utf-8')
            # Use pandas to read the CSV content into a DataFrame
            csv_data = pd.read_csv(StringIO(csv_content))
            if saveFile == True:
                csv_data.to_csv('lastReleaseEntries.csv')

            return csv_data

    def emdbNextRelease(self, saveFile=False, fileType='json'):
        # Find out the date of the next Wednesday
        today = datetime.today()
        days_until_next_wednesday = (
                                            2 - today.weekday()) % 7  # 2 represents Wednesday (0: Monday, 1: Tuesday, ..., 6: Sunday)
        next_wednesday = today + timedelta(days=days_until_next_wednesday)
        nextWednesdayFormatted = next_wednesday.strftime('%Y-%m-%d')

        # URL for API endpoint
        if fileType == 'json':
            URL = '{}search/release_date:"{}T00:00:00Z" AND database:EMDB'.format(self.apiURL,
                                                                                  nextWednesdayFormatted)
            # Use requests to pull the data from that URL
            response = requests.get(URL)
            # Pull the json file from the response that we can then use elsewhere
            json_data = response.json()

            # save json file if wanted
            if saveFile == True:
                with open('lastReleaseEntries.json', 'w') as json_file:
                    json.dump(json_data, json_file)

            return json_data

        elif fileType == 'csv':
            URL = '{}search/release_date:"{}T00:00:00Z"%20AND%20database:EMDB?&wt=csv&downlod=false&fl=emdb_id'.format(
                self.apiURL, nextWednesdayFormatted)
            # Use requests to pull the data from that URL
            response = requests.get(URL)
            csv_content = response.content.decode('utf-8')
            # Use pandas to read the CSV content into a DataFrame
            csv_data = pd.read_csv(StringIO(csv_content))
            if saveFile == True:
                csv_data.to_csv('lastReleaseEntries.csv')

            return csv_data



