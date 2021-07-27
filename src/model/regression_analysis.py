import json
import subprocess
import os

# Configuration file
with open('config.json') as config_file:
    config = json.load(config_file)

os.chdir(config['do_path'])
cmd = [config['stata_installation_path'], "do", config['do_file']]
subprocess.call(cmd)
print("Stata script executed")