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
where n is the action that you want to take. The default action is ``` 6 ``` (regression analysis) which runs the STATA software and produces the correlation plot
between life satisfaction and the music valence index (MVI)

## Feature computation
Due to copyright issues, we have uploaded the features already computed on the test set. We have done the same for the training set, 
however you could recompute the features on the same training set which is not protected by copyright.
To compute the training set fetures, you can follow these steps:
1. Create the folder ```data/raw/train```.
2. Download the dataset https://cvml.unige.ch/databases/emoMusic/ and moving the audio files to ``` data/raw/train ```.

To compute features on your own test set, follow these steps: 
1. Create the folder ```data/raw/test```.
2. Move the audio files to ```data/raw/test```.
3. Create the ```data/annotations/test_annotations.csv``` with a column named ```song_id ``` that includes the filenames that you have in your folder. 

