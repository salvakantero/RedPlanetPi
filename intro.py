
# ==============================================================================
# .::Intro class::.
# An introduction with graphics and sound as an introduction to the game
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
import support
import constants
import enums

class Intro():
    def __init__(self, screen):
        self.screen = screen
        self.img_logo = pygame.image.load('images/assets/logo.png').convert() # PlayOnRetro  
        self.img_intro1 = pygame.image.load('images/assets/intro1.png').convert() # background
        self.img_intro2 = pygame.image.load('images/assets/intro2.png').convert_alpha() # title
        self.img_intro3 = pygame.image.load('images/assets/intro3.png').convert_alpha() # pi
        self.sfx_intro1 = pygame.mixer.Sound('sounds/fx/sfx_intro1.wav') # flash effect
        self.sfx_intro2 = pygame.mixer.Sound('sounds/fx/sfx_intro2.wav') # text sliding
        self.sfx_intro3 = pygame.mixer.Sound('sounds/fx/sfx_intro3.wav') # PlayOnRetro
        self.sfx_intro3.set_volume(.4)
        # auxiliary surface for fading and flashing visual effects
        self.srf_aux = pygame.Surface(constants.MENU_UNSCALED_SIZE, pygame.SRCALPHA)

    def fades_surface(self, target_surf, aux_surf, opacity, delay):
        aux_surf.set_alpha(0) # totally transparent    
        for z in range(opacity):
            aux_surf.set_alpha(z) # opacity is being applied
            target_surf.blit(aux_surf, (0,0)) # the two surfaces come together to be drawn
            self.screen.update(enums.OVER) # draw target_surf
            pygame.time.wait(delay) # speed of transition

    def play(self):
        # PlayOnRetro logo
        # fade in
        self.screen.srf_menu.fill(constants.PALETTE["BLACK"]) # black background
        self.srf_aux.blit(self.img_logo, (0, 0))
        self.fades_surface(self.screen.srf_menu, self.srf_aux, 45, 12)
        if support.main_key_pressed(): return # allows skipping the intro
        self.sfx_intro3.play()
        pygame.time.wait(1500)
        if support.main_key_pressed(): return
        # fade out
        self.srf_aux.fill(constants.PALETTE["BLACK"]) # black background
        self.fades_surface(self.screen.srf_menu, self.srf_aux, 45, 12)
        if support.main_key_pressed(): return # allows skipping the intro 
        pygame.time.wait(1500)
        if support.main_key_pressed(): return

        # RedPlanetPi
        self.sfx_intro1.play()
        self.screen.srf_menu.fill(constants.PALETTE["WHITE"]) # white background
        self.srf_aux.blit(self.img_intro1, (0, 0))
        self.fades_surface(self.screen.srf_menu, self.srf_aux, 50, 8)
        pygame.time.wait(200)
        if support.main_key_pressed(): return # allows skipping the intro
        # slide the title "RED PLANET" from the right to its final position
        self.sfx_intro2.play()
        for x in range(-170, 0, 10):
            self.screen.srf_menu.blit(self.img_intro1, (0, 0))
            self.screen.srf_menu.blit(self.img_intro2, (x, 0))
            self.screen.update(enums.OVER)
        # slides the PI from the bottom to its final position
        self.sfx_intro2.play()
        for y in range(140, -5, -10):
            self.screen.srf_menu.blit(self.img_intro1, (0, 0))
            self.screen.srf_menu.blit(self.img_intro2, (0, 0))
            self.screen.srf_menu.blit(self.img_intro3, (198, y))
            self.screen.update(enums.OVER)
        if support.main_key_pressed(): return # allows skipping the intro
        # pause for recreation. Ooohhh how wonderful!
        pygame.time.wait(500)