import pandas as pd
import numpy as np
import tensorflow as tf
from tensorflow.keras.layers import Dropout
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import classification_report, confusion_matrix
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense
from tensorflow.keras.preprocessing.sequence import pad_sequences
from imblearn.over_sampling import SMOTE
import matplotlib.pyplot as plt
from sklearn.preprocessing import MinMaxScaler

# Read the CSV file
csv_file_path = 'merged.csv'
df = pd.read_csv(csv_file_path)

# Aggregate FSC values for each EntryKey
df_grouped = df.groupby('EntryKey')['FSC'].agg(list).reset_index()

# Extract labels for each EntryKey (assuming all entries with the same EntryKey have the same label)
labels = df.groupby('EntryKey')['Class'].first().reset_index()['Class']

# Split data into training and testing sets
X_train_grouped, X_test_grouped, y_train, y_test = train_test_split(df_grouped['FSC'], labels, test_size=0.4, random_state=42)

# Normalize sequences to the same length using Min-Max scaling
max_length = 200  # Set your desired sequence length
scaler = MinMaxScaler()

# Pad sequences to a common length
X_train_padded = pad_sequences([scaler.fit_transform(np.array(seq).reshape(-1, 1)).flatten() for seq in X_train_grouped], maxlen=max_length, padding='post', dtype='float32')
X_test_padded = pad_sequences([scaler.transform(np.array(seq).reshape(-1, 1)).flatten() for seq in X_test_grouped], maxlen=max_length, padding='post', dtype='float32')

# Convert labels to binary (0 for 'OK', 1 for 'NOT')
y_train_binary = np.array(y_train.map({'OK': 0, 'NOT': 1}))
y_test_binary = np.array(y_test.map({'OK': 0, 'NOT': 1}))

smote = SMOTE(random_state=42)
X_train_resampled, y_train_resampled = smote.fit_resample(X_train_padded, y_train_binary)

# Build the model
model = Sequential()
model.add(Dense(units=128, activation='relu', input_dim=X_train_padded.shape[1]))
model.add(Dropout(0.1))
model.add(Dense(units=64, activation='relu'))
model.add(Dropout(0.1))
model.add(Dense(units=32, activation='relu'))
model.add(Dropout(0.1))
model.add(Dense(units=16, activation='relu'))
model.add(Dropout(0.1))
model.add(Dense(units=1, activation='sigmoid'))

# Compile the model with Adam optimizer
adam_optimizer = tf.keras.optimizers.Adam(learning_rate=1e-3)
model.compile(optimizer=adam_optimizer, loss='binary_crossentropy', metrics=['accuracy', tf.keras.metrics.Precision()])

# Assign weights based on class distribution
class_weights = {0: 1, 1: 10}  # You can adjust the weight for class 1 as needed


# Train the model with class weights and obtain the training history
history = model.fit(X_train_resampled, y_train_resampled, epochs=50, batch_size=32, validation_data=(X_train_padded, y_train_binary), class_weight=class_weights)

# Evaluate the model on the test set
loss, accuracy, precision = model.evaluate(X_test_padded, y_test_binary)
print(f'Test Loss: {loss}, Test Accuracy: {accuracy}, Test Precision: {precision}')

# Make predictions
y_pred = model.predict(X_test_padded)
y_pred_binary = (y_pred > 0.5).astype(int)

# Output additional classification metrics
print("Classification Report:")
print(classification_report(y_test_binary, y_pred_binary))

print("Confusion Matrix:")
print(confusion_matrix(y_test_binary, y_pred_binary))

model.save('model.h5')

# Plot training & validation accuracy values
plt.subplot(3, 1, 1)
plt.plot(history.history['accuracy'], label='Training Accuracy')
plt.plot(history.history['val_accuracy'], label='Validation Accuracy')
plt.title('Model Accuracy')
plt.xlabel('Epoch')
plt.ylabel('Accuracy')
plt.legend()
plt.grid(True)

# Plot training & validation precision values
plt.subplot(3, 1, 2)
plt.plot(history.history['precision'], label='Training Precision')
plt.plot(history.history['val_precision'], label='Validation Precision')
plt.title('Model Precision')
plt.xlabel('Epoch')
plt.ylabel('Precision')
plt.legend()
plt.grid(True)

# Plot training & validation loss values
plt.subplot(3, 1, 3)
plt.plot(history.history['loss'], label='Training Loss')
plt.plot(history.history['val_loss'], label='Validation Loss')
plt.title('Model Loss')
plt.xlabel('Epoch')
plt.ylabel('Loss')
plt.legend()
plt.grid(True)

plt.tight_layout()
plt.savefig('training.png')