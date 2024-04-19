import pandas as pd
import json

# Read the JSON file
json_file_path = 'fscCurves.json'
with open(json_file_path, 'r') as json_file:
    data = json.load(json_file)

# Extract information under "FSC" key for each entry with missingFSC set to False
csv_data_list = []
for entry_key, entry_data in data.items():
    fsc_values = entry_data.get("FSC", [])  # Extract FSC values, default to empty list
    for fsc_value in fsc_values:
        csv_data = {"FSC": fsc_value, "EntryKey": entry_key}  # Create a dictionary for each FSC value
        csv_data_list.append(csv_data)

# Convert the list of dictionaries to a Pandas DataFrame
df = pd.DataFrame(csv_data_list)

# Specify the CSV output path
csv_output_path = 'fsclist2.csv'

# Output Pandas DataFrame to CSV
df.to_csv(csv_output_path, index=False)

print(f'Data has been read from {json_file_path} and written to {csv_output_path}')