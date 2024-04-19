import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import classification_report, confusion_matrix
from sklearn.ensemble import GradientBoostingClassifier
import matplotlib.pyplot as plt
from imblearn.over_sampling import SMOTE
from tensorflow.keras.preprocessing.sequence import pad_sequences

# Read the CSV file
csv_file_path = 'merged.csv'
df = pd.read_csv(csv_file_path)

# Aggregate FSC values for each EntryKey
df_grouped = df.groupby('EntryKey')['FSC'].agg(list).reset_index()

# Extract labels for each EntryKey (assuming all entries with the same EntryKey have the same label)
labels = df.groupby('EntryKey')['Class'].first().reset_index()['Class']

# Split data into training and testing sets
X_train_grouped, X_test_grouped, y_train, y_test = train_test_split(df_grouped['FSC'], labels, test_size=0.4, random_state=42)

# Pad sequences to a common length
max_length = max(map(len, X_train_grouped))
X_train_padded = pad_sequences(X_train_grouped.apply(np.array), maxlen=max_length, padding='post', dtype='float32')
X_test_padded = pad_sequences(X_test_grouped.apply(np.array), maxlen=max_length, padding='post', dtype='float32')

# Standardize the features after padding
scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train_padded)
X_test_scaled = scaler.transform(X_test_padded)

# Convert labels to binary (0 for 'OK', 1 for 'NOT')
y_train_binary = np.array(y_train.map({'OK': 0, 'NOT': 1}))
y_test_binary = np.array(y_test.map({'OK': 0, 'NOT': 1}))

# Apply SMOTE
smote = SMOTE(random_state=42)
X_train_resampled, y_train_resampled = smote.fit_resample(X_train_scaled, y_train_binary)

# Build the Gradient Boosting model
model = GradientBoostingClassifier(n_estimators=100, learning_rate=0.01, max_depth=3, random_state=42)

# Train the model
model.fit(X_train_resampled, y_train_resampled)

# Evaluate the model on the test set
y_pred = model.predict(X_test_scaled)

# Output additional classification metrics
print("Classification Report:")
print(classification_report(y_test_binary, y_pred))

print("Confusion Matrix:")
print(confusion_matrix(y_test_binary, y_pred))

# Note: Boosted Trees don't have a direct 'accuracy' metric like neural networks, so no 'accuracy' in the report.

# You can't plot loss over epochs for GradientBoostingClassifier, as it is not trained in epochs like neural networks.
# You can, however, plot feature importances if you're interested in the contribution of each feature to the model.
plt.bar(range(len(model.feature_importances_)), model.feature_importances_)
plt.title('Feature Importances')
plt.xlabel('Feature Index')
plt.ylabel('Importance')
plt.show()