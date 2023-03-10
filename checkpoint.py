
#===============================================================================
# .::Checkpoint class::.
# Save/Load system
#===============================================================================
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
import constants


class Checkpoint():
    def __init__(self):
        self.filename = 'checkpoint.dat'
        self.data = { # default values...
            'map_number' : 0,
            'player_lives' : 10,
            'player_ammo' : 5,
            'player_keys' : 0,
            'player_TNT' : 0,
            'player_oxygen' : constants.MAX_OXYGEN,
            'player_stacked_TNT' : False,
            'player_facing_right' : True,
            'player_rect' : pygame.Rect(16,112, constants.TILE_SIZE, constants.TILE_SIZE),
            'player_score' : 0   
        }

    def save(self):
        with open(self.filename, "wb") as f:
            pickle.dump(self.data, f)

    def load(self):
        if os.path.exists(self.filename):
            with open(self.filename, "rb") as f:
                self.data = pickle.load(f)


        # save game
        # checkpoint.data = {
        #     'map_number' : map.number,
        #     'player_lives' : player.lives,
        #     'player_ammo' : player.ammo,
        #     'player_keys' : player.keys,
        #     'player_TNT' : player.TNT,
        #     'player_oxygen' : player.oxygen,
        #     'player_stacked_TNT' : player.stacked_TNT,
        #     'player_facing_right' : player.facing_right,
        #     'player_rect' : player.rect
        #     'player_score' : player. 
        # }
        # checkpoint.save()

        # load game
        # checkpoint.load()
        # d = checkpoint.data
        # map.number = d['map_number']
        # map.last = -1
        # player.lives = d['player_lives']
        # player.ammo = d['player_ammo']
        # player.keys = d['player_keys']
        # player.TNT = d['player_TNT']
        # player.oxygen = d['player_oxygen']
        # player.stacked_TNT = d['player_stacked_TNT']
        # player.facing_right = d['player_facing_right']
        # player.rect = d['player_rect']
        # player.score = d['player_score']
        
