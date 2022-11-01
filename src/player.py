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
        
        # loads the lists of images for each state and direction
        path = 'images/sprites/player'
        self.animations_right = {'idle':[],'run':[],'jump':[],'fall':[]}
        self.animations_right.idle.add:
            self.animations_right[animation] = pygame.image.load(
                jp(dp, path + '0.png')).convert()

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

        key_state = pygame.key.get_pressed()

        # horizontal movement
        temp_x = self.rect.x 
        # X varies depending on the key pressed       
        if key_state[pygame.K_o]:
            temp_x -= 2
            self.dir = enums.LEFT
        if key_state[pygame.K_p]:
            temp_x += 2
            self.dir = enums.RIGHT
        # gets the new rectangle and check for collision
        temp_rect = pygame.Rect((temp_x,self.rect.y), 
            (constants.TILE_WIDTH, constants.TILE_HEIGHT))
        index = temp_rect.collidelist(globalvars.tilemap_rect_list) 
        # no collision. Apply the new position X
        if index == -1:
            self.rect.x = temp_x

        # vertical movement
        temp_y = self.rect.y
        # applies acceleration of gravity
        self.y_velocity += constants.GRAVITY
        temp_y += self.y_velocity
        # gets the new rectangle and check for collision
        temp_rect = pygame.Rect((self.rect.x, temp_y), 
            (constants.TILE_WIDTH, constants.TILE_HEIGHT))
        on_ground = False
        index = temp_rect.collidelist(globalvars.tilemap_rect_list)         
        if index == -1: # no collision. Apply the new position Y
            self.rect.y = temp_y
        else:
            on_ground = True
            self.y_velocity = 0

        if key_state[pygame.K_q] and on_ground:
            self.y_velocity = constants.JUMP_VALUE
            self.dir = enums.UP
            on_ground = False
