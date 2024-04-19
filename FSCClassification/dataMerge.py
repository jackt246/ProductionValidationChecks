import pandas as pd

# Assuming df1 is the first dataset and df2 is the second dataset
# Replace 'your_first_dataset.csv' and 'your_second_dataset.csv' with the actual filenames or dataframes you have.

df1 = pd.read_csv('fsclistmegred.csv')
df2 = pd.read_csv('Classes.csv')

# Merge datasets on the 'EntryKey' column
merged_df = pd.merge(df1, df2, on='EntryKey')

# Display the merged dataset
merged_df.to_csv('merged.csv', index=False)