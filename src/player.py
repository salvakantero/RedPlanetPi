#===============================================================================
# Player class
#===============================================================================

import pygame
import constants
import enums
import globalvars
from globalvars import jp, dp # to build file paths

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
        self.y_velocity = 0
        
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

        # horizontal movement
        newx = self.rect.x
        key_state = pygame.key.get_pressed()
        if key_state[pygame.K_o]:
            newx -= 2
            self.dir = enums.LEFT
        if key_state[pygame.K_p]:
            newx += 2
            self.dir = enums.RIGHT
        newpositionx = pygame.Rect((newx,self.rect.y), (constants.TILE_WIDTH, constants.TILE_HEIGHT))
        index = newpositionx.collidelist(globalvars.tilemap_rect_list) 
        if index == -1:
            self.rect.x = newx

        # vertical movement
        newy = self.rect.y
        self.y_velocity += constants.GRAVITY
        newy += self.y_velocity
        newpositiony = pygame.Rect((self.rect.x, newy), (constants.TILE_WIDTH, constants.TILE_HEIGHT))
        playeronground = False
        ydist = 0
        index = newpositiony.collidelist(globalvars.tilemap_rect_list) 
        if index == -1:
            self.rect.y = newy
        else:
            playeronground = True
            self.y_velocity = 0
        if key_state[pygame.K_q] and playeronground:
            self.y_velocity = constants.JUMP_VALUE
            self.dir = enums.UP
            playeronground = False





        # # movement
        # self.mx = 0
        # self.my = 0
        # key_state = pygame.key.get_pressed()
        # if key_state[pygame.K_o]:
        #     self.mx -= 1
        #     self.dir = enums.LEFT
        # if key_state[pygame.K_p]:
        #     self.mx += 1
        #     self.dir = enums.RIGHT
        # if key_state[pygame.K_q]:
        #     self.my -= 1
        #     self.dir = enums.UP
        # if key_state[pygame.K_a]:            
        #     self.my += 1
        #     self.dir = enums.DOWN
        # self.rect.x += self.mx
        # self.my += constants.GRAVITY
        # self.rect.y += self.my
        # # tilemap collisions
        # index = self.rect.collidelist(globalvars.tilemap_rect_list) 
        # if index >= 0:
        #     beh = globalvars.tilemap_behaviour_list[index]
        #     if beh == enums.OBSTACLE:
        #         self.rect.x -= self.mx
        #         self.rect.y -= self.my