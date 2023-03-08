
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

import pickle


class Checkpoint():
    def __init__(self, map_number, player, game):
        self.filename = 'checkpoint.dat'
        self.data = [
            map_number,
            player.lives,
            player.ammo,
            player.keys,
            player.TNT,
            player.oxygen,
            player.stacked_TNT,
            player.state,
            player.facing_right,
            player.on_ground,
            player.direction,
            player.rect,
            game.music_status,
            game.all_sprites_group,     
            game.enemies_group,
            game.hotspot_group,
            game.gate_group,
            game.platform_group
        ]

    def save(self):
        with open(self.filename, "wb") as f:
            pickle.dump(self, f)

    def load(self):
        with open(self.filename, "rb") as f:
            return pickle.load(f)


# import pygame

# # Clase del juego
# class Game:
#     def __init__(self):
#         self.score = 0
#         self.player_position = (0, 0)

# # Función para guardar el estado del juego
# def save_game(game, filename):
#     with open(filename, "wb") as f:
#         pickle.dump(game, f)

# # Función para cargar el estado del juego
# def load_game(filename):
#     with open(filename, "rb") as f:
#         return pickle.load(f)

# # Inicializar el juego
# game = Game()
# game.score = 10
# game.player_position = (100, 200)

# # Guardar el juego
# save_game(game, "save.dat")

# # Cargar el juego
# loaded_game = load_game("save.dat")
# print(loaded_game.score) # Imprime 10
# print(loaded_game.player_position) # Imprime (100, 200)
