#===============================================================================
# Player class
#===============================================================================

import pygame
import enums
import globalvars
from globalvars import jp, dp

class Player(pygame.sprite.Sprite):
    def __init__(self):
        super(Player, self).__init__()
        # properties
        self.lives = 10
        self.oxigen = 99
        self.ammo = 5
        self.keys = 0
        self.explosives = 0
        self.dir = enums.RIGHT
        # images
        num_frames = 3
        self.images = []
        for i in range(num_frames):
            # image for the frame
            self.images.append(pygame.image.load(
                jp(dp, 'images/sprites/player{}.png'.format(i))).convert())
            # mask
            self.images[i].set_colorkey((255, 0, 255))
        self.animation_index = 0
        self.animation_speed = 0.08
        self.image = self.images[self.animation_index]
        # initial position
        self.rect = self.image.get_rect()
        self.rect.x = 32
        self.rect.y = 112

    def update(self):
        # animation
        self.animation_index += self.animation_speed
        if self.animation_index >= len(self.images):
            self.animation_index = 0
        self.image = self.images[int(self.animation_index)]
        # movement
        self.mx = 0
        self.my = 0
        key_state = pygame.key.get_pressed()
        if key_state[pygame.K_o]:
            self.mx -= 1
            self.dir = enums.LEFT
        if key_state[pygame.K_p]:
            self.mx += 1
            self.dir = enums.RIGHT
        if key_state[pygame.K_q]:
            self.my -= 1
            self.dir = enums.UP
        if key_state[pygame.K_a]:            
            self.my += 1
            self.dir = enums.DOWN
        self.rect.x += self.mx
        self.rect.y += self.my
        # tilemap collisions
        index = self.rect.collidelist(globalvars.tilemap_rect_list) 
        if index >= 0:
            beh = globalvars.tilemap_behaviour_list[index]
            if beh == enums.OBSTACLE:
                self.rect.x -= self.mx
                self.rect.y -= self.my