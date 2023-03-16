
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
        self.scanlines_type = 1 # 0 = none, 1 = fast, 2 = HQ   
        self.map_transition = 1 # 0 = no, 1 = yes
        self.control = 0 # 0 = classic, 1 = gamer, 2 = retro, 3 = gamepad
        # default values
        self.jump_key = pygame.K_UP
        self.action_key = pygame.K_DOWN
        self.left_key = pygame.K_LEFT
        self.right_key = pygame.K_RIGHT
        self.fire_key = pygame.K_SPACE
        self.mute_key = pygame.K_m

    def read(self):
        # read configuration file
        with open('config.json', 'r') as file:
            config = json.load(file)
        # applies values
        self.full_screen = config['FULL_SCREEN']
        self.scanlines_type = config['SCANLINES_TYPE']
        self.map_transition = config['MAP_TRANSITION']
        self.control = config['CONTROL']
        self.apply_controls()

    def write(self):
        pass

    def apply_controls(self):
        # control keys
        if self.control == 0: # classic
            self.jump_key = pygame.K_UP
            self.action_key = pygame.K_DOWN
            self.left_key = pygame.K_LEFT
            self.right_key = pygame.K_RIGHT
        elif self.control == 1: # gamer
            self.jump_key = pygame.K_w
            self.action_key = pygame.K_s
            self.left_key = pygame.K_a
            self.right_key = pygame.K_d
        elif self.control == 2: # retro
            self.jump_key = pygame.K_q
            self.action_key = pygame.K_a
            self.left_key = pygame.K_o
            self.right_key = pygame.K_p
    