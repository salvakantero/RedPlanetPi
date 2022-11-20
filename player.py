#===============================================================================
# Player class
#===============================================================================

import pygame
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
        # properties for the dust effect
        self.dust_image_list = dust_image_list
        self.sprites_group = all_sprites_group

    # dust effect when jumping
    def jumping_dust(self,pos):
        jumping_dust_sprite = dust.DustEffect(pos, 
            self.dust_image_list[enums.JUMPING])
        self.sprites_group.add(jumping_dust_sprite)

    # dust effect on landing
    def landing_dust(self,pos):
        landing_dust_sprite = dust.DustEffect(pos, 
            self.dust_image_list[enums.FALLING])
        self.sprites_group.add(landing_dust_sprite)

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
                # landing, creating some dust
                if self.state == enums.FALLING:
                    self.landing_dust(self.rect.center) # dust effect
                self.state = enums.IDLE
            elif self.y_speed >= 1:
                self.state = enums.FALLING
        # press jump
        if key_state[config.jump_key] and self.on_ground:
            self.y_speed = globalvars.JUMP_VALUE
            self.state = enums.JUMPING
            self.jumping_dust(self.rect.center) # dust effect

    def horizontal_mov(self):
        # gets the new rectangle and check for collision
        temp_rect = pygame.Rect((self.temp_x,self.rect.y), 
            (globalvars.TILE_WIDTH, globalvars.TILE_HEIGHT))      
        if temp_rect.collidelist(tiled.tilemap_rect_list) == -1:
            self.rect.x = self.temp_x # no collision. Apply the new position X

    def vertical_mov(self):
        # applies acceleration of gravity
        self.y_speed += globalvars.GRAVITY
        self.temp_y += self.y_speed
        # gets the new rectangle and check for collision
        temp_rect = pygame.Rect((self.rect.x, self.temp_y), 
            (globalvars.TILE_WIDTH, globalvars.TILE_HEIGHT))        
        index = temp_rect.collidelist(tiled.tilemap_rect_list)         
        if index == -1: # no collision            
            self.rect.y = self.temp_y # apply the new position Y
            self.on_ground = False
        else: # collision
            if (tiled.tilemap_behaviour_list[index] == enums.OBSTACLE):        
                self.y_speed = 0 # stops the player
                # avoid the rebound
                tile = tiled.tilemap_rect_list[index]
                if tile.y > self.temp_y: # sticks to platform                    
                    self.rect.y = tile.y - globalvars.TILE_HEIGHT
                    self.on_ground = True   
            # toxic waste and lava             
            elif (tiled.tilemap_behaviour_list[index] == enums.KILLER):
                self.lives -= 1
                globalvars.refresh_scoreboard = True
                # makes a preventive jump (this time without dust)
                self.y_speed = globalvars.JUMP_VALUE
                self.state = enums.JUMPING

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