
#===============================================================================
# Configuration class
#===============================================================================

import pygame
import json

class Configuration():
    def __init__(self):
        self.full_screen = 0 # 0 = no, 1 = yes
        self.scanlines_type = 0 # 0 = none, 1 = fast, 2 = HQ   
        self.map_transition = 0 # 0 = no, 1 = yes
        self.show_fps = 1 # 0 = no, 1 = yes
        # keyboard
        self.left_key = pygame.K_o
        self.right_key = pygame.K_p
        self.jump_key = pygame.K_q
        self.fire_key = pygame.K_SPACE
        self.action_key = pygame.K_a
        self.pause_key = pygame.K_h
        self.mute_key = pygame.K_m

    def read(self):
        # read configuration file
        with open('config.json', 'r') as file:
            config = json.load(file)
        # applies values
        self.full_screen = config['FULL_SCREEN']
        self.scanlines_type = config['SCANLINES_TYPE']
        self.map_transition = config['MAP_TRANSITION']
        self.show_fps = config['SHOW_FPS']
        # self.left_key = config['LEFT_KEY']
        # self.right_key = config['RIGHT_KEY']
        # self.jump_key = config['JUMP_KEY']
        # self.fire_key = config['FIRE_KEY']
        # self.action_key = config['ACTION_KEY']
        # self.pause_key = config['PAUSE_KEY']
        # self.mute_key = config['MUTE_KEY']

    def write_config(self):
        pass
    