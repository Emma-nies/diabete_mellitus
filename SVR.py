import pandas as pd
import numpy as np
from sklearn.svm import SVR
from sklearn.preprocessing import MinMaxScaler
from sklearn.model_selection import train_test_split



df_combined = pd.merge(pd.merge(df_diabetes, df_obesity, on=['Entity', 'Year']), df_calories, on=['Entity', 'Year'])



################# Pour le modèle on remplir les valeurs manquantes par interpolation
df_combined.interpolate(method='linear', inplace=True)


#############################  Préparation des données pour le modèle ########################

def create_sequences(data, seq_length):
    X, y = [], []
    for i in range(len(data) - seq_length):
        X.append(data[i:i+seq_length])
        y.append(data[i+seq_length])
    return np.array(X), np.array(y)


future_predictions = []

############################ On va prédire les données pour chaque pays et chaque variables

for entity in df_combined['Entity'].unique():
    entity_data = df_combined[df_combined['Entity'] == entity]
    
    for column in ['diabetes', 'obesity', 'calories']:
        data_series = entity_data[column].values.reshape(-1, 1)
        
        # Normalisation des données
        scaler = MinMaxScaler()
        scaled_data = scaler.fit_transform(data_series)
        
        SEQ_LENGTH = 10
        X, y = create_sequences(scaled_data, SEQ_LENGTH)
        

        if len(X) == 0 or len(y) == 0:
            print(f"Pas assez de données")
            continue
        
########################### On divise les données pour entraîner le modèle et faire des testes
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
        

        if len(X_train) == 0 or len(X_test) == 0:
            print(f"Pas assez de données partie X_train X_test")
            continue
        
######################################################################################################  
################################## Construction et entraînement du modèle ############################
######################################################################################################

        model = SVR(kernel='rbf', C=100, gamma=0.1, epsilon=0.1)
        model.fit(X_train.reshape((X_train.shape[0], -1)), y_train)
        
######################  Prédiction des 10 prochaines années

        current_seq = scaled_data[-SEQ_LENGTH:]
        future_preds = []
        
        for _ in range(10):
            prediction = model.predict(current_seq.reshape((1, -1)))[0]
            future_preds.append(prediction)
            current_seq = np.append(current_seq[1:], prediction).reshape(-1, 1)
        
        future_preds = scaler.inverse_transform(np.array(future_preds).reshape(-1, 1)).flatten()
        years = range(2022, 2032)
        forecast_df = pd.DataFrame({'Year': years, column: future_preds, 'Entity': entity})
        
        if len(future_predictions) == 0:
            future_predictions = forecast_df
        else:
            future_predictions = pd.concat([future_predictions, forecast_df], ignore_index=True)


################# Création d'un dataframe avec les anciennes et nouvelles données #################

df_future = future_predictions
df_future['Year'] = df_future['Year'].astype(int)

# Fusionner les données actuelles et futures
data_dash = pd.concat([df_combined, df_future], ignore_index=True)

# Sauvegarder les résultats
data_dash.to_csv('output.csv', index=False, sep=';')