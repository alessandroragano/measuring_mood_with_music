import click
import subprocess
import json

@click.command()
@click.option('--action', default=1, required=True, help="Choose which script you want to run. 1) Feature computation, 2) Hyperparameter tuning" + 
                           "3) Model training, 4) Valence prediction, 5) Prepare regression data, 6) Regression analysis")
@click.option('--dataset_mode', required=False)
def main(action, dataset_mode='train'):
    click.echo(action)
    if action == 1:
        print("Feature computation")
        with open('config.json') as config_file:
            config = json.load(config_file)
        config['dataset_mode'] = dataset_mode
        subprocess.check_call(["python3.8", "src/features/audio_processing.py"])
    elif action == 2:
        print("Model tuning")
        subprocess.check_call(["python3.8", "src/model/model_tuning.py"])
    elif action == 3:
        print("Start Training")
        subprocess.check_call(["python3.8", "src/model/model_training.py"])
    elif action == 4:
        print("Predict valence")
        subprocess.check_call(["python3.8", "src/model/model_predictions.py"])
    elif action == 5:
        print("Prepare regression data")
        subprocess.check_call(["python3.8", "hm_replication/form_stata_dta.py"])
    elif action == 6:
        print("Regression analysis")
        subprocess.check_call(["python3.8", "src/model/regression_analysis.py"])
    else:
        click.echo("Action not valid")

if __name__ == '__main__':
    main()