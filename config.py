#===============================================================================
# Configuration
#===============================================================================

import pygame
import json

# configuration values
full_screen = 0 # 0 = no, 1 = yes
scanlines_type = 0 # 0 = none, 1 = fast, 2 = HQ   
map_transition = 0 # 0 = no, 1 = yes
# keyboard
left_key = pygame.K_a
right_key = pygame.K_d
jump_key = pygame.K_w
action_key = pygame.K_s
pause_key = pygame.K_h
mute_key = pygame.K_m

def read():
    global full_screen, scanlines_type, map_transition
    global left_key, right_key, jump_key, action_key, pause_key, mute_key
    # read configuration file
    with open('config.json', 'r') as file:
        config = json.load(file)
    # applies values
    full_screen = config['FULL_SCREEN']
    scanlines_type = config['SCANLINES_TYPE']
    map_transition = config['MAP_TRANSITION']
    left_key = config['LEFT_KEY']
    right_key = config['RIGHT_KEY']
    jump_key = config['JUMP_KEY']
    action_key = config['ACTION_KEY']
    pause_key = config['PAUSE_KEY']
    mute_key = config['MUTE_KEY']

def write_config():
    pass