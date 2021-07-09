import pickle
import json
import pandas as pd

# Configuration file
with open('config.json') as config_file:
    config = json.load(config_file)

# Import test data features
csv_test = config['csv_test_data']
test_data = pd.read_csv(csv_test)
csv_test_features = config['test_features']
test_features = pd.read_csv(csv_test_features, index_col='song_id')
output = pd.read_pickle(config['output'])

# Take best features
csv_best_features = config['csv_feature_selection']
best_features = pd.read_csv(csv_best_features)
X_test = test_features[best_features['features']]
#X_test = test_features.to_numpy()

# Scale, the scaler is loaded since it was found using the training data
scaler = pickle.load(open(config['scaler_path'],'rb'))
X_test = scaler.transform(X_test)

# Load the model
model = pickle.load(open(config['model_path'], 'rb'))

predictions = model.predict(X_test)
if config['store_pred']:
    output['valence_md'] = predictions
    output.to_pickle(output)
else:
    output.to_pickle(config['output'])