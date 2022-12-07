
#===============================================================================
# Player class
#===============================================================================

import pygame
from math import sin
import globalvars
import enums
import config
import tiled
import dust

class Player(pygame.sprite.Sprite):
    def __init__(self, image_list, dust_image_list, all_sprites_group):
        super().__init__()
        # external properties
        self.lives = 10 # lives remaining
        self.oxigen = 99 # oxigen remaining
        self.ammo = 5 # unused ammunition collected
        self.keys = 0 # unused keys collected 
        self.explosives = 0 # explosives collected  
        # internal properties
        self.status = enums.IDLE # to know the animation to be applied
        self.facing_right = True # to know if the sprite needs to be mirrored
        self.on_ground = False # perched on the ground
        self.y_speed = 0 # motion + gravity
        self.invincible = False # invincible after losing a life
        self.invincible_time_from = 0 # tick number where invincibility begins
        self.invincible_time_to = 1000 # time of invincibility (1 sec.)
        # image/animation
        self.image_list = image_list # list of images for animation
        self.frame_index = 0 # frame_number
        self.animation_timer = 16 # timer to change frame
        self.animation_speed = 16 # frame dwell time
        self.image = image_list[enums.IDLE][0] # 1st frame of the animation
        self.rect = self.image.get_rect(topleft = (16,112))  # initial position
        # properties for the dust effect
        self.dust_image_list = dust_image_list
        self.sprites_group = all_sprites_group

        # NUEVO /////////////////////////////////////////////////////////////
        self.direction = pygame.math.Vector2(0,0) # vector de XY
        self.speed = 2 # pixels        
        self.on_ceiling = False
        self.on_left = False
        self.on_right = False
        self.collision_rect = pygame.Rect(
            self.rect.topleft,(12,self.rect.height))

    # dust effect when jumping or landing
    def dust_effect(self, pos, status):
        if not globalvars.dust_in_progress:            
            dust_sprite = dust.DustEffect(pos, self.dust_image_list[status])
            self.sprites_group.add(dust_sprite)
            globalvars.dust_in_progress = True

    def get_input(self):
        # XY temporary to check for collision at the new position
        #self.temp_x = self.rect.x 
        #self.temp_y = self.rect.y

        # manages keystrokes
        key_status = pygame.key.get_pressed()   
        # press left
        if key_status[config.left_key]:
            # self.temp_x -= 2
            self.direction.x = -1
            self.facing_right = False
            # self.state = enums.WALKING
        # press right
        elif key_status[config.right_key]: # if -> elif
            # self.temp_x += 2
            self.direction.x = 1
            self.facing_right = True
            # self.state = enums.WALKING
        else:
            self.direction.x = 0

        # without lateral movement
        # if not key_state[config.left_key] and not key_state[config.right_key]:
        #     if self.on_ground:
        #         # landing, creating some dust
        #         if self.state == enums.FALLING:
        #             self.dust_effect(self.rect.center, self.state)
        #         self.state = enums.IDLE
        #     elif self.y_speed >= 1:
        #         self.state = enums.FALLING

        # press jump
        if key_status[config.jump_key] and self.on_ground:
            #self.y_speed = globalvars.JUMP_VALUE
            #self.state = enums.JUMPING
            self.direction.y = globalvars.JUMP_VALUE
            self.dust_effect(self.rect.center, enums.JUMPING)

    # obtiene estados
    def get_status(self):
        if self.direction.y < 0: # se está decrementando y; saltando
            self.status = enums.JUMPING
        elif self.direction.y > 1: # está aumentando y; cayendo
            self.status = enums.FALLING
        else:
            if self.direction.x != 0: # está cambiando x; en marcha
                self.status = enums.WALKING
            else:
                self.status = enums.IDLE # x no cambia; parado

    # aplica gravedad aumentando Y
    def apply_gravity(self):
        self.direction.y += globalvars.GRAVITY
        self.collision_rect.y += self.direction.y

    def horizontal_mov(self):
        # # gets the new rectangle and check for collision
        # temp_rect = pygame.Rect((self.temp_x,self.rect.y),
        #     (self.rect.width, self.rect.height))      
        # index = temp_rect.collidelist(tiled.tilemap_rect_list) 
        # # no collision, or collides with a platform
        # if index == -1 or tiled.tilemap_behaviour_list[index] == enums.PLATFORM:
        #     self.rect.x = self.temp_x # apply the new position X 

        self.collision_rect.x += self.direction.x * self.speed
        # grupos de sprites que colisionan con el player
        for tile in tiled.tilemap_rect_list:
            if tile.colliderect(self.collision_rect):
                if self.direction.x < 0: 
                    self.collision_rect.left = self.rect.right
                    self.on_left = True
                    self.current_x = self.rect.left # fija el valor de x por la izda.
                elif self.direction.x > 0:
                    self.collision_rect.right = self.rect.left
                    self.on_right = True
                    self.current_x = self.rect.right # fija el valor de x por la derecha

    def vertical_mov(self):
        # # applies acceleration of gravity
        # self.y_speed += globalvars.GRAVITY
        # self.temp_y += self.y_speed

        # # gets the new rectangle and check for collision
        # temp_rect = pygame.Rect((self.rect.x, self.temp_y), 
        #     (self.rect.width, self.rect.height))        
        # index = temp_rect.collidelist(tiled.tilemap_rect_list) 

        # if index == -1: # no collision            
        #     self.rect.y = self.temp_y # apply the new position
        #     self.on_ground = False  

        # else: # collision
        #     # platform, only stops from above
        #     if tiled.tilemap_behaviour_list[index] == enums.PLATFORM:   
        #         # if the player is not jumping (if not climbing)    
        #         if (self.status is not enums.JUMPING):
        #             # if the lower part of the player is below 
        #             # the upper part of the platform
        #             tile = tiled.tilemap_rect_list[index]
        #             if tile.y > self.temp_y + 12:
        #                 # sticks to platform                
        #                 self.rect.y = tile.y - self.rect.height
        #                 self.on_ground = True
        #                 self.y_speed = 0  
        #             # if the player is not on top of the platform
        #             # it keeps moving
        #             else:
        #                 self.rect.y = self.temp_y
        #                 self.on_ground = False
        #         # if it's jumping it keeps moving
        #         else:
        #             self.rect.y = self.temp_y
        #             self.on_ground = False

        #     # obstacles, stops the player from all directions
        #     elif tiled.tilemap_behaviour_list[index] == enums.OBSTACLE:        
        #         self.y_speed = 0
        #         # avoid the rebound
        #         tile = tiled.tilemap_rect_list[index]
        #         if tile.y > self.temp_y:
        #             # sticks to platform                    
        #             self.rect.y = tile.y - self.rect.height
        #             self.on_ground = True 
              
        #     # toxic waste and lava, one life less            
        #     elif tiled.tilemap_behaviour_list[index] == enums.KILLER:
        #         self.loses_life()
        #         # makes a preventive jump (this time without dust)
        #         self.y_speed = globalvars.JUMP_VALUE
        #         self.status = enums.JUMPING

        self.apply_gravity() # aplica gravedad siempre
        
        for tile in tiled.tilemap_rect_list:
            if tile.colliderect(self.collision_rect):
                if self.direction.y > 0: 
                    self.collision_rect.bottom = tile.top
                    self.direction.y = 0 # para el movimiento
                    self.on_ground = True # en tierra
                    if self.status == enums.FALLING:
                        self.dust_effect(self.rect.center, enums.FALLING)
                elif self.direction.y < 0:
                    self.collision_rect.top = tile.bottom
                    self.direction.y = 0 # para el movimiento
                    self.on_ceiling = True # tocando techo

        # si hay movimiento en Y, desactiva el flag "en tierra"
        if self.on_ground and self.direction.y < 0 or self.direction.y > 1:
            self.on_ground = False

    # selects an image according to frame number or player status
    def animate(self):
        # animation speed
        if (self.status == enums.WALKING):
            self.animation_speed = 6 # running fast
        else:
            self.animation_speed = 16 # breathing, jumping, falling          

        self.animation_timer += 1
        # exceeded the frame time?
        if self.animation_timer >= self.animation_speed:
            self.animation_timer = 0 # reset the timer
            self.frame_index += 1 # next frame
        # exceeded the number of frames?
        if self.frame_index > len(self.image_list[self.status]) - 1:
            self.frame_index = 0 # reset the frame number

        # assigns image according to frame, status and direction
        image = self.image_list[self.status][self.frame_index]
        if self.facing_right:
            self.image = image
            self.rect.bottomleft = self.collision_rect.bottomleft # ///////////
        else: # reflects the image when looking to the left
            self.image = pygame.transform.flip(image, True, False)
            self.rect.bottomright = self.collision_rect.bottomright # /////////

        # invincible effect (the player blinks)
        if self.invincible: self.image.set_alpha(self.wave_value()) # 0 or 255
        else: self.image.set_alpha(255) # without transparency
    
        self.rect = self.image.get_rect(midbottom = self.rect.midbottom) # ////

    # subtracts one life and applies temporary invincibility
    def loses_life(self):
        if not self.invincible:
            self.lives -= 1
            self.invincible = True
            self.invincible_time_from = pygame.time.get_ticks()
            globalvars.refresh_scoreboard = True

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
        self.get_status()
        self.horizontal_mov()
        self.vertical_mov()
        self.animate()
        self.invincibility_timer()