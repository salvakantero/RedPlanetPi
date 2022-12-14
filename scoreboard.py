import pygame
import globalvars

class Scoreboard():
    def __init__(self, surface, fg_font, bg_font):
        self.surface = surface
        self.fg_font = fg_font
        self.bg_font = bg_font
        self.needs_updating = False
        # icons
        self.lives_icon = pygame.image.load('images/assets/lives.png').convert()
        self.oxigen_icon = pygame.image.load('images/tiles/T53.png').convert()
        self.ammo_icon = pygame.image.load('images/tiles/T52.png').convert()
        self.keys_icon = pygame.image.load('images/tiles/T51.png').convert()
        self.tnt_icon = pygame.image.load('images/tiles/T50.png').convert()
        
    # Draws the entire scoreboard
    def reset(self):
        # icons
        self.surface.blit(self.lives_icon, (0, 2))
        self.surface.blit(self.oxigen_icon, (42, 2))
        self.surface.blit(self.ammo_icon, (82, 2))
        self.surface.blit(self.keys_icon, (145, 2))
        self.surface.blit(self.tnt_icon, (186, 2))
        # fixed texts
        self.bg_font.render('+50', self.surface, (116, 6))
        self.fg_font.render('+50', self.surface, (114, 4))
        self.bg_font.render('+15', self.surface, (220, 6))
        self.fg_font.render('+15', self.surface, (218, 4))

    # forces the redrawing of the data
    def invalidate(self):
        self.needs_updating = True

    # Update the data (only if it has been invalidated)
    def update(self, player):
        if self.needs_updating:
            pygame.draw.rect(self.surface, globalvars.PALETTE['BLACK'], ((18,4),(13,12)))
            self.bg_font.render(str(player.lives).rjust(2, '0'), self.surface, (20, 6))
            self.fg_font.render(str(player.lives).rjust(2, '0'), self.surface, (18, 4))
            self.bg_font.render(str(player.oxigen).rjust(2, '0'), self.surface, (62, 6))
            self.fg_font.render(str(player.oxigen).rjust(2, '0'), self.surface, (60, 4))
            self.bg_font.render(str(player.ammo).rjust(2, '0'), self.surface, (102, 6))
            self.fg_font.render(str(player.ammo).rjust(2, '0'), self.surface, (100, 4))
            self.bg_font.render(str(player.keys).rjust(2, '0'), self.surface, (166, 6))
            self.fg_font.render(str(player.keys).rjust(2, '0'), self.surface, (164, 4))
            self.bg_font.render(str(player.explosives).rjust(2, '0'), self.surface, (206, 6))
            self.fg_font.render(str(player.explosives).rjust(2, '0'), self.surface, (204, 4))
            self.needs_updating = False