import pickle
import json
import pandas as pd

# Configuration file
with open('config.json') as config_file:
    config = json.load(config_file)

# Import prediction data features
csv_prediction = config['csv_prediction_data']
prediction_data = pd.read_csv(csv_prediction)
csv_prediction_features = config['prediction_features']
prediction_features = pd.read_csv(csv_prediction_features, index_col='song_id')
output = pd.read_pickle(config['output'])

# Take best features
csv_best_features = config['csv_feature_selection']
best_features = pd.read_csv(csv_best_features)
X_prediction = prediction_features[best_features['features']]
X_prediction = X_prediction.to_numpy()

# Scale, the scaler is loaded since it was found using the training data
scaler = pickle.load(open(config['scaler_path'],'rb'))
X_prediction = scaler.transform(X_prediction)

# Load the model and make predictions
model = pickle.load(open(config['model_path'], 'rb'))
predictions = model.predict(X_prediction)

# Match songs
df_pred = pd.DataFrame({'song_id': prediction_features.index, 'valence_md': predictions})
prediction_data['song_id'] = [x[:-4] for x in prediction_data['song_id']]
merged = prediction_data.merge(df_pred, how='inner', on='song_id')
if config['store']:
    output['valence_md'] = merged['valence_md'].values
    output.to_pickle(config['output'])

print("Valence prediction done")