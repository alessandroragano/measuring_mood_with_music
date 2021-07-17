import pandas as pd
from sklearn.svm import SVR
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import r2_score
import json

# Configuration file
with open('config.json') as config_file:
    config = json.load(config_file)

# Import song info
csv_data = config['csv_train_data']
data = pd.read_csv(csv_data, index_col='song_id')
csv_songs_info = config['songs_info']
songs_info = pd.read_csv(csv_songs_info)

# Split into training and test
train_index = songs_info[songs_info['Mediaeval 2013 set'] == 'development']['song_id']
test_index = songs_info[songs_info['Mediaeval 2013 set'] == 'evaluation']['song_id']

train_data = pd.read_csv(csv_data, index_col='song_id').loc[train_index.values.tolist()]
test_data = pd.read_csv(csv_data, index_col='song_id').loc[test_index.values.tolist()]

# Import audio features
csv_features  = config['train_features']
features = pd.read_csv(csv_features, index_col='song_id')
features.index = [int(x.split('.')[0]) for x in features.index]
train_features = features.loc[train_index]
test_features = features.loc[test_index]

# Select best features
csv_best_features = config['csv_feature_selection']
best_features = pd.read_csv(csv_best_features)
train_features = train_features[best_features['features']]
test_features = test_features[best_features['features']]

# Train and test
X_train = train_features.to_numpy()
X_test = test_features.to_numpy()
y_train = train_data['mean_valence'].to_numpy()
y_true = test_data['mean_valence'].to_numpy()

# Scale data
scaler = StandardScaler()
X_train = scaler.fit_transform(X_train)
X_test = scaler.transform(X_test)

# Model best parameters
csv_best_params = config['csv_best_params']
best_params = pd.read_csv(csv_best_params)

# Create model
rv = SVR(kernel='rbf', C=best_params['svr__C'].values[0], epsilon=best_params['svr__epsilon'].values[0], gamma=best_params['svr__gamma'].values[0], coef0=0.1)

# Training
rv.fit(X_train, y_train)

# Prediction
y_pred = rv.predict(X_test)

print("R2 score on 1000 Songs EMO Music test set: {}".format(r2_score(y_true, y_pred)))