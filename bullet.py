
#===============================================================================
# Bullet class
#===============================================================================

import pygame
import enums
import constants

class Bullet(pygame.sprite.Sprite):
    def __init__(self, pos, dir):
        super().__init__()
        self.dir = dir # left / right
        self.image = pygame.image.load('images/sprites/bullet.png')
        self.image.convert_alpha()
        self.rect = self.image.get_rect(center = pos) # XY position
        
    def update(self):
        # moves the bullet according to the direction
        if self.dir == enums.LEFT: 
            self.rect.x -= 3
        else: 
            self.rect.x += 3
        # eliminates the bullet if it has reached the sides of the screen
        if self.rect.x < 0 or self.rect.x > constants.MAP_UNSCALED_SIZE[0]:
            self.kill()