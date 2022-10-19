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
        self.jump_velocity = -7
        
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


    # for p in platforms:
    #     y_collision = newplayerpositiony.colliderect(p) or y_collision
    #     # player collided with ground if player's y position is
    #     # lower than the y position of the platform
    #     if newplayerpositiony.colliderect(p) and (player.y < p.y):
    #         playeronground = True or playeronground
    #         # stick the player to the ground
    #         player.y = p.y - player.h

    # # player no longer has vertical velocity
    # # if colliding with a platform
    # if y_collision:
    #     player.y_velocity = 0
    # # only allow the player to move if it
    # # doesn't collide with any platforms
    # else:
    #     player.y = newy

    # # pressing space sets a negative vertical velocity
    # # only if player is on the ground
    # if keyboard.space and playeronground:
    #     player.y_velocity = player.jump_velocity






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