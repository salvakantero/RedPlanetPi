
#===============================================================================
# Player class
# movement and animations, collisions with the map
#===============================================================================

import pygame
import random
from math import sin
import constants
import enums
from dust import DustEffect
from bullet import Bullet

class Player(pygame.sprite.Sprite):
    def __init__(self, dust_image_list, all_sprites_group, dust_group, bullet_group, map, scoreboard, config):
        super().__init__()
        # attributes
        self.lives = 10 # lives remaining
        self.ammo = 5 # unused ammunition collected
        self.keys = 0 # unused keys collected 
        self.TNT = 0 # explosives collected  
        self.oxygen = constants.MAX_OXYGEN # oxygen remaining
        self.stacked_TNT = False # the 15 TNT charges have been placed?
        self.win = False # Detonated charge?
        self.direction = pygame.math.Vector2(0.0) # direction of movement
        self.x_speed = 2 # movement in the x-axis (pixels)
        self.y_jump = constants.MAP_UNSCALED_SIZE[1] # Y value when jumping (to detect large jumps)
        self.state = enums.IDLE # to know the animation to be applied
        self.facing_right = True # to know if the sprite needs to be mirrored
        self.on_ground = False # perched on the ground   
        self.invincible = False # invincible after losing a life
        self.invincible_time_from = 0 # tick number where invincibility begins
        self.invincible_time_to = constants.INVINCIBLE_TIME # time of invincibility (2 secs.)
        self.oxygen_time_from = pygame.time.get_ticks() # tick number where oxygen unit begins
        self.oxygen_time_to = constants.OXYGEN_TIME # consumption time of each oxygen unit (2 secs.)
        # image/animation        
        self.image_list = {
            # sequences of animations for the player depending on its status
            enums.IDLE: [
                pygame.image.load('images/sprites/player0.png').convert_alpha(),
                pygame.image.load('images/sprites/player1.png').convert_alpha()],
            enums.WALKING: [
                pygame.image.load('images/sprites/player2.png').convert_alpha(),
                pygame.image.load('images/sprites/player0.png').convert_alpha(),
                pygame.image.load('images/sprites/player3.png').convert_alpha(),
                pygame.image.load('images/sprites/player0.png').convert_alpha()],
            enums.JUMPING: [
                pygame.image.load('images/sprites/player4.png').convert_alpha()],
            enums.FALLING: [
                pygame.image.load('images/sprites/player5.png').convert_alpha()]
        }
        self.frame_index = 0 # frame number
        self.animation_timer = 16 # timer to change frame
        self.animation_speed = 16 # frame dwell time
        self.image = self.image_list[self.state][0] # 1st frame of the animation
        self.rect = self.image.get_rect(topleft = (16,112))  # initial position
        # the FIRING state is independent of the other states and requires 
        # a specific image for a certain number of frames
        self.firing = 0 # frame counter
        self.image_firing = pygame.image.load('images/sprites/player6.png').convert_alpha()
        # dust effect
        self.dust_image_list = dust_image_list 
        self.dust_group = dust_group
        # sounds
        self.sfx_jump = (
            pygame.mixer.Sound('sounds/fx/sfx_jump1.wav'),
            pygame.mixer.Sound('sounds/fx/sfx_jump2.wav'),
            pygame.mixer.Sound('sounds/fx/sfx_jump3.wav'),
            pygame.mixer.Sound('sounds/fx/sfx_jump4.wav'))
        for i in range(4): self.sfx_jump[i].set_volume(0.3)
        self.sfx_landing = pygame.mixer.Sound('sounds/fx/sfx_landing.wav')
        self.sfx_landing.set_volume(0.2)
        self.sfx_shot = pygame.mixer.Sound('sounds/fx/sfx_shot.wav')
        self.sfx_no_ammo = pygame.mixer.Sound('sounds/fx/sfx_no_ammo.wav')
        self.sfx_no_ammo.set_volume(0.8)
        self.sfx_death = pygame.mixer.Sound('sounds/fx/sfx_death.wav')
        self.sfx_alarm = pygame.mixer.Sound('sounds/fx/sfx_alarm.wav')
        self.sfx_TNT = pygame.mixer.Sound('sounds/fx/sfx_TNT.wav')        
        
        # objects and others
        self.all_sprites_group = all_sprites_group   
        self.bullet_group = bullet_group
        self.map = map
        self.scoreboard = scoreboard
        self.config = config

    # dust effect when jumping or landing
    def dust_effect(self, pos, state):
        if self.dust_group.sprite == None:        
            dust_sprite = DustEffect(pos, self.dust_image_list[state])
            self.dust_group.add(dust_sprite)
            self.all_sprites_group.add(dust_sprite)

    def get_input(self):
        # manages keystrokes
        key_state = pygame.key.get_pressed()  
        # press right ----------------------------------------------------------
        if key_state[self.config.right_key]:
            self.direction.x = 1
            self.facing_right = True
        # press left -----------------------------------------------------------
        elif key_state[self.config.left_key]:
            self.direction.x = -1
            self.facing_right = False
        # without lateral movement ---------------------------------------------
        elif not key_state[self.config.right_key] and not key_state[self.config.left_key]:
            self.direction.x = 0
        # press jump -----------------------------------------------------------
        if key_state[self.config.jump_key] and self.on_ground:            
            self.direction.y = constants.JUMP_VALUE
            self.on_ground = False
            self.y_jump = self.rect.y # to detect large jumps on landing            
            self.dust_effect(self.rect.center, enums.JUMPING)
            # randomly plays one of the four jumping sounds
            self.sfx_jump[random.randint(0, 3)].play()
        # press fire -----------------------------------------------------------
        if key_state[self.config.fire_key]:
            if self.ammo > 0:
                if self.bullet_group.sprite == None: # no shots on screen        
                    bullet = Bullet(self.rect, self.facing_right)
                    self.bullet_group.add(bullet)
                    self.all_sprites_group.add(bullet)
                    self.sfx_shot.play()
                    self.ammo -= 1
                    self.scoreboard.invalidate()
                    self.firing = 12 # frames drawing the image "firing".
            else: # no bullets
                self.sfx_no_ammo.play()
        # press action ---------------------------------------------------------
        if key_state[self.config.action_key]:
            action_taken = False
            # stacking explosives
            if self.map.number == 44 \
            and self.rect.x > 90 and self.rect.x < 165 \
            and self.rect.y == 96 and self.TNT == 15:  
                    self.stacked_TNT = True
                    self.TNT = 0
                    self.scoreboard.game_percent += 5
                    self.scoreboard.invalidate()
                    self.map.add_TNT_pile()                  
                    self.sfx_TNT.play()
                    action_taken = True
            # detonate explosives
            elif self.map.number == 0 \
            and self.rect.x < 25 and self.rect.y == 112 and self.stacked_TNT:
                    self.win = True
                    action_taken = True
            # no action required
            if not action_taken:   
                self.sfx_no_ammo.play()            

    def get_state(self):
        if self.direction.y < 0: # decrementing Y. Jumping
            self.state = enums.JUMPING
        elif self.direction.y > 1: # increasing Y. Falling
            self.state = enums.FALLING
            self.on_ground = False
        else:
            if self.direction.x != 0: # is moving
                self.state = enums.WALKING
            else: # x does not change. Stopped
                self.state = enums.IDLE

    def horizontal_mov(self):
        # gets the new rectangle and check for collision
        x_temp = self.rect.x + (self.direction.x * self.x_speed)
        temp_rect = pygame.Rect((x_temp, self.rect.y),
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
            self.rect.x = x_temp # apply the new X position

    def vertical_mov(self):        
        # applies acceleration of gravity up to the vertical speed limit.
        # a fall speed limit is necessary to avoid affecting collisions.
        if self.direction.y < constants.MAX_Y_SPEED:
            self.direction.y += constants.GRAVITY
            
        # gets the new rectangle and check for collision
        y_temp = self.rect.y + self.direction.y
        temp_rect = pygame.Rect((self.rect.x, y_temp), 
            (self.rect.width, self.rect.height))  

        collision = False # True if at least one tile collides
        index = -1 # index of the colliding tile to obtain its type
        # it is necessary to check all colliding tiles.
        for tile in self.map.tilemap_rect_list:
            index += 1
            if tile.colliderect(temp_rect):
                collision = True

                # fixed platform, only stops from above ------------------------
                if self.map.tilemap_behaviour_list[index] == enums.PLATFORM_TILE:   
                    # if the player is not jumping (if not climbing)    
                    if (self.state is not enums.JUMPING):
                        # if the lower part of the player is below 
                        # the upper part of the platform
                        if tile.y > y_temp + 12:
                            # sticks to platform                
                            self.rect.y = tile.y - self.rect.height
                            self.on_ground = True
                            self.direction.y = 0  
                        # if the player is not on top of the platform
                        # it keeps moving
                        else: collision = False
                    # if it's jumping it keeps moving
                    else: collision = False

                # obstacles, stops the player from all directions --------------      
                elif self.map.tilemap_behaviour_list[index] == enums.OBSTACLE:
                    self.direction.y = 0
                    # avoid the rebound
                    if tile.y > y_temp:
                        # sticks to tile             
                        self.rect.y = tile.y - self.rect.height
                        self.on_ground = True
                        
                # toxic waste and lava, one life less --------------------------           
                elif self.map.tilemap_behaviour_list[index] == enums.KILLER:
                    self.loses_life()
                    self.scoreboard.invalidate()
                    # makes a preventive jump (this time without dust)
                    self.direction.y = constants.JUMP_VALUE

        if not collision:
            self.rect.y = y_temp # apply the new Y position

        # landing, creating some dust and shaking the map
        if self.state == enums.FALLING and self.on_ground:
            self.dust_effect(self.rect.center, self.state)
            self.sfx_landing.play()
            # large jump?
            if self.rect.y > self.y_jump:                
                self.map.shake = [0, 4]
                self.map.shake_timer = 4
                self.y_jump = constants.MAP_UNSCALED_SIZE[1]
                
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
        if self.firing == 0: # normal sequence of images
            if self.facing_right:
                self.image = self.image_list[self.state][self.frame_index]
            else: # reflects the image when looking to the left
                self.image = pygame.transform.flip(self.image_list[self.state][self.frame_index], True, False)
        else: # frame firing
            self.firing -= 1
            if self.facing_right: self.image = self.image_firing
            else: self.image = pygame.transform.flip(self.image_firing, True, False)            
        # invincible effect (the player blinks)
        if self.invincible: self.image.set_alpha(self.wave_value()) # 0 or 255
        else: self.image.set_alpha(255) # without transparency
    
    # subtracts one life and applies temporary invincibility
    def loses_life(self):
        if not self.invincible:
            self.lives -= 1
            self.sfx_death.play()
            self.invincible = True
            self.invincible_time_from = pygame.time.get_ticks()

    # controls the invincibility time
    def invincibility_timer(self):
        if self.invincible:
            if (pygame.time.get_ticks() - self.invincible_time_from) >= self.invincible_time_to:
                self.invincible = False

    # returns the value 0 or 255 depending on the number of ticks.
    def wave_value(self):
        if sin(pygame.time.get_ticks()) >= 0: return 255
        else: return 0

    # controls the oxygen time
    def oxygen_timer(self):
        if (pygame.time.get_ticks() - self.oxygen_time_from) >= self.oxygen_time_to:
            self.oxygen -= 1
            if self.oxygen <= 10: self.sfx_alarm.play()
            self.scoreboard.invalidate()
            self.oxygen_time_from = pygame.time.get_ticks()

    def update(self):
        self.get_input()
        self.get_state()
        self.horizontal_mov()
        self.vertical_mov()
        self.animate()
        self.invincibility_timer()
        self.oxygen_timer()