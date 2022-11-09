#===============================================================================
# Configuration
#===============================================================================

import json

def read():
    # read configuration file
    with open('config.json', 'r') as file:
        config = json.load(file)
    return config['FULL_SCREEN'], config['SCANLINES_TYPE'], config['MAP_TRANSITION']

def write_config():
    pass