from sklearn.feature_selection import SelectKBest, f_regression
from sklearn.model_selection import GridSearchCV
from sklearn.pipeline import Pipeline
import json
import pandas as pd
from sklearn.svm import SVR
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split
import numpy as np
from sklearn.model_selection import KFold

# Model tuning consists of finding the best hyperparameters and the best features
# N.B: never use the test data in this process to avoid any data leakage
# We use the entire EMO dataset since it represents the training set

# Configuration file
with open('config.json') as config_file:
    config = json.load(config_file)

csv_songs_info = config['songs_info']
songs_info = pd.read_csv(csv_songs_info)

# Use only development set (useful for benchmarking)
if config['benchmark']:
    train_index = songs_info[songs_info['Mediaeval 2013 set'] == 'development']['song_id']

# import audio features
csv_feature_path  = config['train_features']
features_df = pd.read_csv(csv_feature_path, index_col='song_id')
if config['benchmark']:
    features_df = features_df.loc[train_index]
X = features_df.to_numpy()

# import ground truth arousal and ground truth valence
train_data_file = config['csv_train_data']
df_train = pd.read_csv(train_data_file, index_col='song_id')

if config['benchmark']: 
    df_train = df_train.loc[train_index]

valence = df_train['mean_valence'].to_numpy()

# Create pipeline
pipe = Pipeline([
    ('feature_selection', SelectKBest(f_regression, k=100)),
    ('scale', StandardScaler()), 
    ('svr', SVR(kernel="rbf"))
])

# Create grid search with cross-validation
param_grid = {
            'svr__C': [0.1, 1, 5, 10, 100],
            'svr__epsilon': [0.0001, 0.0005, 0.001, 0.005, 0.01, 0.05, 0.1, 0.3, 0.5, 0.7, 1, 5, 10],
            'svr__gamma': [0.0001, 0.001, 0.005, 0.1, 1, 3, 5]
            }   
grid = GridSearchCV(pipe, param_grid, cv=5, scoring='r2')

# Training
grid.fit(X, valence) 

# Best parameters and best estimator
print(grid.best_params_)
print(grid.best_estimator_)
best_params = pd.DataFrame.from_dict(grid.best_params_, orient='index').transpose()
best_params.to_csv(config['csv_best_params'])

# Get names of the best features
mask = grid.best_estimator_.named_steps["feature_selection"].get_support()
names = features_df.columns.values[mask]
scores = grid.best_estimator_.named_steps["feature_selection"].scores_[mask]
names_scores = list(zip(names, scores))
ns_df = pd.DataFrame(data = names_scores, columns=['features', 'F_Scores'])

# Store dataframe
ns_df_sorted = ns_df.sort_values(['F_Scores', 'features'], ascending = [False, True])
ns_df_sorted.to_csv(config['csv_feature_selection'])