# Measuring Mood with Music
## Preparation
To use the repository follow these steps first:

```
git clone <repo>
pip install virtualenv
virtualenv <your_env> # your_env is how you want to name the virtual environment
source <your_env>/bin/activate
cd <repo>
pip install -r requirements.txt
```

The regression analysis is made with STATA (SE) https://www.stata.com. You need to update "stata_installation_path" in config.json by indicating the path to the STATA software. 

The default location in Mac OS usually is ```/Applications/Stata/StataSE.app/Contents/MacOS/StataSE```.

## Usage
You can choose which action you want to execute: 
1. Compute audio features (training set and prediction set)
2. Model tuning (find the best model hyperparameters)
3. Model training (train support vector regression)
4. Model testing
5. Valence prediction (predict valence scores on the prediction set)
6. Run regression analysis (STATA)

To choose the action you need to run: 
```
python main.py --action=<n>
```
where n is the action that you want to execute. The default action is ``` 6 ``` (regression analysis) which runs the STATA software and produces the regression and correlation results (statistics, tables and figures) for the paper, e.g. the scatter plot
of life satisfaction and the music valence index (MVI).
Even though any action depends on the previous ones, we have provided the results already calculated so that you can run any action independently of each other.
To run all the steps, you should follow the order above. N.B.: the action ``` 1 ``` cannot be directly executed since the audio files of the prediction set are missing due to copyright (see below).

## Feature computation
### Training set features
To compute the training set fetures, you can follow these steps:
1. Create the folder ```data/raw/train```.
2. Download the dataset https://cvml.unige.ch/databases/emoMusic/ and move the audio files to ``` data/raw/train ```.
3. Run this command
```
python main.py --action=1 --dataset_mode="train"
```
### Prediction set features
The prediction set features that we have provided in the repo cannot be recomputed since the audio files are protected by copyright. However, you could use your own prediction set (e.g. chart music for any country). 
To compute features of your own prediction set, follow these steps: 
1. Create the folder ```data/raw/prediction```.
2. Move the audio files to ```data/raw/prediction```.
3. Create the csv file ```data/annotations/prediction_annotations.csv``` with a column named ```song_id ``` that includes the filenames that you have in your folder. 
4. Run this command
```
python main.py --action=1 --dataset_mode="prediction"
```

#### Essentia features
Some features are computed using the open source library Essentia https://essentia.upf.edu. This library is not compatible with virtual environment. 
You can install Essentia outside the virtual environment and copy its content to the virtual environment:
1. Install Essentia https://essentia.upf.edu/installing.html
2. Copy the library content to your virtual environment as follows:
   ```
   cp -r /usr/local/lib/python3.8/site-packages/essentia <path_to_your_env>/lib/python3.8/site-packages/essentia
   ```
   where <path_to_your_env> is where your virtual environment is located.
   N.B: all the actions except ``` 1 ``` will run even without Essentia. Therefore, you could skip this step if you don't need to compute the audio features.
