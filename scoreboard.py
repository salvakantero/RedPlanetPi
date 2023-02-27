
# ==============================================================================
# .::Scoreboard class::.
# Draws the scoreboard and refreshes its data.
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
import constants
import enums

class Scoreboard():
    def __init__(self, surface, fonts, hotspot_images):
        # attributes
        self.surface = surface
        self.fonts = fonts
        self.needs_updating = False # redrawing of the data if True
        # icons
        self.lives_icon = pygame.image.load('images/sprites/player0.png').convert()
        self.hotspot_images = hotspot_images

        # Game Percentage %
        # ----------------------------
        # TNT           15 * 3     45%
        # Keys           9 * 2     18%
        # Gates          9 * 3     27%
        # Locate TNT     1 * 5      5%
        # Detonator      1 * 5      5%
        #                         ----
        # TOTAL:                  100%
        self.game_percent = 0

    # draws the name of the map and other data
    def map_info(self, map_number):
        # print map name
        x = 0
        y = 22
        self.fonts[enums.L_B_WHITE].render(constants.MAP_NAMES[map_number], self.surface, (x+2, y+2)) # shadow
        self.fonts[enums.L_F_WHITE].render(constants.MAP_NAMES[map_number], self.surface, (x, y))
        # print map number
        x = constants.SBOARD_UNSCALED_SIZE[0] - 55
        text_1 = 'SCREEN.....' + str(map_number+1).rjust(2, '0') + '/45'        
        self.fonts[enums.S_B_GREEN].render(text_1, self.surface, (x+1, y+1)) # shadow
        self.fonts[enums.S_F_GREEN].render(text_1, self.surface, (x, y))
        # prints a fixed text
        text_2 = 'COMPLETED..'
        self.fonts[enums.S_B_GREEN].render(text_2, self.surface, (x+1, y+self.fonts[enums.S_B_GREEN].line_height+1)) # shadow
        self.fonts[enums.S_F_GREEN].render(text_2, self.surface, (x, y+self.fonts[enums.S_F_GREEN].line_height))

    # draws a text with its shadow
    def shaded_text(self, data, x, y):       
        self.fonts[enums.L_B_WHITE].render(str(data).rjust(2, '0'), self.surface, (x, y))  # shadow
        self.fonts[enums.L_F_WHITE].render(str(data).rjust(2, '0'), self.surface, (x-2, y-2))

    # draws the entire scoreboard
    def reset(self):
        # delete the entire scoreboard
        self.surface.fill((0,0,0))
        # icons
        self.surface.blit(self.lives_icon, (0, 2))
        self.surface.blit(self.hotspot_images[enums.OXYGEN], (42, 2))
        self.surface.blit(self.hotspot_images[enums.AMMO], (82, 2))
        self.surface.blit(self.hotspot_images[enums.KEY], (145, 2))
        self.surface.blit(self.hotspot_images[enums.TNT], (186, 2))
        # fixed texts
        self.shaded_text('\'50', 116, 6) # ' = /
        self.shaded_text('\'15', 220, 6)

    # forces the redrawing of the data
    def invalidate(self):
        self.needs_updating = True

    # clean the previous data
    def clear_zone(self, x):
        pygame.draw.rect(self.surface, constants.PALETTE['BLACK'], ((x, 4),(13, 12)))

    # update the data (only if it has been invalidated)
    def update(self, player):
        if self.needs_updating:
            # player data
            self.clear_zone(18)
            self.shaded_text(player.lives, 20, 6)
            self.clear_zone(60)
            self.shaded_text(player.oxygen, 62, 6)
            self.clear_zone(100)
            self.shaded_text(player.ammo, 102, 6)
            self.clear_zone(164)
            self.shaded_text(player.keys, 166, 6)
            self.clear_zone(204)
            self.shaded_text(player.TNT, 206, 6)
            self.needs_updating = False
            # game percentage
            x = constants.SBOARD_UNSCALED_SIZE[0] - 13
            y = 30
            pygame.draw.rect(self.surface, constants.PALETTE['BLACK'], ((x, y),(8, 8)))
            text = str(self.game_percent).rjust(2, '0') + ';' # ; = %
            self.fonts[enums.S_B_GREEN].render(text, self.surface, (x+1, y+1)) # shadow
            self.fonts[enums.S_F_GREEN].render(text, self.surface, (x, y))