import os
from numpy.core.numeric import full
import pandas as pd
import numpy as np
from feature_computation import Feature
import json
import librosa
from collections import defaultdict

# ***************** PATH CONFIGURATION ***************** 
# Configuration file
with open('config.json') as config_file:
    config = json.load(config_file)

# Import data
csv_file = config['csv_test_data']
song_id_list = pd.read_csv(csv_file, index_col='song_id').index.values.tolist() # Getting list of filename songs
root_data = config['root_test_data']

# Feature files
csv_features = config['csv_test_features']

# Update features equal to true allows udpating a csv of feature values already computed previously, otherwise an empty dictionary is initialized
if config['update_features']:
    features = pd.read_csv(csv_features, index_col='song_id')
    features = features.to_dict()
else:
    features = defaultdict(defaultdict)

# **************** FEATURE COMPUTATION *****************
win_length = config['win_length']
hop_length = config['hop_length']
sr = config['sampling_rate']

# For each filename, use feature.call_function to compute features that are included in config['feature_list'] which should be modified in the config.json file accordingly
for i, filename in enumerate(sorted(song_id_list)):
    fullpath = os.path.join(root_data, str(filename) + '.mp3')
    waveform, _ = librosa.load(fullpath, mono=True, sr=sr)

    # Take 45s middle of the song in the case of the test songs (Amazon music)
    if config['middle']:
        duration_secs = 45
        middle = waveform.shape[0]//2
        waveform = waveform[middle - int((duration_secs/2)*sr): middle + int((duration_secs/2)*sr)]
    print ("Processing audio file: {0}".format(filename))

    # create feature object
    feature = Feature(filename, waveform, win_length, hop_length, sr, features)

    # compute features and store them in the dataframe
    for feature_name, args in config['feature_list'].items():
        feature.call_function(feature_name, **args)

# Convert datframe to dictionary. Saving the features to a dictionary and then converting to a dataframe is faster than working on dataframe directly
df_features = pd.DataFrame.from_dict(feature.features)
df_features.index.rename('song_id', inplace=True)
df_features.to_csv(csv_features)