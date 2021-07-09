import json
import subprocess

# Configuration file
with open('config.json') as config_file:
    config = json.load(config_file)

cmd = [config['stata_installation_path'], "do", config['do_file']]
subprocess.call(cmd)
print("Stata script executed")