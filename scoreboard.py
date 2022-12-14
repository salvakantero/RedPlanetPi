import pygame
import globalvars

class Scoreboard():
    def __init__(self, surface):
        self.surface = surface
        self.need_refresh = False
        # icons
        self.lives_icon = pygame.image.load('images/assets/lives.png').convert()
        self.oxigen_icon = pygame.image.load('images/tiles/T53.png').convert()
        self.ammo_icon = pygame.image.load('images/tiles/T52.png').convert()
        self.keys_icon = pygame.image.load('images/tiles/T51.png').convert()
        self.tnt_icon = pygame.image.load('images/tiles/T50.png').convert()
        
    # Draw the entire scoreboard
    def render(self):
        pass

    # Update the data
    def update(self):
        pass