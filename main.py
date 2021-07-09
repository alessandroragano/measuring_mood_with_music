import click
import subprocess

@click.command()
@click.option('--action', default=4, help="Choose what script you want to run. 1) Feature Computation, 2) Hyperparameter tuning, 3) Model training and valence prediction, 4) Music Valence Index and Life Satisfaction analysis")
#@click.option('--action', prompt='Your name', 
#              help='The person to greet.')
def main(action):
    click.echo(action)
    if action == 1:
        subprocess.check_call(["python3.8", "src/features/audio_processing.py"])
    elif action == 2:
        subprocess.check_call(["python3.8", "src/model/model_tuning.py"])
    elif action == 3:
        subprocess.check_call(["python3.8", "src/model/model_training.py"])
    elif action == 4:
        subprocess.check_call(["python3.8", "hm_replication/form_stata_dta.py"])
    else:
        click.echo("Your input value is not valid")


if __name__ == '__main__':
    main()