import pandas as pd
from sklearn.svm import SVR
from sklearn.preprocessing import StandardScaler
import json
import pickle

# Configuration file
with open('config.json') as config_file:
    config = json.load(config_file)

# Import song info
csv_train = config['csv_train_data']
train_data = pd.read_csv(csv_train, index_col='song_id')

# Import audio features
csv_train_features  = config['train_features']
train_features = pd.read_csv(csv_train_features, index_col='song_id')

# Select best features
csv_best_features = config['csv_feature_selection']
best_features = pd.read_csv(csv_best_features)
train_features = train_features[best_features['features']]

# Train and test
X_train = train_features.to_numpy()
y_train = train_data['mean_valence'].to_numpy()

# Scale data
scaler = StandardScaler()
X_train = scaler.fit_transform(X_train)
pickle.dump(scaler, open(config['scaler_path'],'wb'))

# Model best parameters
csv_best_params = config['csv_best_params']
best_params = pd.read_csv(csv_best_params)

# Create model
model = SVR(kernel='rbf', C=best_params['svr__C'].values[0], epsilon=best_params['svr__epsilon'].values[0], gamma=best_params['svr__gamma'].values[0], coef0=0.1)

# Training
model.fit(X_train, y_train)
print("Training done")

# Save model
pickle.dump(model, open(config['model_path'], 'wb'))
print("Model stored in: {}".format(config['model_path']))