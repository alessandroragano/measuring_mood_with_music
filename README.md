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
1. Compute audio features (training set and test set)
2. Model tuning (find the best model hyperparameters)
3. Model training (train support vector regression)
4. Valence prediction (predict valence scores on the test set)
5. Prepare data for regression
6. Run regression analysis (STATA)

To choose the action you need to run: 
```
python main.py --action=<n>
```
where n is the action that you want to execute. The default action is ``` 6 ``` (regression analysis) which runs the STATA software and produces the correlation plot
between life satisfaction and the music valence index (MVI).
Even though any action depends on the previous ones, we have provided the results already calculated so that you can run any action independently of each other.
To run all the steps, you should follow the order above. N.B.: the action ``` 1 ``` cannot be directly executed since the audio files are missing in the repo (see below).

## Feature computation
Features cannot be directly computed since the audio files are missing.
### Training set features
To compute the training set fetures, you can follow these steps:
1. Create the folder ```data/raw/train```.
2. Download the dataset https://cvml.unige.ch/databases/emoMusic/ and move the audio files to ``` data/raw/train ```.
3. Run this command
```
python main.py --action=1
```
### Test set features
The test set features that we have provided in the repo cannot be recomputed since the audio files are protected by copyright. However, you could use your test set. 
To compute features of your test set, follow these steps: 
1. Create the folder ```data/raw/test```.
2. Move the audio files to ```data/raw/test```.
3. Create the csv file ```data/annotations/test_annotations.csv``` with a column named ```song_id ``` that includes the filenames that you have in your folder. 
4. Run this command
```
python main.py --action=1
```

