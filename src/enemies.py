
#===============================================================================
# Enemy class and functions
#===============================================================================

import pygame
from globalvars import jp, dp, tile_width, tile_height


class Enemy(pygame.sprite.Sprite):
    def __init__(self, enemy_type, mov, dir, pos, limit):
        super(Enemy, self).__init__()
 
        self.images = []
        # frame 1
        self.images.append(pygame.image.load(
            jp(dp, "images/sprites/" + enemy_type.name + "0.png")).convert())
        # frame 2
        self.images.append(pygame.image.load(
            jp(dp, "images/sprites/" + enemy_type.name + "1.png")).convert())
  
        self.index = 0
        self.animation_speed = 0.08
        self.image = self.images[self.index]
        self.mov = mov
        self.dir = dir
        self.rect = pygame.Rect(
            pos[0]*tile_width, pos[1]*tile_height, tile_width, tile_height)
 
    def update(self):
        # animation
        self.index += self.animation_speed
        if self.index >= len(self.images):
            self.index = 0
        self.image = self.images[int(self.index)]
        
        # movement

