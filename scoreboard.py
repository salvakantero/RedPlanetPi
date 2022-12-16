import pygame
import constants

class Scoreboard():
    def __init__(self, surface, fg_font_L, bg_font_L, fg_font_S, bg_font_S):
        # attributes
        self.surface = surface
        self.fg_font_L = fg_font_L # large foreground font
        self.bg_font_L = bg_font_L # large background font
        self.fg_font_S = fg_font_S # small foreground font
        self.bg_font_S = bg_font_S # small background font
        self.needs_updating = False # redrawing of the data if True
        # icons
        self.lives_icon = pygame.image.load('images/assets/lives.png').convert()
        self.oxigen_icon = pygame.image.load('images/tiles/T53.png').convert()
        self.ammo_icon = pygame.image.load('images/tiles/T52.png').convert()
        self.keys_icon = pygame.image.load('images/tiles/T51.png').convert()
        self.tnt_icon = pygame.image.load('images/tiles/T50.png').convert()

    # draws the name of the map and other data
    def map_info(self, map_number, game_percent):
        # print map name
        x = 0
        y = 22
        self.bg_font_L.render(
            constants.MAP_NAMES[map_number], self.surface, (x+2, y+2)) # shadow
        self.fg_font_L.render(
            constants.MAP_NAMES[map_number], self.surface, (x, y))
        # print map number and game percentage
        x = constants.SBOARD_UNSCALED_SIZE[0] - 55
        text_1 = 'SCREEN.....' + str(map_number+1).rjust(2, '0') + '/45'
        text_2 = 'COMPLETED..' + str(game_percent).rjust(2, '0') + ';' # %
        self.bg_font_S.render(text_1, self.surface, (x+1, y+1)) # shadow
        self.fg_font_S.render(text_1, self.surface, (x, y))
        self.bg_font_S.render(text_2, self.surface, 
            (x+1, y+self.bg_font_S.line_height+1)) # shadow
        self.fg_font_S.render(text_2, self.surface, 
            (x, y+self.fg_font_S.line_height))

    # draws a text with its shadow
    def shaded_text(self, data, x, y):
        # shadow
        self.bg_font_L.render(str(data).rjust(2, '0'), self.surface, (x, y))
        # foreground
        self.fg_font_L.render(str(data).rjust(2, '0'), self.surface, (x-2, y-2))

    # draws the entire scoreboard
    def reset(self):
        # delete the entire scoreboard
        self.surface.fill((0,0,0))
        # icons
        self.surface.blit(self.lives_icon, (0, 2))
        self.surface.blit(self.oxigen_icon, (42, 2))
        self.surface.blit(self.ammo_icon, (82, 2))
        self.surface.blit(self.keys_icon, (145, 2))
        self.surface.blit(self.tnt_icon, (186, 2))
        # fixed texts
        self.shaded_text('+50', 116, 6)
        self.shaded_text('+15', 220, 6)

    # forces the redrawing of the data
    def invalidate(self):
        self.needs_updating = True

    # update the data (only if it has been invalidated)
    def update(self, player):
        if self.needs_updating:
            # clean the previous data
            pygame.draw.rect(self.surface, 
                constants.PALETTE['BLACK'], ((18,4),(13,12))) 
            # draws the new data
            self.shaded_text(player.lives, 20, 6)
            self.shaded_text(player.oxigen, 62, 6)
            self.shaded_text(player.ammo, 102, 6)
            self.shaded_text(player.keys, 166, 6)
            self.shaded_text(player.explosives, 206, 6)
            self.needs_updating = False