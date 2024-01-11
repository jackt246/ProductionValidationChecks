import requests
import numpy as np
from PIL import Image
import io

class falseColourChecks():
    '''This class is designed to run checks on the FSC curve of every entry staged for release. Each check should be added as a function and then called in RunChecksPerCheck.py'''
    def __init__(self, inputFile):
        self.input = inputFile

        try:
            self.rawMapFalseColourMaxProjections = self.input['rawmap_orthogonal_glow_max']
            self.rawMapFalseColourMaxProjectionsScaled = self.rawMapFalseColourMaxProjections['scaled']
        except KeyError as e:
            raise Exception(f"Error: Required data not found in the JSON file. {e}")

    def maskCheck(self, entry, baseURL, saveImg=False):
        # Get the filename from the JSON fil
        maskFile = self.rawMapFalseColourMaxProjectionsScaled['z']

        # create the URL extension which returns the false colour image we want (could expand to use the
        # three directions but I think one will be enough
        entry = entry.strip('EMD-')
        entry = entry.strip('emd-')
        urlExtension = 'va-{}/va/{}'.format(entry, maskFile)
        fullURL = baseURL + urlExtension

        # Fetch the image using requests
        response = requests.get(fullURL)
        if response.status_code == 200:
            # Open the image using PIL
            img = Image.open(io.BytesIO(response.content))
            if saveImg is True:
                img.save('ImageChecks/images/{}.jpeg'.format(entry))
            # Convert the image to a NumPy array
            img_array = np.array(img)
            # Get the number of green pixels (assuming RGB where green is [0, 255, 0])
            green_pixels = np.sum(np.all(img_array == [0, 138, 0], axis=-1))
            # Get the total number of pixels in the image
            total_pixels = img_array.shape[0] * img_array.shape[1]
            # Calculate the proportion of green pixels
            proportion_green = (green_pixels / total_pixels) *100

            # Calculate proportions of green for halves split vertically
            mid_vertical = img_array.shape[1] // 2
            green_pixels_left_half = np.sum(np.all(img_array[:, :mid_vertical, :] == [0, 138, 0], axis=-1))
            green_pixels_right_half = np.sum(np.all(img_array[:, mid_vertical:, :] == [0, 138, 0], axis=-1))
            proportion_green_left_half = (green_pixels_left_half / (total_pixels // 2)) * 100
            proportion_green_right_half = (green_pixels_right_half / (total_pixels // 2)) * 100
            diff_vertical = proportion_green_left_half - proportion_green_right_half

            # Calculate proportions of green for halves split horizontally
            mid_horizontal = img_array.shape[0] // 2
            green_pixels_top_half = np.sum(np.all(img_array[:mid_horizontal, :, :] == [0, 138, 0], axis=-1))
            green_pixels_bottom_half = np.sum(np.all(img_array[mid_horizontal:, :, :] == [0, 138, 0], axis=-1))
            proportion_green_top_half = (green_pixels_top_half / (total_pixels // 2)) * 100
            proportion_green_bottom_half = (green_pixels_bottom_half / (total_pixels // 2)) * 100
            diff_horizontal = proportion_green_top_half - proportion_green_bottom_half

            return proportion_green, diff_vertical, diff_horizontal
        else:
            print("Failed to fetch the image")
            return None




