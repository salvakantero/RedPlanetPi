
# ==============================================================================
# .::Screen class::.
# refreshes the screen, scaling its content x 3 and applying scanlines.
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
import random
import constants
import enums

class Screen():
    def __init__(self, clock, config):
        self.menu_surf = pygame.Surface(constants.MENU_UNSCALED_SIZE)
        self.map_surf = pygame.Surface(constants.MAP_UNSCALED_SIZE)
        self.sboard_surf = pygame.Surface(constants.SBOARD_UNSCALED_SIZE)
        self.clock = clock
        self.config = config
        # generates a main window (or full screen) with title, icon, and 32-bit colour.
        flags = 0
        if self.config.full_screen: flags = pygame.FULLSCREEN
        self.screen = pygame.display.set_mode(constants.WIN_SIZE, flags, 32)
        pygame.display.set_caption('.:: Red Planet Pi ::.')
        icon = pygame.image.load('images/assets/intro3.png').convert_alpha()
        pygame.display.set_icon(icon)
        # surface for HQ scanlines
        self.scanlines_surf = pygame.Surface(constants.WIN_SIZE)
        self.scanlines_surf.set_alpha(40)

    # draws scanlines
    def scanlines(self, surface, height, from_x, to_x, rgb):
        j = constants.V_MARGIN # Y axis
        while j < height:
            j+=3
            pygame.draw.line(surface, (rgb, rgb, rgb), (from_x, j), (to_x, j))

    # applies scanlines according to the configuration
    def apply_scanlines(self):
        if self.config.scanlines_type == 2: # HQ
            self.scanlines(self.scanlines_surf, constants.WIN_SIZE[1]-30, constants.H_MARGIN, 
                constants.WIN_SIZE[0]-constants.H_MARGIN-1, 200)
            self.screen.blit(self.scanlines_surf, (0, 0))
        elif self.config.scanlines_type == 1: # fast
            self.scanlines(self.screen, constants.WIN_SIZE[1]-30, constants.H_MARGIN, 
                constants.WIN_SIZE[0]-constants.H_MARGIN-1, 15)

    # dumps and scales surfaces to the screen
    def update(self, game_status):
        if game_status == enums.OVER:
            # scale x 3 the menu
            self.screen.blit(pygame.transform.scale(
                self.menu_surf, constants.MENU_SCALED_SIZE),
                (constants.H_MARGIN, constants.V_MARGIN))
        else:
            # shakes the surface of the map if it has been requested
            offset = [0,0]
            if map.shake_timer > 0:
                if map.shake_timer == 1: # last frame shaken   
                    # it's necessary to clean the edges of the map after shaking it         
                    pygame.draw.rect(self.screen, constants.PALETTE['BLACK'], (20, 120 , 20 , 500))
                    pygame.draw.rect(self.screen, constants.PALETTE['BLACK'], (760, 120 , 20 , 500))
                    pygame.draw.rect(self.screen, constants.PALETTE['BLACK'], (40, 610 , 720 , 20))
                else:
                    offset[0] = random.randint(-map.shake[0], map.shake[0])
                    offset[1] = random.randint(-map.shake[1], map.shake[1])
                map.shake_timer -= 1
            # scale x 3 the scoreboard
            self.screen.blit(pygame.transform.scale(
                self.sboard_surf, constants.SBOARD_SCALED_SIZE), 
                (constants.H_MARGIN, constants.V_MARGIN))
            # scale x 3 the map
            self.screen.blit(pygame.transform.scale(
                self.map_surf, constants.MAP_SCALED_SIZE), (constants.H_MARGIN + offset[0], 
                constants.SBOARD_SCALED_SIZE[1] + constants.V_MARGIN + offset[1]))

        self.apply_scanlines()
        pygame.display.update() # refreshes the screen
        self.clock.tick(60) # 60 FPS
