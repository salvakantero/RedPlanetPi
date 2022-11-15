#===============================================================================
# Player class
#===============================================================================

import pygame
import constants
import enums
import config
import tiled

class Player(pygame.sprite.Sprite):
    def __init__(self, image_list):
        super().__init__()
        # properties
        self.lives = 10 # lives remaining
        self.oxigen = 99 # oxigen remaining
        self.ammo = 5 # unused ammunition collected
        self.keys = 0 # unused keys collected 
        self.explosives = 0 # explosives collected        
        self.state = enums.IDLE # to know the animation to be applied
        self.facing_right = True # to know if the sprite needs to be mirrored
        self.on_ground = False # perched on the ground
        self.y_speed = 0 # motion + gravity
        # image/animation
        self.image_list = image_list # list of images for animation
        self.frame_index = 0 # frame_number
        self.animation_timer = 16 # timer to change frame
        self.animation_speed = 16 # frame dwell time
        self.image = image_list[self.state][0] # 1st frame of the animation
        self.rect = self.image.get_rect(topleft = (32,112))  # initial position

    def get_input(self):
        # XY temporary to check for collision at the new position
        self.temp_x = self.rect.x 
        self.temp_y = self.rect.y
        # manages keystrokes
        key_state = pygame.key.get_pressed()   
        # press left
        if key_state[config.left_key]:
            self.temp_x -= 2
            self.facing_right = False
            self.state = enums.WALKING
        # press right
        if key_state[config.right_key]:
            self.temp_x += 2
            self.facing_right = True
            self.state = enums.WALKING
        # without lateral movement
        if not key_state[config.left_key] and not key_state[config.right_key]:
            if self.on_ground:
                self.state = enums.IDLE
            elif self.y_speed > 1:
                self.state = enums.FALLING
        # press jump
        if key_state[config.jump_key] and self.on_ground:
            self.y_speed = constants.JUMP_VALUE
            self.state = enums.JUMPING

    def horizontal_mov(self):
        # gets the new rectangle and check for collision
        temp_rect = pygame.Rect((self.temp_x,self.rect.y), 
            (constants.TILE_WIDTH, constants.TILE_HEIGHT))      
        if temp_rect.collidelist(tiled.tilemap_rect_list) == -1:
            self.rect.x = self.temp_x # no collision. Apply the new position X

    def vertical_mov(self):
        # applies acceleration of gravity
        self.y_speed += constants.GRAVITY
        self.temp_y += self.y_speed
        # gets the new rectangle and check for collision
        temp_rect = pygame.Rect((self.rect.x, self.temp_y), 
            (constants.TILE_WIDTH, constants.TILE_HEIGHT))        
        index = temp_rect.collidelist(tiled.tilemap_rect_list)         
        if index == -1: # no collision            
            self.rect.y = self.temp_y # apply the new position Y
            self.on_ground = False
        else: # collision            
            self.y_speed = 0 # stops the player
            # avoid the rebound
            tile = tiled.tilemap_rect_list[index]
            if tile.y > self.temp_y: # sticks to platform                    
                    self.rect.y = tile.y - constants.TILE_HEIGHT
                    self.on_ground = True

    def animate(self):
        # animation
        if (self.state == enums.WALKING):
            self.animation_speed = 6 # running fast
        else:
            self.animation_speed = 16 # breathing, jumping, falling
        self.animation_timer += 1
        # exceeded the frame time?
        if self.animation_timer >= self.animation_speed:
            self.animation_timer = 0 # reset the timer
            self.frame_index += 1 # next frame
        # exceeded the number of frames?
        if self.frame_index > len(self.image_list[self.state]) - 1:
            self.frame_index = 0 # reset the frame number
        # assigns image according to frame, status and direction
        if self.facing_right:
            self.image = self.image_list[self.state][self.frame_index]
        else: # reflects the image when looking to the left
            self.image = pygame.transform.flip(
                self.image_list[self.state][self.frame_index], True, False)
                
    def update(self):
        self.get_input()
        self.horizontal_mov()
        self.vertical_mov()
        self.animate()