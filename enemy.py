
#===============================================================================
# Enemy class
#===============================================================================

import pygame
import enums
import constants
import support


class Enemy(pygame.sprite.Sprite):
    def __init__(self, enemy_data, player_rect):
        # enemy_data = (x1, y1, x2, y2, vx, vy, type)
        super().__init__()
        self.player = player_rect # player's current position
        # from xy values
        self.x = self.x1 = enemy_data[0]
        self.y = self.y1 = enemy_data[1]
        # to xy values
        self.x2 = enemy_data[2]
        self.y2 = enemy_data[3]
        # speed (pixels per frame)
        self.vx = enemy_data[4]
        self.vy = enemy_data[5]
        # enemy type (and name, to load the image)
        self.type = enemy_data[6]
        if self.type == enums.INFECTED:
            enemy_name = 'infected'
        elif self.type == enums.PELUSOID:
            enemy_name = 'pelusoid'
        elif self.type == enums.AVIRUS:
            enemy_name = 'avirus'
        elif self.type == enums.PLATFORM_SPR:
            enemy_name = 'platform'
        elif self.type == enums.FANTY:
            enemy_name = 'fanty'  
            self.state = enums.IDLE          
            self.sight_distance = 1.0 # x64 pixels/frame
            self.acceleration = 0.05 # pixels/frame
            self.max_speed = 2.0 # pixels/frame
        # images
        self.image_list = []
        for i in range(2): # only 2 frames per enemy
            # image for the frame
            self.image_list.append(pygame.image.load('images/sprites/' + enemy_name + str(i) + '.png'))
            self.image_list[i].convert_alpha()
        self.frame_index = 0 # frame number
        self.animation_timer = 12 # timer to change frame
        self.animation_speed = 12 # frame dwell time
        self.image = self.image_list[0]
        self.rect = self.image.get_rect()

    def animate(self):
        self.animation_timer += 1
        # exceeded the frame time?
        if self.animation_timer >= self.animation_speed:
            self.animation_timer = 0 # reset the timer
            self.frame_index += 1 # next frame
        # exceeded the number of frames?
        if self.frame_index > len(self.image_list) - 1:
            self.frame_index = 0 # reset the frame number
        # assigns the original or inverted image:
        # moving to the right, or idle looking at the player
        if self.vx > 0 or (self.vx == 0 and self.player.x >= self.x):
            self.image = self.image_list[self.frame_index]
        # moving to the left, or idle looking at the player
        elif self.vx < 0 or (self.vx == 0 and self.player.x < self.x):
            self.image = pygame.transform.flip(self.image_list[self.frame_index], True, False)

    def update(self):
        # movement
        if self.type != enums.FANTY: # no fanty  
            self.x += self.vx
            self.y += self.vy
            if self.x == self.x1 or self.x == self.x2:
                self.vx = -self.vx
            if self.y == self.y1 or self.y == self.y2:
                self.vy = -self.vy
        else: # fanty
            # >>6 is equivalent to dividing by 64 (more efficient)
            # gpx = int(self.player.x) >> 6
            # gpy = int(self.player.y) >> 6
            # gpen_cx = int(self.x) >> 6
            # gpen_cy = int(self.y) >> 6
            gpx = self.player.x / 64
            gpy = self.player.y / 64
            gpen_cx = self.x / 64
            gpen_cy = self.y / 64
            if self.state == enums.IDLE:                
                if support.distance (gpx, gpy, gpen_cx, gpen_cy) <= self.sight_distance:
                    print (support.distance (gpx, gpy, gpen_cx, gpen_cy))
                    # close to the player, chases him
                    self.state = enums.CHASING
            elif self.state == enums.CHASING:
                if support.distance (gpx, gpy, gpen_cx, gpen_cy) > self.sight_distance:
                    # away from the player, stops the chase and retreats
                    self.state = enums.RETREATING
                else:
                    # moves according to the value of several variables
                    self.vx = support.limit(self.vx + support.addsign(self.player.x - self.x, self.acceleration), -self.max_speed, self.max_speed)
                    self.vy = support.limit(self.vy + support.addsign(self.player.y - self.y, self.acceleration), -self.max_speed, self.max_speed)
                    # applies the new position, 
                    # but keeps it within the boundaries of the screen.
                    self.x = support.limit(self.x + self.vx, 0, constants.MAP_UNSCALED_SIZE[0])
                    self.y = support.limit(self.y + self.vy, 0, constants.MAP_UNSCALED_SIZE[1])
            else: # retreating; going back to the starting point
                self.x += support.addsign(self.x1 - int(self.x), 1)
                self.y += support.addsign(self.y1 - int(self.y), 1)
                # close to the player, chases him again!
                if support.distance(gpx, gpy, gpen_cx, gpen_cy) <= self.sight_distance:
                    self.state = enums.CHASING		

            if self.state == enums.RETREATING:
                if (self.x1 >= self.x-1 and self.x1 <= self.x+1) \
                and (self.y1 >= self.y-1 and self.y1 <= self.y+1):
                    # very close to the starting point; switch to IDLE
                    self.state = enums.IDLE
                    self.x = self.x1
                    self.y = self.y1      
						
        # applies the calculated position and the corresponding frame
        self.rect.x = self.x
        self.rect.y = self.y
        self.animate()
