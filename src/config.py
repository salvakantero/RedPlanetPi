#===============================================================================
# Configuration
#===============================================================================

import json
from globalvars import jp, dp

cfg_full_screen = 0 # 0 = no, 1 = yes
cfg_scanlines_type = 0 # 0 = none, 1 = fast, 2 = HQ   
cfg_map_transition = 0 # 0 = no, 1 = yes

def read_config():
    # read configuration file
    with open(jp(dp,'config.json'), 'r') as file:
        config = json.load(file)
    # 0 = no, 1 = yes
    cfg_full_screen = config['FULL_SCREEN']
    # 0 = none, 1 = fast, 2 = HQ
    cfg_scanlines_type = config['SCANLINES_TYPE']
    # 0 = no, 1 = yes
    cfg_map_transition = config['MAP_TRANSITION']

def write_config():
    pass