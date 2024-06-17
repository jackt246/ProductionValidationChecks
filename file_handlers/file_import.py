import json
import requests
import logging
import re
import os


class importJsons():
    def __init__(self, baseUrl):
        self.baseUrl = baseUrl

    def requestJsonFile(self, entry):
        # this should create a URL that will pull the json for the current entry
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


class StatusJsonReader:
    def __init__(self, update_json_path='/nfs/production/gerard/emdb/archive/staging/status/latest/emdb_update.json'):
        self.update_json_path = update_json_path
    def this_weeks_release(self):
        with open(self.status_json_path, 'r') as file:
            update_json = json.load(file)

        return update_json['Releases']['entries']

class VaFileFinder:
    def __init__(self, va_path='/hps/nobackup/gerard/emdb/va/entry_results'):
        self.va_path = va_path

    def find_va_file(self, entry):
        # Check the EMD-ID agrees with regular expression
        if not re.match(r'^EMD-\d{4,5}$', entry):
            raise ValueError('Entry must be in the format EMD-XXXX or EMD-XXXXX where X is an integer.')
        # Strip EMD- for now
        entry = entry.strip('EMD-')
        # Find path depending on 4/5 digits
        if len(entry) == 4:
            full_va_path = f"{self.va_path}/{entry[0]}{entry[1]}/{entry}/va/checks/{entry}_all_checks.json"
        elif len(entry) == 5:
            full_va_path = f"{self.va_path}/{entry[0]}{entry[1]}/{entry[2]}/{entry}/va/checks/{entry}_all_checks.json"
        else:
            raise ValueError('Unable to find that ID')
        #check file exists
        if os.path.exists(full_va_path) == False:
            raise ValueError('{} - file not found'.format(full_va_path))

        return full_va_path
