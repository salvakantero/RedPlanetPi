
#===============================================================================
# Player class
# movement and animations, collisions with the map
#===============================================================================

import pygame
from math import sin

import constants
import enums
import dust

class Player(pygame.sprite.Sprite):
    def __init__(self, image_list, dust_image_list, all_sprites_group, 
        dust_group, map, scoreboard, config):
        super().__init__()
        # external attributes
        self.lives = 90 # lives remaining
        self.oxigen = 99 # oxigen remaining
        self.ammo = 5 # unused ammunition collected
        self.keys = 0 # unused keys collected 
        self.explosives = 0 # explosives collected  
        # internal attributes
        self.direction = pygame.math.Vector2(0.0)
        self.x_speed = 2 # movement in the x-axis (pixels)
        self.state = enums.IDLE # to know the animation to be applied
        self.facing_right = True # to know if the sprite needs to be mirrored
        self.on_ground = False # perched on the ground        
        self.invincible = False # invincible after losing a life
        self.invincible_time_from = 0 # tick number where invincibility begins
        self.invincible_time_to = 2000 # time of invincibility (1 sec.)
        # image/animation
        self.image_list = image_list # list of images for animation
        self.frame_index = 0 # frame number
        self.animation_timer = 16 # timer to change frame
        self.animation_speed = 16 # frame dwell time
        self.image = image_list[self.state][0] # 1st frame of the animation
        self.rect = self.image.get_rect(topleft = (16,112))  # initial position
        # dust effect
        self.dust_image_list = dust_image_list
        self.all_sprites_group = all_sprites_group    
        self.dust_group = dust_group    
        # objects and others
        self.map = map
        self.scoreboard = scoreboard
        self.config = config

    # dust effect when jumping or landing
    def dust_effect(self, pos, state):
        if self.dust_group.sprite == None:        
            dust_sprite = dust.DustEffect(pos, self.dust_image_list[state])
            self.dust_group.add(dust_sprite)
            self.all_sprites_group.add(dust_sprite)

    def get_input(self):
        # # XY temporary to check for collision at the new position
        self.x_temp = self.rect.x 
        self.y_temp = self.rect.y
        # manages keystrokes
        key_state = pygame.key.get_pressed()  
        # press right
        if key_state[self.config.right_key]:
            self.direction.x = 1
            self.facing_right = True
        # press left
        elif key_state[self.config.left_key]:
            self.direction.x = -1
            self.facing_right = False
        # without lateral movement
        elif not key_state[self.config.right_key] \
        and not key_state[self.config.left_key]:
            self.direction.x = 0 
        # press jump
        if key_state[self.config.jump_key] and self.on_ground \
        and not self.state == enums.JUMPING:
            self.direction.y = constants.JUMP_VALUE
            self.dust_effect(self.rect.center, enums.JUMPING)

    def get_state(self):
        if self.direction.y < 0: # decrementing Y. Jumping
            self.state = enums.JUMPING
        elif self.direction.y > 1: # increasing Y. Falling
            self.state = enums.FALLING
        else:
            if self.direction.x != 0: # is moving
                self.state = enums.WALKING
            else: # x does not change. Stopped
                self.state = enums.IDLE

    def horizontal_mov(self):
        # gets the new rectangle and check for collision
        self.x_temp += self.direction.x * self.x_speed
        temp_rect = pygame.Rect((self.x_temp,self.rect.y),
            (self.rect.width, self.rect.height))

        collision = False # True if at least one tile collides
        index = -1 # index of the colliding tile to obtain its type
        # it is necessary to check all colliding tiles.
        for tile in self.map.tilemap_rect_list:
            index += 1
            if tile.colliderect(temp_rect) \
            and self.map.tilemap_behaviour_list[index] != enums.PLATFORM_TILE:
                collision = True
                if self.direction.x < 0: # adjusts to the right of the tile
                    self.rect.left = tile.right
                elif self.direction.x > 0: # adjusts to the left of the tile
                    self.rect.right = tile.left
        if not collision:
            self.rect.x = self.x_temp # apply the new X position

    def vertical_mov(self):        
        # applies acceleration of gravity up to the vertical speed limit
        if self.direction.y < constants.MAX_Y_SPEED:
            self.direction.y += constants.GRAVITY
        self.y_temp += self.direction.y

        # gets the new rectangle and check for collision
        temp_rect = pygame.Rect((self.rect.x, self.y_temp), 
            (self.rect.width, self.rect.height))  

        collision = False # True if at least one tile collides
        index = -1 # index of the colliding tile to obtain its type
        # it is necessary to check all colliding tiles.
        for tile in self.map.tilemap_rect_list:
            index += 1
            if tile.colliderect(temp_rect):
                collision = True

                # fixed platform, only stops from above
                if self.map.tilemap_behaviour_list[index] == enums.PLATFORM_TILE:   
                    # if the player is not jumping (if not climbing)    
                    if (self.state is not enums.JUMPING):
                        # if the lower part of the player is below 
                        # the upper part of the platform
                        if tile.y > self.y_temp + 12:
                            # sticks to platform                
                            self.rect.y = tile.y - self.rect.height
                            self.on_ground = True
                            self.direction.y = 0  
                        # if the player is not on top of the platform
                        # it keeps moving
                        else: collision = False
                    # if it's jumping it keeps moving
                    else: collision = False

                # obstacles, stops the player from all directions      
                elif self.map.tilemap_behaviour_list[index] == enums.OBSTACLE:
                    self.direction.y = 0
                    # avoid the rebound
                    if tile.y > self.y_temp:
                        # sticks to tile             
                        self.rect.y = tile.y - self.rect.height
                        self.on_ground = True
                        
                # toxic waste and lava, one life less            
                elif self.map.tilemap_behaviour_list[index] == enums.KILLER:
                    self.loses_life()
                    self.scoreboard.invalidate()
                    # makes a preventive jump (this time without dust)
                    self.direction.y = constants.JUMP_VALUE

        if not collision:
            self.rect.y = self.y_temp # apply the new Y position
            self.on_ground = False

        # landing, creating some dust
        if self.state == enums.FALLING and self.on_ground:
            self.dust_effect(self.rect.center, self.state)

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
        # invincible effect (the player blinks)
        if self.invincible: self.image.set_alpha(self.wave_value()) # 0 or 255
        else: self.image.set_alpha(255) # without transparency
    
    # subtracts one life and applies temporary invincibility
    def loses_life(self):
        if not self.invincible:
            self.lives -= 1
            self.invincible = True
            self.invincible_time_from = pygame.time.get_ticks()

    # controls the invincibility time
    def invincibility_timer(self):
        if self.invincible:
            if (pygame.time.get_ticks() - self.invincible_time_from) \
            >= self.invincible_time_to:
                self.invincible = False

    # returns the value 0 or 255 depending on the number of ticks.
    def wave_value(self):
        if sin(pygame.time.get_ticks()) >= 0: return 255
        else: return 0

    def update(self):
        self.get_input()
        self.get_state()
        self.horizontal_mov()
        self.vertical_mov()
        self.animate()
        self.invincibility_timer()