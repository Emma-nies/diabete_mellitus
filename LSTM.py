import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import MinMaxScaler
df_combined = pd.read_csv('tous_data.csv')

scaler = MinMaxScaler()
scaled_data = scaler.fit_transform(df_combined[['calories', 'obesity', 'diabetes']])

def create_sequences(data, seq_length):
    X = []
    y = []
    for i in range(len(data) - seq_length):
        X.append(data[i:i+seq_length])
        y.append(data[i+seq_length])  
    return np.array(X), np.array(y)

SEQ_LENGTH = 10
X, y = create_sequences(scaled_data, SEQ_LENGTH)

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

### Construction et entrainement du modèle

import tensorflow as tf
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import LSTM, Dense, Dropout

model = Sequential()
model.add(LSTM(50, return_sequences=True, input_shape=(SEQ_LENGTH, X_train.shape[2])))
model.add(LSTM(50))
model.add(Dropout(0.2))
model.add(Dense(3))  

model.compile(optimizer='adam', loss='mean_squared_error', metrics=['accuracy'])

history = model.fit(X_train, y_train, epochs=50, batch_size=32, validation_split=0.2)

loss = model.evaluate(X_test, y_test)
print(f'Loss: {loss}')

def predict_future(data, model, seq_length, n_predictions):
    predictions = []
    current_seq = data[-seq_length:]

    for _ in range(n_predictions):
        prediction = model.predict(np.array([current_seq]))
        predictions.append(prediction[0])
        current_seq = np.vstack([current_seq[1:], prediction[0]])

    return np.array(predictions)

n_future_years = 10
future_predictions = []

for entity in df_combined['Entity'].unique():
    entity_data = df_combined[df_combined['Entity'] == entity][['calories', 'obesity', 'diabetes']].values
    scaled_entity_data = scaler.transform(entity_data)
    future_preds = predict_future(scaled_entity_data, model, SEQ_LENGTH, n_future_years)
    future_preds = scaler.inverse_transform(future_preds)
    for i, year in enumerate(range(2022, 2022+n_future_years)):
        future_predictions.append([entity, year, *future_preds[i]])

df_future = pd.DataFrame(future_predictions, columns=['Entity', 'year', 'calories', 'obesity', 'diabetes'])

df_future_diabetes = df_future[['Entity', 'year', 'diabetes']]
df_future_obesity = df_future[['Entity', 'year', 'obesity']]
df_future_calories = df_future[['Entity', 'year', 'calories']]

print(df_combined.head())
print(df_future.head())

df_total = pd.concat([df_combined, df_future])

df_total.to_csv('output.csv', index=False)

