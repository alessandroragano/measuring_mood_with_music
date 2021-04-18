import pandas as pd
from sklearn.svm import SVR
from sklearn.preprocessing import StandardScaler
import numpy as np
import json

# Configuration file
with open('config.json') as config_file:
    config = json.load(config_file)

# Import song info
csv_train = config['csv_train_data']
train_data = pd.read_csv(csv_train, index_col='song_id')
csv_test = config['csv_test_data']
test_data = pd.read_csv(csv_test, index_col='song_id')

# Import audio features
csv_train_features  = config['train_features']
train_features = pd.read_csv(csv_train_features, index_col='song_id')
csv_test_features = config['test_features']
test_features = pd.read_csv(csv_test_features, index_col='song_id')

# Select best features
csv_best_features = config['csv_feature_selection']
best_features = pd.read_csv(csv_best_features)
train_features = train_features[best_features['features']]
test_features = test_features[best_features['features']]

# Train and test
X_train = train_features.to_numpy()
X_test = test_features.to_numpy()
y_train = train_data['mean_valence'].to_numpy()

# Scale Training data
scaler = StandardScaler()
X_train = scaler.fit_transform(X_train)
X_test = scaler.transform(X_test)

# Model best parameters
csv_best_params = config['csv_best_params']
best_params = pd.read_csv(csv_best_params)

# Create model
rv = SVR(kernel='rbf', C=best_params['svr__C'].values[0], epsilon=best_params['svr__epsilon'].values[0], gamma=best_params['svr__gamma'].values[0])

# Training
rv.fit(X_train, y_train)

# Prediction
print(rv.predict(X_test))