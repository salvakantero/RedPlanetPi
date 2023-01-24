
#===============================================================================
# Scoreboard class
#===============================================================================

import pygame
import constants
import enums

class Scoreboard():
    def __init__(self, surface, hotspot_images, font_FL, font_BL, font_FS, font_BS):
        # attributes
        self.surface = surface
        self.font_FL = font_FL # large foreground font
        self.font_BL = font_BL # large background font
        self.font_FS = font_FS # small foreground font
        self.font_BS = font_BS # small background font
        self.needs_updating = False # redrawing of the data if True
        # icons
        self.lives_icon = pygame.image.load('images/assets/lives.png').convert()
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
        self.font_BL.render(constants.MAP_NAMES[map_number], self.surface, (x+2, y+2)) # shadow
        self.font_FL.render(constants.MAP_NAMES[map_number], self.surface, (x, y))
        # print map number
        x = constants.SBOARD_UNSCALED_SIZE[0] - 55
        text_1 = 'SCREEN.....' + str(map_number+1).rjust(2, '0') + '/45'        
        self.font_BS.render(text_1, self.surface, (x+1, y+1)) # shadow
        self.font_FS.render(text_1, self.surface, (x, y))
        # prints a fixed text
        text_2 = 'COMPLETED..'
        self.font_BS.render(text_2, self.surface, (x+1, y+self.font_BS.line_height+1)) # shadow
        self.font_FS.render(text_2, self.surface, (x, y+self.font_FS.line_height))

    # draws a text with its shadow
    def shaded_text(self, data, x, y):
        # shadow
        self.font_BL.render(str(data).rjust(2, '0'), self.surface, (x, y))
        # foreground
        self.font_FL.render(str(data).rjust(2, '0'), self.surface, (x-2, y-2))

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
        self.shaded_text('+50', 116, 6)
        self.shaded_text('+15', 220, 6)

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
            self.font_BS.render(text, self.surface, (x+1, y+1)) # shadow
            self.font_FS.render(text, self.surface, (x, y))