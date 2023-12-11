import json
import matplotlib.pyplot as plt
import requests
import logging


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





