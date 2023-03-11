
# ==============================================================================
# .::Configuration class::.
# Reads and writes to the json configuration file.
# Makes the configuration accessible from the attributes of class.
# ==============================================================================
#
#  This file is part of "Red Planet Pi". Copyright (C) 2023 @salvakantero
#
#  This program is free software: you can redistribute it and/or modify
#  it under the terms of the GNU Lesser General Public License as published by
#  the Free Software Foundation, either version 3 of the License, or
#  (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU Lesser General Public License
#  along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
# ==============================================================================

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
        # self.mute_key = config['MUTE_KEY']

    def write(self):
        pass
    