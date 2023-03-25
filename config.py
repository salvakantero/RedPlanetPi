
# ==============================================================================
# .::Configuration class::.
# Save/Load the configuration file.
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
import pickle
import os
import enums

class Configuration():
    def __init__(self):
        self.filename = 'config.dat'
        self.data = { # default values
            'full_screen' : False,
            'scanlines' : 1, # 0 = none, 1 = fast, 2 = HQ   
            'map_transition' : True, # 0 = no, 1 = yes
            'control' : enums.CLASSIC # 0 = classic, 1 = gamer, 2 = retro, 3 = joypad
        }
        # default values for controls (classic layout)
        self.jump_key = pygame.K_UP
        self.action_key = pygame.K_DOWN
        self.left_key = pygame.K_LEFT
        self.right_key = pygame.K_RIGHT
        self.fire_key = pygame.K_SPACE
        self.mute_key = pygame.K_m

    def save(self):
        with open(self.filename, "wb") as f:
            pickle.dump(self.data, f)

    def load(self):
        if os.path.exists(self.filename):
            with open(self.filename, "rb") as f:
                self.data = pickle.load(f)
            self.apply_controls()

    def apply_controls(self):
        # control keys
        if self.data['control'] == enums.CLASSIC:
            self.jump_key = pygame.K_UP
            self.action_key = pygame.K_DOWN
            self.left_key = pygame.K_LEFT
            self.right_key = pygame.K_RIGHT
        elif self.data['control'] == enums.GAMER:
            self.jump_key = pygame.K_w
            self.action_key = pygame.K_s
            self.left_key = pygame.K_a
            self.right_key = pygame.K_d
        elif self.data['control'] == enums.RETRO:
            self.jump_key = pygame.K_q
            self.action_key = pygame.K_a
            self.left_key = pygame.K_o
            self.right_key = pygame.K_p
    
    # create a joystick/joypad/gamepad object
    def prepare_joystick(self):
        joystick = None
        if self.data['control'] == enums.JOYSTICK:
            try: # find a joystick/joypad/gamepad
                joystick = pygame.joystick.Joystick(0)
                joystick.init()
            except Exception: # No device was found
                self.data['control'] == enums.CLASSIC
        return joystick