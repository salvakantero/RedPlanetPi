
#===============================================================================
# Bullet class
#===============================================================================

import pygame
import constants

class Bullet(pygame.sprite.Sprite):
    def __init__(self, pos, facing_right):
        super().__init__()
        self.facing_right = facing_right
        self.speed = 4
        self.image = pygame.image.load('images/sprites/bullet.png')
        self.image.convert_alpha()
        # positions the bullet in front of the weapon
        self.rect = self.image.get_rect(center = pos.center)
        if facing_right: self.rect.x = pos.right
        else: self.rect.x = pos.left - self.rect.width
        
    def update(self):
        # moves the bullet according to the direction
        if self.facing_right: 
            self.rect.x += self.speed
        else: 
            self.rect.x -= self.speed 
        # eliminates the bullet if it has reached the sides of the screen
        if self.rect.x < 0 or self.rect.x > constants.MAP_UNSCALED_SIZE[0]:
            self.kill()